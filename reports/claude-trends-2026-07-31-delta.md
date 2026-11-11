# Claude Trends — Delta Report 2026-07-31

*Baseline: 2026-06-22 (claude-trends-2026-06-22-delta.md). Analyzed 12 of 15 candidate videos uploaded between 2026-06-22 and 2026-07-31 (39-day window), cross-checked against Anthropic first-party sources (Claude Code weekly digests W26–W29, the Claude 5 context-engineering blog post, and the official Opus 5 prompting guide).*

---

## Executive Summary

- **Claude Opus 5 shipped 2026-07-24** and inverts the model hierarchy the baseline assumed: it beats Fable 5 on most benchmarks at **half the token price** ($5/$25 vs $10/$50 per MTok). Fable 5 is no longer the default choice for serious work.
- **Anthropic deleted >80% of Claude Code's own system prompt** with no measurable loss on coding evals, and shipped `/doctor` to help you do the same to your setup. Context bloat is now officially framed as a *performance regression*, not a safety net.
- **The official Opus 5 prompting guide retires advice this report series has been accumulating for three windows** — remove verification instructions, remove double-check lines, don't use subagents to verify your own work, and re-run an effort sweep because your inherited effort defaults are probably too high.
- **This creates the first genuine contradiction in the series**: practitioner content published the same week (maker/checker verification loops, "loop engineering") pushes *more* verification scaffolding while Anthropic pushes *less*. Flagged below — treat with care.
- **Sonnet 5 quietly became the default model** for Pro/Team Standard/Enterprise (1M context, promotional $2/$10 through Aug 31), and **plugins proved portable to non-Claude hosts** (same `plugin.json` runs on GitHub Copilot CLI).

---

## NEW Features / Releases

### Models

| Item | Detail | Source | Strength |
|---|---|---|---|
| **Claude Opus 5** (2026-07-24) | Tops Artificial Analysis Intelligence Index at 61; more than doubles Opus 4.8's Frontier-Bench score; ties GPT-5.6 Sol at 67 on the Coding Agent Index at extended-high effort. Knowledge cutoff **May 2026** (vs Jan 2026 for Fable 5 and Opus 4.8). 1M context as both default *and* max. | Web/official; `tHQ34j8_toI`, `2J3uX8iRNng`, `RCsBJz4W4bA` | **HIGH** |
| Opus 5 — five effort levels | `low` / `medium` / `high` / `xhigh` / `max`. Default is `high`. Thinking on by default; can only be disabled at `high` or below. | Official prompting guide | **HIGH** |
| Opus 5 — long-horizon autonomy | Boris Cherny: it "can go for days, weeks, months at a time, especially with auto mode… you don't even need scaffolding." | `qyPCVqFUyDo` (Claude Code creator) | **HIGH** |
| Opus 5 — prompt-injection resistance | Cherny: "the model does not seem to be prompt injectable anymore." | `qyPCVqFUyDo` | **MEDIUM** (claimed, not independently demonstrated) |
| Opus 5 — API additions | Mid-conversation tool changes (beta), automatic safety fallbacks to alternate models (beta), visual output generation. Fast mode: 2.5× faster at 2× base cost. | Anthropic release notes | **HIGH** |
| **Claude Sonnet 5** (W27, ~2026-06-30) | New default for Pro, Team Standard, Enterprise seats. Native 1M context, adaptive thinking on by default. Requires CLI v2.1.197+. | Claude Code W27 digest | **HIGH** |
| **Claude Voice** (iOS) | Real-time bidirectional audio agent on Opus 5, with integrations to existing apps/tools. Launched into the same week as OpenAI's Codex voice. | `Hv8YGUXZY1g` | **MEDIUM** |

### Claude Code CLI

