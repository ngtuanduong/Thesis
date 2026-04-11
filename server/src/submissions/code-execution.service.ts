import { Injectable, Logger } from '@nestjs/common';
import { exec } from 'child_process';
import { promisify } from 'util';
import { writeFile, unlink, mkdir } from 'fs/promises';
import { join } from 'path';
import { randomUUID } from 'crypto';
import { SubmissionStatus } from '@prisma/client';

const execAsync = promisify(exec);

interface TestCase {
  input: string;
  expected: string;
}

interface ExecutionResult {
  status: SubmissionStatus;
  output: string;
  runtime?: number;
  memory?: number;
  error?: string;
}

@Injectable()
export class CodeExecutionService {
  private readonly logger = new Logger(CodeExecutionService.name);
  private readonly sandboxImage = 'code-sandbox:latest';
  private readonly timeoutMs = 5000; // 5 seconds
  private readonly memoryLimit = '256m';
  private readonly cpuLimit = '0.5';
  // Cache the sandbox-image check so we don't invoke `docker info` + `docker
  // images -q` on every submission. On Windows each Docker CLI call is
  // ~1-2s, and doing 2 extra calls per submission × 170 problems adds ~10min
  // of overhead and pushes some submissions past the verify script's poll
  // timeout. Memoizing keeps the first call correct and all subsequent calls
  // effectively free.
  private sandboxReady: Promise<void> | null = null;

  private get execEnv(): Record<string, string> {
    return { ...process.env as Record<string, string> };
  }

  /** Verify Docker is available and build the sandbox image if it doesn't exist. */
  async ensureSandboxImage(): Promise<void> {
    if (this.sandboxReady) return this.sandboxReady;
    this.sandboxReady = this.checkSandboxImage().catch((e) => {
      // Clear cache on failure so a retry can re-check.
      this.sandboxReady = null;
      throw e;
    });
    return this.sandboxReady;
  }

  private async checkSandboxImage(): Promise<void> {
    try {
      // Verify Docker is available and responsive
      await execAsync('docker info', { env: this.execEnv });
    } catch (error: any) {
      const msg = error.message || '';
      if (msg.includes('API version') || msg.includes('too old')) {
        throw new Error(
          'Docker API version mismatch. Your Docker CLI is too old for the Docker daemon. ' +
          'Install a newer Docker CLI (v24+) or set DOCKER_API_VERSION to match your daemon.',
        );
      }
      throw new Error(
        'Docker is not available. Ensure Docker is installed and the daemon is running. ' +
        `Details: ${msg}`,
      );
    }

    try {
      const { stdout } = await execAsync(
        `docker images -q ${this.sandboxImage}`,
        { env: this.execEnv },
      );
      if (!stdout.trim()) {
        this.logger.log('Building sandbox Docker image...');
        const dockerfilePath = join(process.cwd(), '..', 'docker', 'sandbox');
        await execAsync(
          `docker build -t ${this.sandboxImage} ${dockerfilePath}`,
          { env: this.execEnv },
        );
        this.logger.log('Sandbox image built successfully');
      }
    } catch (error) {
      this.logger.error('Failed to ensure sandbox image', error);
      throw error;
    }
  }

  /**
   * Execute student code against test cases in an isolated Docker container.
   *
   * Flow: ensure sandbox image -> iterate test cases -> for each test, write code
   * to a temp file, run it in a memory/CPU-limited container with no network,
   * compare output to expected. Stops on first failure.
   *
   * @param code - The student's source code.
   * @param language - Programming language (currently only "python" supported).
   * @param testCases - Array of input/expected-output pairs.
   * @returns Execution result with status, output, runtime, and optional error.
   */
  async executeCode(
    code: string,
    language: string,
    testCases: TestCase[],
  ): Promise<ExecutionResult> {
    await this.ensureSandboxImage();

    if (language !== 'python') {
      return {
        status: SubmissionStatus.RUNTIME_ERROR,
        output: '',
        error: 'Only Python is currently supported',
      };
    }

    const results: Array<{ passed: boolean; output: string; expected: string }> = [];
    let totalRuntime = 0;

    for (const testCase of testCases) {
      const result = await this.runSingleTest(code, testCase);

      if (result.status !== SubmissionStatus.ACCEPTED) {
        return result;
      }

      const passed = this.compareOutputs(result.output.trim(), testCase.expected.trim());
      results.push({
        passed,
        output: result.output.trim(),
        expected: testCase.expected.trim(),
      });

      totalRuntime += result.runtime || 0;

      if (!passed) {
        return {
          status: SubmissionStatus.WRONG_ANSWER,
          output: `Expected: ${testCase.expected}\nGot: ${result.output}`,
          runtime: totalRuntime,
        };
      }
    }

    return {
      status: SubmissionStatus.ACCEPTED,
      output: 'All test cases passed',
      runtime: totalRuntime,
    };
  }

