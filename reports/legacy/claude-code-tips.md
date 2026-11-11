# Claude Code — Actionable Tips & Best Practices

*Extracted from 16 top YouTube tutorials (analyzed 2026-03-14)*

---

## Getting Started & Setup

- [ ] Install Claude Code via package manager (not desktop app) for full feature access
  - **Rationale:** Terminal version has more power than desktop client; enables scripting, full tool integration, background tasks
  - **How:** Mac/Linux: `curl https://installer.src.claude.com/claude | bash`; Windows: Use `irm` command in PowerShell

- [ ] Create a Git repository immediately and configure GitHub auth
  - **Rationale:** Enables Claude to auto-commit work, prevents code loss, creates checkpoints for reverting mistakes
  - **How:** Run `gh login` to authenticate GitHub locally; Claude will auto-save code via Git thereafter

- [ ] Always use a code editor (VS Code, Cursor, Windsurf) alongside Claude CLI, not terminal alone
  - **Rationale:** See files change in real-time, track progress, understand file structure, debug faster
  - **How:** Open editor → open folder → open integrated terminal (Ctrl+`) → run `claude` there

- [ ] Create a CLAUDE.md file in project root on first session using `/init`
  - **Rationale:** Provides persistent memory across sessions; Claude reads it automatically to understand project rules, context, conventions
  - **How:** Type `/init` in Claude, review generated content, edit to add team conventions, commit to Git

- [ ] Install Claude Desktop app as separate tool for quick chat (not code generation)
  - **Rationale:** Quick Q&A and planning without spinning up CLI; lighter weight
  - **How:** Download from Claude.com, use for brainstorming; use CLI for actual building

- [ ] Trust the current folder once (first run), then you never need to do it again
  - **Rationale:** Security gate to prevent accidental CLI execution in unintended directories
  - **How:** First `claude` run asks "Trust folder?" → press Y → never prompted again in that directory

---

## Workflow Optimization

- [ ] Always start in **plan mode** for non-trivial tasks (3+ steps or decisions)
  - **Rationale:** Gives visibility on what Claude will do before it acts; lets you edit the plan, ask clarifications, catch mistakes early
  - **How:** `Shift+Tab` to cycle modes; use plan mode to explore, understand, modify; don't blindly accept plans

- [ ] Edit the plan Claude generates—don't just accept it
  - **Rationale:** You catch issues before tokens burn; iterating on a plan costs less than redoing broken code
  - **How:** Read the plan, spot problems, say "I don't like X, change it to Y" and get a revised plan before approval

- [ ] Use **coding mode** (auto-accept edits) only after plan is approved and trivial changes
  - **Rationale:** Reduces friction on proven workflows; use ask mode for experiments
  - **How:** Plan mode → get approval → switch to coding mode for implementation sprint

- [ ] Set context goal upfront: tell Claude what model to use, token budget, and success criteria
  - **Rationale:** Prevents token waste; Claude makes cheaper choices (Haiku for lookups, Sonnet for focused work, Opus for architecture)
  - **How:** "Using Haiku for speed, I want X done in <500 tokens. Success = passing these tests."

- [ ] Break large prompts into sequences of small, clear requests instead of one big one
  - **Rationale:** Small requests = better focus, faster iteration, easier to fix when wrong
  - **How:** Don't: "Build a full auth system with email, 2FA, recovery codes." Do: "Add email signup" → "Add 2FA" → "Add recovery codes"

- [ ] Use **alt+Enter** (option+Enter on Mac) to write multi-line prompts without submitting
  - **Rationale:** Compose complex thoughts before sending; reduces garbled requests
  - **How:** Alt+Enter moves to next line; Escape twice clears draft; Enter submits

- [ ] Keep context window < 50% usage whenever possible
  - **Rationale:** Model performs worse when context is >50% full; responses get shorter and lower quality
  - **How:** Run `/context` to check; use subagents to offload work when you hit 40%; clear context with `/clear` (saves as checkpoint)

- [ ] Use plan mode to ask Claude clarifying questions if your idea is vague
  - **Rationale:** Q&A in plan mode doesn't burn tokens on bad code; saves iteration cycles
  - **How:** Plan mode + vague prompt = Claude asks clarifications before building

- [ ] Always review and test code yourself before shipping
  - **Rationale:** "AI wrote it" is not an excuse; you own the code and its security/performance
  - **How:** Read diffs, run tests locally, check security manually (especially auth, payment, DB queries)

- [ ] Stay in control—don't use loops/ROLF workflows for critical builds
  - **Rationale:** Running Claude in a loop on a document removes human oversight; things go wrong silently
  - **How:** Manual approach: plan, review, approve, execute each step; better results with less waste

---

## Subagents

- [ ] Create subagents for **tasks**, not roles (e.g., "code reviewer" not "junior developer")
  - **Rationale:** Claude struggles with role-playing; excels at specific tasks with clear success criteria
  - **How:** Bad: "Act as a frontend dev." Good: "Review this UI for accessibility issues and suggest 3 fixes."

- [ ] Dispatch subagents for parallel work to keep main context window clean
  - **Rationale:** Subagents get their own context; main window stays focused; combine results at end
  - **How:** Main agent: "Launch 5 research agents to find X in these 5 directories; summarize findings"

- [ ] Use Haiku for research/exploration subagents (fast, cheap)
  - **Rationale:** Haiku is 90% cheaper than Opus; perfect for "find all X in codebase" tasks
  - **How:** Create subagent, select Haiku model, use for grep-like searches and data gathering

- [ ] Use Opus for code-generation subagents (complex logic, refactors)
  - **Rationale:** Opus handles intricate refactors better; pays for itself on complex tasks
  - **How:** Create subagent with Opus for migrations, architecture decisions, multi-file changes

- [ ] Use Sonnet for medium-weight subagents (debugging, documentation, small features)
  - **Rationale:** Sweet spot: cheaper than Opus, smarter than Haiku; good for focused work
  - **How:** Default subagent model for general-purpose specialist agents

- [ ] Subagents work best for isolated, specific work (testing, code review, research)
  - **Rationale:** Subagents can't coordinate complex cross-domain tasks; mainagent should orchestrate
  - **How:** Use subagents for "run tests", "review this PR", "find all SQL queries"; main agent decides what to do with results

- [ ] Create subagent with **read-only tools** for code audits (prevents accidental changes)
  - **Rationale:** Safety gate; auditor can't modify code, only report issues
  - **How:** /agents → create → uncheck "execute" tool → only allow "read files"

- [ ] Return subagent results to main conversation explicitly (don't auto-merge)
  - **Rationale:** Visibility; you see what each subagent found before combining
  - **How:** Subagent returns summary → main agent shows you → ask if you want to proceed

- [ ] Limit subagent count to 5-10 unless task is embarrassingly parallel
  - **Rationale:** Too many = cost spike, coordination overhead, noise
  - **How:** Start with 2-3, increase only if results are incomplete

- [ ] Subagents inherit from project `.claude/agents/` directory
  - **Rationale:** Reusable specs; commit them to Git so team has consistent agents
  - **How:** Define once in `.claude/agents/code-reviewer.md`; use in all sessions

---

## Skills & Custom Commands

- [ ] Create skills for workflows you repeat 3+ times (not one-off tasks)
  - **Rationale:** Skills are only loaded when triggered; saves context tokens vs. hardcoding in CLAUDE.md
  - **How:** Identify "I keep doing X", write skill.md, test it, commit to `.claude/skills/`

- [ ] Skills are YAML + Markdown; name becomes `/slash command`
  - **Rationale:** Slash commands are faster to invoke than describing workflow each time
  - **How:** skill.md → YAML header with name: "code-review" → becomes `/code-review` command

- [ ] Add `description` field to let Claude auto-trigger skill when relevant
  - **Rationale:** Reduces need to manually invoke; Claude uses skill when it matches description
  - **How:** description: "Use when reviewing code for quality, security, style issues"

- [ ] Set `disable_model_invocation: true` for dangerous skills (deploy, delete, send)
  - **Rationale:** Only you invoke manually; prevents Claude from accidentally running it
  - **How:** Add to YAML; now skill is manual-only, Claude can't auto-trigger

- [ ] Use `context_fork: true` in skill YAML to run skill in isolated subagent
  - **Rationale:** Skill runs in separate context; results return to main conversation; main window stays clean
  - **How:** Long-running skills get isolated; results summarized and returned

- [ ] Build library of 3-5 core skills for your common tasks
  - **Rationale:** Multiplier effect; reusable foundation for all projects
  - **How:** Start: frontend-design, stripe-setup, code-review, docs-writer, test-generator

- [ ] Test skills in plan mode first; verify they trigger correctly
  - **Rationale:** Catch typos, wrong descriptions, missing tools before they fail in production
  - **How:** Ask Claude to use skill; check if it triggers; edit skill.md and retry if needed

- [ ] Keep skill.md under 500 lines; move reference docs to separate files
  - **Rationale:** Huge skills slow down invocation and context loading
  - **How:** skill.md = instructions; references.md = detailed guides; skill imports references

- [ ] Use commands directory for quick bash commands (simpler than skills)
  - **Rationale:** One-line scripts for common tasks; faster to create than full skill
  - **How:** `.claude/commands/lint.md` → `/lint` runs TypeScript linter, fixes errors automatically

- [ ] Skills are markdown files committed to Git; share them with team via Git
  - **Rationale:** Team consistency; easy to update across projects; version control
  - **How:** Commit `.claude/skills/` → pull in other projects → everyone uses same workflow

- [ ] Use skill creator skill to build, test, benchmark your skills automatically
  - **Rationale:** Validates skills work; shows which skills Claude actually uses; tracks improvements
  - **How:** `/skill-creator` → design your skill → run evals → get pass rate, token count, success metrics

---

## Hooks

- [ ] Use pre-tool hooks to validate commands before Claude runs them
  - **Rationale:** Catch dangerous operations (rm -rf, delete prod DB, etc.) before execution
  - **How:** Hook on bash tool → check for dangerous patterns → block or warn

- [ ] Use post-tool hooks to auto-format code after every file write
  - **Rationale:** Keep codebase formatted without manual intervention
  - **How:** Post-tool-use on "edit file" → run prettier/ruff automatically

- [ ] Add hooks to log all tool invocations for auditing
  - **Rationale:** Track what Claude did, when, why; helps debug issues, comply with audit needs
  - **How:** Pre-tool hook → write tool name + input to audit.log file

- [ ] Use notification hooks to alert on task completion (Slack, OS notification)
  - **Rationale:** Know when long-running tasks finish without polling
  - **How:** Stop hook → send Slack message "Claude finished your deployment" + result

- [ ] Use user-input hooks to filter/validate prompts before Claude sees them
  - **Rationale:** Enforce naming conventions, block certain keywords, auto-format requests
  - **How:** User-prompt hook → check if PR title follows "type: description" → reject or fix if not

- [ ] Add session-start hook to load team rules/context automatically
  - **Rationale:** No need to re-paste conventions at start of each session
  - **How:** Session-start hook → cat team-rules.md → Claude reads rules automatically

- [ ] Hooks can run bash, Python, or HTTP requests (invoke external services)
  - **Rationale:** Integrate with CI/CD, databases, APIs, webhooks
  - **How:** Post-tool hook → curl to localhost:8000/hooks/tool-use → external service validates/logs

- [ ] Store hooks in `.claude/settings.local.json` (project-level) or global config (all projects)
  - **Rationale:** Local = team-specific rules; global = personal automation
  - **How:** Project hook: `.claude/settings.local.json`; global hook: `~/.claude/config.json`

- [ ] Test hooks locally before deploying (run them manually first)
  - **Rationale:** Broken hooks block Claude; test syntax and logic standalone
  - **How:** Run hook bash/Python directly → confirm output → add to Claude → test with small prompt

---

## MCP Servers

- [ ] Add Context7 MCP for automatic doc lookups
  - **Rationale:** Claude uses up-to-date docs instead of training data (which lags 6+ months); reduces hallucinations
  - **How:** `claude mcp add -dt http context7 https://mcp.context7.com` → add memory "use context7 for docs"

- [ ] Add Playwright MCP for browser automation and frontend testing
  - **Rationale:** Claude can open browser, take screenshots, inspect DOM, test UI interactively
  - **How:** `claude mcp add playwright` → ask Claude "test this login form" → it opens browser, fills form, verifies

- [ ] Add GitHub MCP for querying repos, creating PRs, reading issues
  - **Rationale:** Claude has direct GitHub access; no need to copy-paste issue text
  - **How:** `claude mcp add github` → "find all open bugs labeled critical" → returns live GitHub data

- [ ] Use **Context Mode MCP** to compress large file outputs
  - **Rationale:** Reduces output size 99% (56KB → 299 bytes); extends session life from 30 min to 3 hours
  - **How:** `claude mcp add context-mode` → ask to "index this 5MB CSV and find patterns" → Claude keeps file in sandbox, not context

- [ ] Install MCP at **project scope** to share with team via Git
  - **Rationale:** Team members get same MCP config; consistent setup
  - **How:** `claude mcp add context7 ... --scope project` → check `.mcp.json` → commit to Git

- [ ] Be cautious with Playwright MCP—it burns tokens fast
  - **Rationale:** Screenshots + DOM inspection = 50KB+ per page; use sparingly
  - **How:** Use Playwright only for critical UI tests; prefer API testing where possible

- [ ] Don't add 10+ MCPs; start with 2-3 core ones
  - **Rationale:** Too many MCPs slow down tool discovery, increase token cost
  - **How:** Start: Context7 + Playwright; add others only if you use them weekly

- [ ] MCPs on Windows need `cmd /c` prefix for npm packages (workaround for WSL issues)
  - **Rationale:** Windows command line handling differs; npx sometimes fails without prefix
  - **How:** `claude mcp add myserver --scope project ... -- cmd /c npx myserver`

---

## Cost Optimization

- [ ] Use model cascading: Haiku for research, Sonnet for code, Opus for architecture
  - **Rationale:** 10-100x cost difference; pick right model for task
  - **How:** Search codebase? Haiku. Fix bug? Sonnet. Design new system? Opus.

- [ ] Clear context when approaching 50% window fill
  - **Rationale:** Model quality drops at >50%; clearing saves tokens + improves output
  - **How:** `/context` → see usage → `/clear` when >40% → continues work with summary snapshot

- [ ] Leverage Context Mode MCP to compress log files, CSVs, API responses
  - **Rationale:** 99% compression; dramatically extends session length
  - **How:** "Use context mode to index access.log" → Claude keeps it in sandbox, searches efficiently

- [ ] Run expensive operations in parallel via subagents (5x faster, 20% cost savings)
  - **Rationale:** 5 Haiku agents in parallel < 1 Opus agent sequentially (cost & time)
  - **How:** "Launch 5 agents to search for X in 5 directories" → all run simultaneously

- [ ] Use `/simplify` skill before every commit (runs 3 agents in parallel, auto-fixes)
  - **Rationale:** Catches inefficiencies, quality issues, lint errors once; prevents rework
  - **How:** Make changes → `/simplify` → agents check code reuse, quality, performance → fixes applied

- [ ] Batch similar requests into one prompt instead of 10 separate prompts
  - **Rationale:** Amortizes setup overhead; less total tokens
  - **How:** Don't: "Fix bug A" → wait → "Fix bug B". Do: "Fix bugs A, B, C in one session"

- [ ] Ask Claude to explain its token usage and suggest optimizations
  - **Rationale:** Claude understands context bloat; can suggest techniques you're missing
  - **How:** "We used 50K tokens. How could we do this in <30K?" → gets specific suggestions

- [ ] Use `/batch` skill for large migrations (parallelizes across isolated agents)
  - **Rationale:** Migrate entire codebase (Jest → Vitest, CommonJS → ES modules) in fraction of time
  - **How:** `/batch migrate jest vitest` → Claude splits work, agents run in parallel, opens PRs

---

## Common Mistakes & Anti-Patterns

- [ ] Don't use loops (ROLF workflow) for critical builds
  - **Rationale:** You lose visibility; Claude makes decisions in isolation; hard to debug
  - **How:** Use manual workflow: you read plan, approve, execute, review—takes longer but safer

- [ ] Don't blindly accept plans without reading them
  - **Rationale:** Plans often have subtly wrong logic; catching errors before code saves hours
  - **How:** Read every plan, edit if needed, ask clarifications before approval

- [ ] Don't give Claude too many MCP tools at once
  - **Rationale:** Too many tools = poor tool selection; Claude gets confused
  - **How:** Start with 2-3; add more only if used regularly

- [ ] Don't assign skills that are too broad
  - **Rationale:** Broad skills trigger in wrong contexts; narrow descriptions work better
  - **How:** Bad: "Help with code." Good: "Generate unit tests using Jest for TypeScript functions."

- [ ] Don't store secrets (API keys, credentials) in CLAUDE.md or skills
  - **Rationale:** Gets committed to Git; leaks credentials
  - **How:** Use environment variables; reference them in CLAUDE.md as `${API_KEY}` not literal values

- [ ] Don't let AI write complex security code (auth, encryption, payment) without review
  - **Rationale:** Subtle bugs in security code are hard to spot; you own the risk
  - **How:** Review every auth/payment/crypto line manually; don't trust AI output

- [ ] Don't run `/batch` on tasks with file conflicts
  - **Rationale:** Subagents can't coordinate file edits; conflicts pile up
  - **How:** Use `/batch` only for migrations where each agent touches different files

- [ ] Don't create subagents without specific task descriptions
  - **Rationale:** Vague agents make vague decisions; narrow descriptions = better focus
  - **How:** Bad: "Help debug." Good: "Find why auth token is missing in POST /login responses."

- [ ] Don't ignore context window health
  - **Rationale:** > 60% context = hallucinations, shorter responses, worse code
  - **How:** Check `/context` every 10 prompts; clear when >50%

- [ ] Don't use planning mode for trivial tasks
  - **Rationale:** Overkill; wastes tokens on simple changes
  - **How:** Plan mode for: architecture decisions, large refactors, unclear goals. Skip for: typo fixes, small edits.

- [ ] Don't let code review be 100% automated
  - **Rationale:** Human review catches issues automation misses (edge cases, performance, design)
  - **How:** Use Claude to do initial pass; you do final review before merge

- [ ] Don't assume Claude remembers previous sessions
  - **Rationale:** Each session starts fresh; CLAUDE.md provides only some context
  - **How:** Write detailed CLAUDE.md; in new session, ask Claude "What was I working on?" and paste context

---

## Quick Reference: When to Use What

| Task | Mode | Model | Tool |
|------|------|-------|------|
| Planning architecture | Plan | Opus | Main agent |
| Searching codebase | Coding | Haiku | Subagent (5x parallel) |
| Fixing bug | Plan → Code | Sonnet | Main agent |
| Code review | Code | Haiku | /review skill |
| Writing frontend | Code | Opus | /frontend-design skill |
| Testing | Code | Sonnet | Subagent |
| Setting up Stripe | Code | Sonnet | /stripe-setup skill |
| Migrating framework | Plan → Coding | Opus | `/batch` skill |
| Finding docs | N/A | Haiku | Context7 MCP |
| Testing UI | N/A | Sonnet | Playwright MCP |

---

## Setup Checklist

- [ ] Install Claude via package manager (not desktop)
- [ ] Create GitHub account and auth locally (`gh login`)
- [ ] Open code editor (Cursor/VS Code) with integrated terminal
- [ ] Run `/init` to create CLAUDE.md
- [ ] Create `.claude/skills/` directory for custom skills
- [ ] Create `.claude/agents/` directory if using subagents
- [ ] Commit `.claude/` to Git
- [ ] Add Context7 MCP (`claude mcp add context7`)
- [ ] Set up 2-3 foundational skills (frontend-design, code-review, test-writer)
- [ ] Test each skill in plan mode before using in production
- [ ] Review `/help` and `/commands` to discover built-ins
- [ ] Read Claude docs on hooks if you need automation

---

*Last updated: 2026-03-14*
*Video sources: Sabrina Ramonov, Nick Saraev, Net Ninja tutorials, Boris Churney, Maximilian Schwarzmüller, and others*