| Item | Detail | Source | Strength |
|---|---|---|---|
| **80% system-prompt reduction** | Anthropic removed >80% of Claude Code's system prompt for Claude 5 models "with no measurable loss on our coding evaluations." Example: `"default to writing no comments. Never write multi-paragraph docstrings"` → `"Write code that reads like the surrounding code."` | Anthropic blog; `qyPCVqFUyDo`, `uD5OGiuNTK4` | **HIGH** |
| **`/doctor` is now a full setup checkup** (v2.1.205, W28) | No longer a read-only report — it diagnoses *and* fixes. Checks install health, finds unused skills/MCP servers/plugins vs their context cost, dedupes local `CLAUDE.md` against checked-in ones, proposes trimming `CLAUDE.md` content Claude could derive from the codebase, flags slow hooks. Reports first, confirms before changing. `/checkup` is an alias. | Claude Code W28 digest; `uD5OGiuNTK4` | **HIGH** |
| **In-app browser on Desktop** (W28) | Sandboxed built-in browser; Claude reads/clicks/interacts with external sites. Session persistence is configurable; safety classifiers review actions. | W28 digest | **HIGH** |
| **Subagents run in background by default** (v2.1.198, W27) | Claude keeps working while subagents run. Foreground only when the result is needed to continue. Pin with the `background` frontmatter field. | W27 digest | **HIGH** |
| **`/fork` → background session** (W29) | `/fork` now copies the conversation into a *new background session* with its own `claude agents` row. The old in-session forked subagent is renamed **`/subtask`**. | W29 digest | **HIGH** |
| **Artifacts call MCP connectors** (W29) | A published artifact can call MCP connectors on every view — live dashboards, not snapshots. Runs through the *viewing* account's connections, viewer approves first. Plus public share links and editor roles. | W29 digest | **HIGH** |
| **Artifacts GA on Pro/Max** (W27) | Previously Team/Enterprise only. | W27 digest | **HIGH** |
| **Runaway-loop caps** (W29) | Session-wide defaults of 200 WebSearch calls and 200 subagent spawns (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`). | W29 digest | **HIGH** |
| **MCP auto-background** (W29) | MCP tool calls over 2 minutes move to the background automatically (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`). | W29 digest | **HIGH** |
| **`claude mcp login` / `logout`** (v2.1.186, W26) | Run an MCP server's OAuth flow from the shell instead of the interactive `/mcp` menu. | W26 digest | **HIGH** |
| **Shell mode responds to output** (v2.1.186, W26) | `! npm test` now gets an explanation without a second prompt. Costs the same as a normal prompt. Disable via `respondToBashCommands: false`. | W26 digest | **HIGH** |
| **Claude in Chrome GA** (W27) | Out of preview for all direct Anthropic plans. | W27 digest | **HIGH** |
| **Claude Desktop on Linux (beta)** (W27) | Ubuntu 22.04+ / Debian 12+, x86_64 and arm64, via Anthropic's apt repo. Full Chat + Cowork + Code. | W27 digest | **HIGH** |
| **Screen reader mode** (W29) | `claude --ax-screen-reader` / `CLAUDE_AX_SCREEN_READER` / `axScreenReader` — plain linear text for VoiceOver and NVDA. | W29 digest | **HIGH** |
| Smaller wins | `/rewind` can resume from before `/clear` (W26); `/radio` (Claude FM lo-fi) (W27); new `/dataviz` skill (W27); Explore agent now inherits the session model instead of running on Haiku (W27); stacked skill invocations load up to 5 leading skills (W27); "default" permission mode renamed **Manual** (W27). | W26–W29 digests | **HIGH** |

### Plugins / Skills

| Item | Detail | Source | Strength |
|---|---|---|---|
| **`claude-code-setup` official plugin** | `claude plugin install claude-code-setup@claude-plugins-official`. Analyzes your project and recommends fitting automations (hooks, skills, subagents, MCP servers). **Read-only — modifies nothing.** | `OLW7FcsGMrI` | **MEDIUM** |
| **Anthropic maintains two marketplaces** | Official + community, with a naming distinction most tutorials get wrong. | `FI2GwpI92IM` (description) | **LOW** (no transcript) |
| **Plugin trust boundary is explicit** | Anthropic's own docs state a plugin runs arbitrary code with your permissions and Anthropic cannot verify every plugin's behavior. Installing a plugin = trusting one more author. | `FI2GwpI92IM` (description) | **MEDIUM** |

---

## NEW Workflow Patterns

**1. Context minimalism replaces context maximalism.** The highest-leverage move is now *deletion*. Anthropic's own six reframings: rules → judgment; examples → interface design; upfront disclosure → progressive loading; repetition → clarity; manual memory → auto-memory; simple specs → rich references (code, HTML mockups, test suites beat markdown prose). → Anthropic blog, `uD5OGiuNTK4` — **HIGH**.

**2. Effort as the primary cost lever, not model choice.** Official guidance: start at `high`, then run an effort sweep on your own evals; use `low`/`medium` liberally wherever quality holds; reserve `xhigh` for demanding agentic work. Explicitly: *if you carried effort defaults over from a prior model, re-run the sweep.* Also — thinking enabled at `low` effort beats thinking disabled at similar cost. → Official prompting guide — **HIGH**.