  private async runSingleTest(
    code: string,
    testCase: TestCase,
  ): Promise<ExecutionResult> {
    const executionId = randomUUID();
    const tempDir = join('/tmp', 'code-execution', executionId);
    const codeFile = join(tempDir, 'solution.py');

    try {
      // Create temp directory
      await mkdir(tempDir, { recursive: true });

      // Write code to file
      const codeWithInput = this.prepareCode(code, testCase.input);
      await writeFile(codeFile, codeWithInput);

      // Execute in Docker sandbox - use base64 to avoid escaping issues
      const startTime = Date.now();
      const codeBase64 = Buffer.from(codeWithInput).toString('base64');
      const dockerCommand = `docker run --rm \
        --memory=${this.memoryLimit} \
        --cpus=${this.cpuLimit} \
        --network=none \
        ${this.sandboxImage} \
        sh -c "echo '${codeBase64}' | base64 -d | timeout ${this.timeoutMs / 1000} python3"`;

      const { stdout, stderr } = await execAsync(dockerCommand, {
        timeout: this.timeoutMs + 1000,
        env: this.execEnv,
      });

      const runtime = Date.now() - startTime;

      if (stderr && !stdout) {
        return {
          status: SubmissionStatus.RUNTIME_ERROR,
          output: stderr,
          runtime,
          error: stderr,
        };
      }

      return {
        status: SubmissionStatus.ACCEPTED,
        output: stdout,
        runtime,
      };
    } catch (error: any) {
      // Detect timeout/killed scenarios. On Linux error.killed is true and
      // error.signal is 'SIGTERM'. On Windows (Docker Desktop / WSL2) the
      // signal may not propagate, so also check:
      //   - exit code 124 (from `timeout` command inside the container)
      //   - exit code 137 (SIGKILL / OOM-killer)
      //   - Node's execAsync timeout sets error.killed
      const isTimeout =
        error.killed ||
        error.signal === 'SIGTERM' ||
        error.signal === 'SIGKILL' ||
        error.code === 124 ||
        error.code === 137;
      if (isTimeout) {
        return {
          status: SubmissionStatus.TIME_LIMIT,
          output: '',
          error: 'Time limit exceeded',
        };
      }

      // Extract the meaningful error from stderr, stripping the docker command prefix
      const stderr = error.stderr || '';
      const cleanError = stderr.trim() || error.message.replace(/^Command failed:.*?\n?/, '').trim();

      return {
        status: SubmissionStatus.RUNTIME_ERROR,
        output: cleanError,
        error: cleanError,
      };
    } finally {
      // Cleanup
      try {
        await unlink(codeFile);
      } catch {
        // Ignore cleanup errors
      }
    }
  }

  private prepareCode(code: string, input: string): string {
    // Embed the raw test-case input as a Python string literal and let Python
    // parse it with json.loads. This avoids two bugs from the previous approach
    // (JSON.stringify the parsed value into Python source):
    //   1. JS booleans/null serialize as `true`/`false`/`null` which are not
    //      Python literals → NameError.
    //   2. Round-tripping through JS JSON loses type info for some edge cases.
    // Using json.loads also means the output is always JSON-encoded, so string
    // results come back as `"hello"` matching JSON-stringified expected values.
    const rawInputLiteral = JSON.stringify(input);

    return `
import json
import sys

# User's solution
${code}

# Test input — parse the raw JSON string; fall back to the raw string for bare scalars
_raw_input = ${rawInputLiteral}
try:
    test_input = json.loads(_raw_input)
except (json.JSONDecodeError, ValueError):
    test_input = _raw_input

# Execute and print result (always json.dumps for consistent comparison)
try:
    if isinstance(test_input, dict):
        result = solution(**test_input)
    elif isinstance(test_input, list):
        result = solution(*test_input)
    else:
        result = solution(test_input)

    print(json.dumps(result))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
`;
  }

  private compareOutputs(actual: string, expected: string): boolean {
    // Try to parse as JSON for structured comparison
    try {
      const actualParsed = JSON.parse(actual);
      const expectedParsed = JSON.parse(expected);
      return JSON.stringify(actualParsed) === JSON.stringify(expectedParsed);
    } catch {
      // Fallback to string comparison
      return actual === expected;
    }
  }
}
