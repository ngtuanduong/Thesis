# Claude Code Configuration
Do not commit anything with claude or Anthropic contribution mention


<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: `skillkit read <skill-name>` or `npx skillkit read <skill-name>`
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>architecture-diagram-creator</name>
<description>Create comprehensive HTML architecture diagrams showing data flows, business objectives, features, technical architecture, and deployment. Use when users request system architecture, project documentation, high-level overviews, or technical specifications.</description>
<location>project</location>
</skill>

<skill>
<name>code-auditor</name>
<description>Performs comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability. Use when user wants to audit code quality, identify technical debt, find security issues, assess test coverage, or get a codebase health check.</description>
<location>project</location>
</skill>

<skill>
<name>code-execution</name>
<description>Execute Python code locally with marketplace API access for 90%+ token savings on bulk operations. Activates when user requests bulk operations (10+ files), complex multi-step workflows, iterative processing, or mentions efficiency/performance.</description>
<location>project</location>
</skill>

<skill>
<name>code-refactor</name>
<description>Perform bulk code refactoring operations like renaming variables/functions across files, replacing patterns, and updating API calls. Use when users request renaming identifiers, replacing deprecated code patterns, updating method calls, or making consistent changes across multiple locations.</description>
<location>project</location>
</skill>

<skill>
<name>code-transfer</name>
<description>Transfer code between files with line-based precision. Use when users request copying code from one location to another, moving functions or classes between files, extracting code blocks, or inserting code at specific line numbers.</description>
<location>project</location>
</skill>

<skill>
<name>codebase-documenter</name>
<description>Generates comprehensive documentation explaining how a codebase works, including architecture, key components, data flow, and development guidelines. Use when user wants to understand unfamiliar code, create onboarding docs, document architecture, or explain how the system works.</description>
<location>project</location>
</skill>

<skill>
<name>conversation-analyzer</name>
<description>Analyzes your Claude Code conversation history to identify patterns, common mistakes, and opportunities for workflow improvement. Use when user wants to understand usage patterns, optimize workflow, identify automation opportunities, or check if they&apos;re following best practices.</description>
<location>project</location>
</skill>

<skill>
<name>dashboard-creator</name>
<description>Create HTML dashboards with KPI metric cards, bar/pie/line charts, progress indicators, and data visualizations. Use when users request dashboards, metrics displays, KPI visualizations, data charts, or monitoring interfaces.</description>
<location>project</location>
</skill>

<skill>
<name>ensemble-solving</name>
<description>Generate multiple diverse solutions in parallel and select the best. Use for architecture decisions, code generation with multiple valid approaches, or creative tasks where exploring alternatives improves quality.</description>
<location>project</location>
</skill>

<skill>
<name>feature-planning</name>
<description>Break down feature requests into detailed, implementable plans with clear tasks. Use when user requests a new feature, enhancement, or complex change.</description>
<location>project</location>
</skill>

<skill>
<name>file-operations</name>
<description>Analyze files and get detailed metadata including size, line counts, modification times, and content statistics. Use when users request file information, statistics, or analysis without modifying files.</description>
<location>project</location>
</skill>

<skill>
<name>flowchart-creator</name>
<description>Create HTML flowcharts and process diagrams with decision trees, color-coded stages, arrows, and swimlanes. Use when users request flowcharts, process diagrams, workflow visualizations, or decision trees.</description>
<location>project</location>
</skill>

<skill>
<name>git-pushing</name>
<description>Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or asks to save and push their work. Also activates when user says &quot;push changes&quot;, &quot;commit and push&quot;, &quot;push this&quot;, &quot;push to github&quot;, or similar git workflow requests.</description>
<location>project</location>
</skill>

<skill>
<name>mastering-typescript</name>
<description>Master enterprise-grade TypeScript development with type-safe patterns, modern tooling, and framework integration. This skill provides comprehensive guidance for TypeScript 5.9+, covering type system fundamentals (generics, mapped types, conditional types, satisfies operator), enterprise patterns (error handling, validation with Zod), React integration for type-safe frontends, NestJS for scalable APIs, and LangChain.js for AI applications. Use when building type-safe applications, migrating JavaScript codebases, configuring modern toolchains (Vite 7, pnpm, ESLint, Vitest), implementing advanced type patterns, or comparing TypeScript with Java/Python approaches.
</description>
<location>project</location>
</skill>

<skill>
<name>nestjs-best-practices</name>
<description>NestJS best practices and architecture patterns for building production-ready applications. This skill should be used when writing, reviewing, or refactoring NestJS code to ensure proper patterns for modules, dependency injection, security, and performance.</description>
<location>project</location>
</skill>

<skill>
<name>playwright-skill</name>
<description>Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task. Use when user wants to test websites, automate browser interactions, validate web functionality, or perform any browser-based testing.</description>
<location>project</location>
</skill>

<skill>
<name>project-bootstrapper</name>
<description>Sets up new projects or improves existing projects with development best practices, tooling, documentation, and workflow automation. Use when user wants to start a new project, improve project structure, add development tooling, or establish professional workflows.</description>
<location>project</location>
</skill>

<skill>
<name>review-implementing</name>
<description>Process and implement code review feedback systematically. Use when user provides reviewer comments, PR feedback, code review notes, or asks to implement suggestions from reviews.</description>
<location>project</location>
</skill>

<skill>
<name>solid</name>
<description>Use this skill when writing code, implementing features, refactoring, planning architecture, designing systems, reviewing code, or debugging. This skill transforms junior-level code into senior-engineer quality software through SOLID principles, TDD, clean code practices, and professional software design.</description>
<location>project</location>
</skill>

<skill>
<name>supabase-postgres-best-practices</name>
<description>Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations.</description>
<location>project</location>
</skill>

<skill>
<name>technical-doc-creator</name>
<description>Create HTML technical documentation with code blocks, API workflows, system architecture diagrams, and syntax highlighting. Use when users request technical documentation, API docs, API references, code examples, or developer documentation.</description>
<location>project</location>
</skill>

<skill>
<name>test-fixing</name>
<description>Run tests and systematically fix all failing tests using smart error grouping. Use when user asks to fix failing tests, mentions test failures, runs test suite and failures occur, or requests to make tests pass.</description>
<location>project</location>
</skill>

<skill>
<name>timeline-creator</name>
<description>Create HTML timelines and project roadmaps with Gantt charts, milestones, phase groupings, and progress indicators. Use when users request timelines, roadmaps, Gantt charts, project schedules, or milestone visualizations.</description>
<location>project</location>
</skill>

<skill>
<name>vercel-composition-patterns</name>
<description>React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or designing reusable APIs. Triggers on tasks involving compound components, render props, context providers, or component architecture. Includes React 19 API changes.</description>
<location>project</location>
</skill>

<skill>
<name>vercel-react-best-practices</name>
<description>React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.</description>
<location>project</location>
</skill>

<skill>
<name>vercel-react-native-skills</name>
<description>React Native and Expo best practices for building performant mobile apps. Use when building React Native components, optimizing list performance, implementing animations, or working with native modules. Triggers on tasks involving React Native, Expo, mobile performance, or native platform APIs.</description>
<location>project</location>
</skill>

<skill>
<name>web-design-guidelines</name>
<description>Review UI code for Web Interface Guidelines compliance. Use when asked to &quot;review my UI&quot;, &quot;check accessibility&quot;, &quot;audit design&quot;, &quot;review UX&quot;, or &quot;check my site against best practices&quot;.</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>