**3. "Loop engineering" crystallized as a named discipline** with six components: automations, worktrees, skills, connectors, subagents (maker + checker), and memory. Practitioner framing: the hard part is defining what "done" looks like, and a `/goal` prompt needs three parts — a clear end state, a check, and a guardrail (e.g. "stop after 30 turns"). → `C673pP-XQRM`, `vZZRx4g6tcs` — **HIGH**.

**4. Event-based triggers over cron, for token economy.** Cron loops burn tokens on no-ops; event/webhook triggers and cheap local pre-checks (plain scripts, zero tokens) gate the expensive AI step. Canonical example: an agency monitoring 50+ WordPress sites runs a zero-token script on advisory arrival, and only then invokes the model on affected sites. → `vZZRx4g6tcs` — **MEDIUM**.

**5. Plugins are cross-host artifacts.** The same `plugin.json` + skills + agents/hooks bundle runs on Claude Code *and* GitHub Copilot CLI (which can drive non-Anthropic models). Recommendation: validate against both hosts before release; distribute via `marketplace.json`. → `qDvsGI4q8-M` — **HIGH**.

**6. Cowork's "central hub" setup.** One folder holding `CLAUDE.md` (standing instructions) plus `memory.md` (auto-updating learned preferences), both plain text and human-editable, auto-loaded on every task start. Skills invoked on demand from there. → `szWBwfPX30M` — **HIGH**.

**7. Scope control is now a prompting concern.** Opus 5 expands scope and delegates more readily than prior models. Official mitigations: an explicit scope paragraph ("deliver what was asked, at the scope intended"), and explicit delegation criteria or hard caps on subagent spawn counts. → Official prompting guide — **HIGH**.

---

## NEW Tools / MCPs / Integrations

| Tool / MCP | Source | What it does | Nature | Strength |
|---|---|---|---|---|
| **`/doctor` (`/checkup`)** | W28 digest | Audits and fixes context bloat: unused skills/MCP/plugins, duplicated CLAUDE.md, slow hooks | Claude-native | **HIGH** |
| **`claude-code-setup` plugin** | `OLW7FcsGMrI` | Official read-only advisor recommending automations per project | Claude-native (official) | **MEDIUM** |
| **Loop Library** | `vZZRx4g6tcs` | Community skill (Matthew Berman) that discovers repeatable work patterns and audits loop exit conditions | Third-party | **MEDIUM** |
| **GitHub Copilot CLI as plugin host** | `qDvsGI4q8-M` | Runs Claude-format plugins; can back them with non-Anthropic models | Adjacent | **HIGH** |
| **Snyk MCP for Claude Code** | search metadata | Pre-commit vulnerability blocking as an MCP layer | Third-party | **LOW** (not analyzed) |
| **`awesome-claude-code`** (45K★) | `Oz4IMQ5AGIA` | Community index of skills, hooks, slash commands, orchestrators, plugins | Third-party | **MEDIUM** |
| **OpenWork** | `hUmXzW3ZSlY` | Open-source Cowork alternative on `opencode`; MIT core, Linux support, shared skills across Claude Code / Codex / Cursor | Adjacent/competitive | **LOW** |

---

## Notable Applications

- **Windows 11 replica in the browser** — Opus 5 generated a working Windows 11 UI with functional apps (Office, Store, Explorer, Discord, Slack) in a single Claude Code session. → `RCsBJz4W4bA` — **HIGH**.
- **Support-ticket maker/checker loop** — a maker routine processes Intercom tickets at 8am; an independent checker routine verifies ~2h later and reopens anything that slipped. Wired to a tool with no native connector via API key + custom environment. → `C673pP-XQRM` — **HIGH**.
- **Cowork "OS" for a teacher** — `CLAUDE.md` holds grading rules and an exam-analysis skill, `memory.md` accumulates preferences; the single prompt "analyze new exams" produces a correctly formatted HTML report with no re-explanation. → `szWBwfPX30M` — **HIGH**.
- **Cross-platform plugin at scale** — a 31-skill, 4-subagent plugin validated on both Claude Code and GitHub Copilot CLI from one manifest. → `qDvsGI4q8-M` — **HIGH**.
- **ARC-AGI-3 at 30%** — a large jump over prior frontier results, cited by Cherny as the headline reasoning gain. → `qyPCVqFUyDo` — **MEDIUM** (single source).

---

## Pricing / Cost shifts

