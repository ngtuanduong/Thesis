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

  private get execEnv(): Record<string, string> {
    return { ...process.env as Record<string, string> };
  }

  async ensureSandboxImage(): Promise<void> {
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
      if (error.killed || error.signal === 'SIGTERM') {
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
    // For simple problems, we'll parse the input and inject it
    // This is a simplified approach - in production, you'd want more sophisticated handling
    let parsedInput: any;
    try {
      parsedInput = JSON.parse(input);
    } catch {
      parsedInput = input;
    }

    // Wrap the user's code to provide input
    return `
import json
import sys

# User's solution
${code}

# Test input
test_input = ${JSON.stringify(parsedInput)}

# Execute and print result
try:
    if isinstance(test_input, dict):
        result = solution(**test_input)
    elif isinstance(test_input, list):
        result = solution(*test_input)
    else:
        result = solution(test_input)

    print(json.dumps(result) if not isinstance(result, str) else result)
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