- **Opus 5: $5 / $25 per MTok** — identical to Opus 4.8, and **half** Fable 5's $10 / $50. This is the single biggest cost event of the window. Available on Claude API, claude.ai, Claude Code, Claude Cowork, Bedrock, Google Cloud, and Microsoft Foundry from day one. → Official / multiple — **HIGH**.
- **Sonnet 5 promotional API pricing: $2 / $10 per MTok through 2026-08-31.** → W27 digest — **HIGH**.
- **Opus 5 fast mode: 2.5× faster at 2× base cost.** → Anthropic release notes — **HIGH**.
- **Effort level is now the recommended cost dial** — `low`/`medium` deliver "strong quality at a fraction of the tokens and latency." Inherited effort defaults are a live cost bug. → Official prompting guide — **HIGH**.
- **Removing verification scaffolding cuts cost with no quality loss** on Opus 5 — over-verification is now a named waste category. → Official prompting guide — **HIGH**.
- Claude Cowork remains included on every paid plan (from Pro at $20/mo); no separate license. → Web — **MEDIUM**.

---

## Consensus shifts (vs 2026-06-22)

1. **Fable 5 is no longer the default frontier choice** (**REVERSED**). The baseline treated Fable 5 as the top of the ladder. Opus 5 matches or beats it on most axes at half the price. New default: Opus 5 for most work; Fable 5 only where it demonstrably wins.
2. **More context → worse, not better** (**REVERSED**). Baseline windows accumulated advice about richer CLAUDE.md, more skills, more scaffolding. Anthropic's own 80% cut plus `/doctor` reframe the pile as a liability.
3. **Effort tuning replaces model shopping as the cost lever** (**NEW**). The baseline's cost discussion was about adapter choice (skill+CLI vs MCP) and workflow fan-out. Now it's primarily about effort levels.
4. **Plugins escape the Claude ecosystem** (**NEW**). Baseline framed plugins as Claude-native versioned bundles; they now run on GitHub Copilot CLI from the same manifest. Skills-as-open-standard (06-22) has extended to plugins-as-open-standard.
5. **Cowork is a distinct product, not a Claude Code surface** (**CLARIFIED**). Baseline mentioned it only as a `.skill` packaging target. It has its own workflow model (auto-loaded standing instructions + persistent memory, no terminal), reached mobile and web on 2026-07-07, and now runs on Linux desktop.
6. **Orchestration-over-autonomy is under pressure** (**WEAKENED**). Held since 2026-05-27. Cherny's claim that Opus 5 + auto mode runs for days without scaffolding, plus official guidance to cap delegation and drop verification subagents, both cut against elaborate harnesses. Not reversed — but no longer unopposed.
7. **Loop engineering as named discipline** (**TERMINOLOGY**). The baseline's "Dynamic Workflows / goal loops / Agent Teams" ladder is being absorbed into a broader practitioner vocabulary ("loop engineering", six concepts). Same substance, new label — expect the label to stick.

---

## Contradictions vs baseline

**Three, and one is live and unresolved.**

**1. ⚠️ LIVE CONFLICT — verification subagents.** Anthropic's official Opus 5 prompting guide says, verbatim: *"Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work,"* and *"If your prompt contains explicit verification instructions… remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality."*

Meanwhile, practitioner content published the *same week* (`C673pP-XQRM`, 2026-07-24) presents the **maker/checker loop** — a second agent that independently re-verifies the first agent's work — as the flagship production pattern.

These are not trivially reconcilable. The defensible reading: **maker/checker across separate scheduled runs with independent context (a checker routine reviewing yesterday's ticket closures) is still sound**, because the checker is auditing an external artifact, not the model second-guessing itself inside one turn. **In-turn "spawn a subagent to verify my own output" scaffolding is what Anthropic is telling you to delete.** Prior reports in this series did not draw that line; draw it now.

**2. Retire "Fable 5 for all serious work."** The 06-22 report logged Fable 5 as the new Mythos-class frontier release. Opus 5 supersedes it on price/performance for most tasks. Weak-evidence Fable 5 benchmark claims from 06-22 (Japanese, description-only) should be considered stale rather than wrong.

**3. Retire "exhaustive CLAUDE.md" and "detailed examples for every tool."** Both explicitly listed as retired guidance by Anthropic. Also retired: repeating instructions across context layers, and preferring simple markdown specs over rich references. Note also **auto-memory** — manual CLAUDE.md upkeep for memory purposes is no longer necessary.

---

## Sources

| Video ID | Title | Channel | Upload date | Strength |
|---|---|---|---|---|
| qyPCVqFUyDo | Boris Cherny: We Cut 80% of Claude Code's Prompt | Y Combinator | 2026-07-27 | **strong** (first-party, creator) |
| uD5OGiuNTK4 | Your Claude Code Context Is Bloated. Here's the Fix. | Daniel Zambrini | 2026-07-31 | **strong** (sourced to Anthropic blog) |
| C673pP-XQRM | Loop Engineering for AI Agents (Claude /goal & Routines) | Sabrina Ramonov | 2026-07-24 | **strong** (live build) |
| vZZRx4g6tcs | [LIVE] WTF Is Loop Engineering? | Ship Sh!t Show | 2026-06-24 | **strong** (49 min, practitioner panel) |
| szWBwfPX30M | Claude Cowork Finally Clicked When I Learned This | Paul J Lipsky | 2026-07-12 | **strong** (Anthropic-sponsored walkthrough) |
| qDvsGI4q8-M | Inside A Plugin — Agents, Skills, & Workflows | Dewain Robinson | 2026-07-24 | **strong** (31 min, real plugin) |
| RCsBJz4W4bA | Claude Opus 5 is a freak | AI Search | 2026-07-27 | **strong** (demo-heavy) |
| tHQ34j8_toI | What did Anthropic do?! (Opus 5) | Matthew Berman | 2026-07-24 | **strong** (benchmarks) |
| 2J3uX8iRNng | I Tested Opus 5 vs. Fable 5 | Nate Herk | 2026-07-24 | **strong** (instrumented) |
| Z8CtXdQExek | Anthropic Just Revealed How to Prompt Opus 5 | Paul J Lipsky | 2026-07-27 | **strong** (reads official guide) |
| Hv8YGUXZY1g | Opus 5 Is Here… But NEW Claude Voice Is Even Bigger | Riley Brown | 2026-07-25 | **medium** |
| XNbc2HhL7J4 | Claude Cowork: coming to mobile and web | Claude (official) | 2026-07-07 | **weak** (95-char promo transcript) |
| SZgsphLx2Hc | Weekly AI roundup (Claude Code / Opus 5 / Cowork / Fable 5) | AI大学 | 2026-07-26 | **weak** (JP, no transcript) |
| aw5aBxuZJkw | Hooks, Skills oder Agents? Wann du was nimmst | AppX Patterns | 2026-07-28 | **weak** (DE, no transcript) |
| FI2GwpI92IM | Claude Code Plugins 生態系完全教學 (trust boundary) | Herbert AI 開發筆記 | 2026-07-25 | **weak** (CN, no transcript; description only) |

**First-party sources cross-checked** (used to arbitrate and to fill gaps the video corpus missed):
- [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- Claude Code What's New — [W26](https://code.claude.com/docs/en/whats-new/2026-w26), [W27](https://code.claude.com/docs/en/whats-new/2026-w27), [W28](https://code.claude.com/docs/en/whats-new/2026-w28), [W29](https://code.claude.com/docs/en/whats-new/2026-w29)

---

## Methodology

- **Baseline auto-detected** from `reports/claude-trends-2026-06-22-delta.md`. Window: 2026-06-22 → 2026-07-31 (39 days).
- **Searches**: 5 seed YouTube MCP `search_videos` queries (Claude Code workflow / Claude Opus agents / skills-plugins-hooks / MCP / routines-subagents) at `publishedAfter=2026-06-22`, `order=date`, `maxResults=15`, plus 2 targeted follow-ups (`Claude Cowork`, `Claude Opus 5 review coding`, `order=viewCount`) once Opus 5 and Cowork surfaced as the window's dominant themes.
- **Filters applied**: dropped everything under 5 minutes (this window was unusually short-form-heavy — 8 otherwise-relevant hits were Shorts, including the official `claude-code-setup` plugin announcement and the official Cowork mobile/web clip, both retained as description-only evidence); dropped competitor-only comparisons (GLM 5.2, Grok 4.5, Kimi K3) unless they benchmarked Claude directly; dropped obvious AI-slop reuploads and listicle channels.
- **Transcript download + analysis**: dispatched to two subagents (split by theme) so transcripts never entered the main context. **12/15 succeeded.** Failures: 1 Japanese, 1 German, 1 Chinese — all IP-blocked or caption-restricted, all marked weak and used at description level only.
- **First-party arbitration**: because the video corpus disagreed on the Opus 5 release date (24th vs 27th) and could not settle the verification-scaffolding question, Anthropic's blog, prompting guide, and the four weekly Claude Code digests were fetched directly. **Release date corrected to 2026-07-24.** Several CLI features in this report (Sonnet 5 default, `/fork`→`/subtask`, Artifacts+MCP, session caps, screen reader mode, Linux desktop) appear in *no* analyzed video and were recovered only from the official digests — a coverage gap worth noting for future runs.
- **Deviation from skill spec**: used two analysis subagents rather than one, to avoid overloading a single agent's context with 12 transcripts. Main-context protection — the reason for the rule — was preserved.
