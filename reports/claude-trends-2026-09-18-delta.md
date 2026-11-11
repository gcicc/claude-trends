# Claude Trends — Delta Report 2026-09-18

*Baseline: 2026-09-02 (claude-trends-2026-09-02-delta.md). Window 2026-09-02 → 2026-09-18 (16 days). Sources: Anthropic first-party (claude.com announcements, Claude Code "What's new" W36–W37, Platform release notes), releasebot changelog summary v2.1.262–v2.1.276, 14 YouTube transcripts (12 in or near window), and a separate web sweep of hobby and personal-project use across domains.*

*This run adds a second lane at the user's request: **what other people are doing with Claude for their hobbies**, cast deliberately wide rather than anchored on the user's own interests.*

---

## Executive Summary

- **Cowork and chat merged into one Claude** (2026-09-16). Docs and Slides (beta) and Claude Design are now available from any conversation, with shared context. Rolling out on Pro/Max first.
- **Projects became a coordinator, not a folder** (2026-09-17, beta). You describe a goal; a coordinator splits it into parallel threads (each a full Claude Code session) with shared memory and a shared file/artifact library, reviews the outputs, and assembles the result. Threads are **cloud-only for now**.
- **Weekly usage limits changed on 2026-09-14** — the temporary +50% boost expired and a permanent +25% (over May levels) replaced it. Net effect vs the prior month: **~17% less weekly usage**. The separate Opus-only weekly cap was **removed**.
- **Anthropic says Claude now leads ~25–26% of its own R&D work** (zero in February), and is involved in ~90% in collaboration; ~30,000 agents doing research/engineering work as of August.
- **Hobby use has its own ecosystem now.** The best-evidenced clusters are Home Assistant automation, tabletop RPG tooling, retro gaming, and a "Claude writes the code, human is the hands" pattern on physical hardware (ESP32, cars, pen plotters, radios). Anthropic's own data: personal use is ~35% of Claude.ai conversations on weekdays and ~50% on weekends.

---

## NEW Features / Releases

### Claude apps

| Item | Detail | Source | Strength |
|---|---|---|---|
| **One Claude** (09-16) | Cowork and chat unified. Docs and Slides in beta, Claude Design built in. Existing chats, projects, artifacts, connectors, skills preserved; no user action. Pro/Max over the next few weeks; Team/Free after; Enterprise admins get 30+ days' notice. | claude.com/blog/cowork-is-now-claude | **HIGH** |
| **Projects redesigned** (09-17, beta) | Coordinator chat delegates to parallel threads, each a full Claude Code session; shared memory and library; steerable from phone; continues with laptop closed. Per-project usage tracking; model and effort configurable separately for coordinator and workers. Threads run in the cloud; local execution "coming very soon." | claude.com/blog/projects-redesigned | **HIGH** |
| Projects rollout gate | First wave: Pro/Max users of Claude Code cloud sessions **with no existing web/desktop projects**. Widening to all Claude Code Pro/Max over the following week, then Team/Enterprise. | same | **HIGH** |
| Claude for Small Business (09-15), Claude for Financial Advisors (09-14) | Vertical packages: workflows, integrations, training; advisor plugin with a licensing credit for September sign-ups. | claude.com announcements | **HIGH** |
| Cowork feature map | Task assignment vs chat Q&A; browser automation; scheduled cloud runs (hourly/daily/weekly); **Dispatch** (phone-initiated control of your own computer); **"record a skill"** (screen + voice + click capture, Mac, paid plans). | R2FFvPDUo7g | MEDIUM |
| Claude in Chrome default blocks | Financial-services and adult sites blocked by default. | 0FAsRBsk9YM | MEDIUM |

### Models and API

| Item | Detail | Source | Strength |
|---|---|---|---|
| Fable 5.1 **and Mythos 5.1** (09-01) | 1M context, 128k max output, adaptive thinking, $0.25/MTok cache reads. Mythos 5.1 is new to this series. | Platform release notes | **HIGH** |
| On-demand compaction (09-14) | Messages API `compact-2026-09-04` beta header. | Platform release notes | **HIGH** |
| Managed Agents `auto` permission mode (09-10) | Server-side evaluation of agent actions. | Platform release notes | **HIGH** |
| `ant apply` (09-03) | Manage API resources as code. | Platform release notes | **HIGH** |

### Claude Code CLI (v2.1.262 → v2.1.276)

| Item | Detail | Source | Strength |
|---|---|---|---|
| **`claude plugin eval`** (W37) | Run a plugin against test cases, score, compare against a no-plugin baseline; `init` drafts cases and graders. | What's new W37 | **HIGH** |
| `maxEffortLevel` (W37) | Caps effort on every provider. | W37 | **HIGH** |
| Desktop panes pop out (W37) | Undock any pane into its own window. | W37 | **HIGH** |
| **`/skill-doctor`** (W36) | Shows each skill's context cost and usage frequency. | W36 | **HIGH** |
| Background computer use on macOS (W36) | Desktop, Pro/Max. Not Windows. | W36 | **HIGH** |
| Live `/diff` panel (W36) | Refreshes beside the conversation in fullscreen. | W36 | **HIGH** |
| Skills/plugins sync from claude.ai (v2.1.275) | Account skills and plugins appear in terminal sessions. | releasebot | MEDIUM |
| Ctrl+Enter "send now" (v2.1.275) | Interrupts the turn and dispatches queued messages. | releasebot | MEDIUM |
| Memory-pressure warning; `CLAUDE_CODE_MCP_STARTUP_WAIT_MS` (v2.1.274) | Visible critical-memory warning; bound on first-turn MCP wait. | changelog; LRQ3QkVPffM | **HIGH** |
| Per-command domain allowlists for sandboxed shells; fast mode in remote sessions (v2.1.271) | | releasebot | MEDIUM |
| Fork a remote-control session to run locally (v2.1.273) | | releasebot | MEDIUM |

---

## NEW Workflow Patterns

- **Photo as debug input.** Photograph a malfunctioning physical output (e-ink display, printed part, plotter drawing) and paste it in rather than describing it. Claude diagnosed a 34-pixel row offset from a phone photo. `Zvb01TRY6UY`; independently in the pen-plotter case below.
- **Probe the hardware, don't trust the docs.** Given an under-documented radio protocol, Claude wrote a probe that set and read every control and flagged near-identical values as likely stubs. `3XDqqBHGqwU`.
- **State what works, not only what is broken.** "X doesn't work" alone makes the agent fixate and sometimes break adjacent working features. `3XDqqBHGqwU`.
- **Split models by sub-task.** Fable for modeling, Opus for rigging and animation, a purpose-built staging tool in between — reported as materially faster than one model doing everything. `BW0pEuQ6ZXw` (single creator).
- **Compose MCP servers in one session.** Blender + 3D-asset generation, or DAW + Blender, configured side by side with no special setup. `g_XF5l1ighc`, `BW0pEuQ6ZXw`.

---

## NEW Tools / MCPs / Integrations

| Tool | Use | Verdict | Source |
|---|---|---|---|
| FreeCAD MCP (community) | Text → parametric part edits | Text prompts clean in ~30 s; image-to-model struggled; Sonnet/Haiku sufficient | `MrOUIC1TJGY` |
| 3D AI Studio MCP + Blender MCP | Generated PBR textures and props, assembled in Blender, exported to Unity | Worked | `g_XF5l1ighc` |
| **Producer Pal** (Ableton Max-for-Live) | Claude Code controls Ableton | **Failed** — empty clips, MIDI in wrong view, musically wrong edits | `dVt8gBynsRQ` |
| Home Assistant MCP (`ha-mcp`, 86 tools) | Automations written against the user's own entity IDs | Mature; multiple community threads | github.com/homeassistant-ai/ha-mcp |
| D&D Beyond MCPs; Mimir DM; DM20 Protocol | Character/campaign access, NPC and module authoring | Active ecosystem | GitHub, mcpmarket.com |
| Yahoo Fantasy Football MCP | Lineup optimisation, draft help | Open source | github.com/derekrbreese |
| Adobe for Creativity connector | Photoshop/Lightroom/Premiere from chat | Cloud-exported files only | PetaPixel 2026-04-28 |

---

## Notable Applications — what other people are doing with their hobbies

Ranked by the strength of evidence found, not by novelty.

1. **Home automation (Home Assistant).** The most active and most polished category. A Cowork user got CO2 alerts, auto-lock and sunset lighting, plus a broken automation fixed (XDA, 2026-05-20). Others run a whole house through Claude Code as the primary interface, or built a new house's setup from scratch (HA community forum). A German creator documented three months of handing every automation to Claude (`uiyfxtosuCk`, older model generation).
2. **Tabletop RPGs.** D&D Beyond MCP servers, campaign-authoring skills with 20–66 tools, and an Obsidian-backed Dungeon Master's assistant.
3. **Retro gaming.** One user plugged an Android handheld into Claude Code over USB/ADB; Claude audited ROMs across 26 systems, synced 366 files and set up emulators in about 3 hours (jimchristian.net, 2026-03-25). A developer had Claude write a working NES emulator that plays Donkey Kong in the browser (Tom's Hardware; HN).
4. **Cars.** A kei-car owner built a real-time OBD-II dashboard — 36 live parameters, ~21 samples/sec, SQLite, PDF trip reports — writing no code himself (note.com, 2026-07). There are packaged skills for OBD-II decoding and CAN-bus reverse engineering.
5. **Cheap electronics (ESP32).** From $20 boards: a live sea-conditions e-ink display, a Bluetooth spectrum analyser for phone audio, an e-paper "sonic Polaroid" of a room's temperature, humidity and noise, a Wi-Fi/Bluetooth airspace scanner, and a desk mascot driven by Claude Code hooks that shows idle / working / needs-approval (`Zvb01TRY6UY`, `Vt5APRiFBSU`). The pattern: identify unknown hardware cold, back up firmware, then flash, test, photograph, fix.
6. **Ham radio.** A club lecture built a full rig-control GUI (frequency, S-meter, mode buttons, mouse-wheel tuning) from one natural-language spec with no CAT library, and diagnosed a manufacturer firmware bug from a Chinese-only datasheet; the vendor shipped the fix within days. The session also hit the usage limit mid-demo (`3XDqqBHGqwU`).
7. **Pen plotters and generative art.** Claude produced SVGs, the owner plotted and photographed them, and Claude iterated — learning that on-screen opacity does not exist when a pen is either touching paper or not (harmonique.one, 2026-02).
8. **Genealogy.** A researcher grew a family tree from fewer than 10 to 168 people across 19 lines and 300+ years, with sourced records in per-person Markdown files and an SVG tree (fulghum.io, 2026-03). Genealogy societies report Claude transcribing cursive records into comparison tables.
9. **Parent-and-child builds.** A flag-guessing game with an 8-year-old in under an hour, where the parent judged the child's hand-ranking of flags more educational than the code; a Thomas-the-Tank-Engine alphabet app built in one Sunday; an 11-year-old shipping a game in 4 weeks.
10. **Game dev and 3D scenes.** A full dragon flythrough built with Blender MCP, Godot MCP and a video-to-video reskin (`BW0pEuQ6ZXw`); an alchemist-shop interior assembled from generated assets (`g_XF5l1ighc`).
11. **Smaller niches with real examples:** fantasy football (MCP server and skill), a fitness coach integrating Garmin/Coros/WHOOP with Obsidian memory, a git-repo pantry that answers "what can I cook right now," and a personal life dashboard still in daily use 3.5 months later (`froH46jjFlY`).

**Searched and found thin or nothing concrete:** knitting/crochet, woodworking, quilting, model trains, RC aircraft, beekeeping, aquariums, gardening/hydroponics, astronomy, birding, chess, guitar. This is absence of evidence in web search, not evidence of absence.

### The reusable shapes

- **An MCP server as a bridge into the hobby's existing app** (Home Assistant, D&D Beyond, Yahoo Fantasy, Blender, FreeCAD).
- **USB, serial or ADB as Claude's hands** on physical devices (ESP32, handhelds, cars, radios).
- **A photo closes the physical feedback loop.**
- **A lifelong hobby turned into a versioned personal dataset** — genealogy, fitness, and pantry kept as files Claude can read and update.
- **Hobby-specific skills and plugins** are now packaged and installable.

---

## Pricing / Cost shifts

- **Weekly limits, 2026-09-14:** the temporary +50% boost (since May) expired 09-13; a permanent +25% over May levels began 09-14. 150 → 125 units, a **~17% cut** from the prior month. The 5-hour window is unchanged. **The separate Opus-only weekly cap was removed** — the whole weekly budget can go to any model. Verified across multiple outlets (BleepingComputer, implicator.ai, daily.dev); original source is an Anthropic post on X.
- Projects threads run concurrently and **draw down limits faster**; Anthropic says so in the announcement.
- A live evening hardware session hit 95–98% of a personal plan's limit with a 43-minute reset wait (`3XDqqBHGqwU`).

## Consensus shifts (vs 2026-09-02)

- **Orchestration moved into the product.** The baseline's "mesh of sessions" (cross-session messaging, fork mode, no subagent cap) was user-assembled. Projects now ships a coordinator that does the splitting and handoffs itself.
- **Photo/screenshot verification is a standard hobbyist technique**, strengthening the baseline's "evidence-producing verification" thread.
- **Multi-MCP composition is unremarkable** in creator content.

## Contradictions vs baseline

1. **None against a HIGH-strength baseline claim.** Auto mode default, cross-session messaging and the Concise style are all confirmed.
2. **MCP integrations are not uniformly usable.** Producer Pal (Ableton) failed outright. Treat DAW control as a gap, not a solved category.
3. **Refinement on autonomy:** the baseline's RemakeBench result (slow, visually blind single-session build) is answered in `BW0pEuQ6ZXw` by composing models and tools rather than running longer — single creator, MEDIUM.
4. **`-Nmo6zqVicI` is not a Claude case study** — its agent is GPT-5.4-mini via a third-party harness. Excluded from findings.

---

## Sources

| Video ID | Title | Channel | Upload date | Strength |
|---|---|---|---|---|
| shYJ0P-vvdI | Don't Miss These 7 Claude Code Updates | Eric Tech | 2026-09-18 | MEDIUM |
| LRQ3QkVPffM | Claude Code 2.1.274 | Cognitive Capital | 2026-09-18 | MEDIUM |
| 0FAsRBsk9YM | What People Actually Do With Claude | Drago Agent | 2026-09-17 | LOW-MEDIUM |
| R2FFvPDUo7g | Learn 95% of Claude Cowork in Under 9 Minutes | Tristen O'Brien | 2026-09-17 | MEDIUM |
| dVt8gBynsRQ | Control Ableton Live with Claude Code | JulianNox | 2026-09-12 | MEDIUM (negative result) |
| froH46jjFlY | 3.5 Months Later: Claude Code Life Dashboard | Jerad Hill | 2026-09-10 | MEDIUM |
| Vt5APRiFBSU | I Plugged 3 More $20 ESP32s Into Claude Code | Creator Magic | 2026-09-09 | MEDIUM-HIGH |
| BW0pEuQ6ZXw | Fable 5 Makes FULL GAME Using Godot MCP Blender MCP | JC BuenaVentura | 2026-09-04 | MEDIUM |
| Zvb01TRY6UY | I Plugged a $20 ESP32 Into Claude Code | Creator Magic | 2026-09-02 | MEDIUM-HIGH |
| 3XDqqBHGqwU | Claude Code Meets the Xiegu G90 | VK2MB-TV | 2026-08-26 | MEDIUM-HIGH |
| g_XF5l1ighc | I Gave Claude a 3D Model MCP Server | Building Aeon | 2026-08-16 | MEDIUM |
| MrOUIC1TJGY | I Connected Claude AI to FreeCAD | Engineering With Pritam | 2026-08-04 | MEDIUM |
| -Nmo6zqVicI | Raspberry Pi as wireless Arduino workbench | IQ Workshop | 2026-07-23 | EXCLUDED (not Claude) |
| uiyfxtosuCk | 3 Monate mit Claude in Home Assistant | simon42 | 2026-07-01 | LOW (pre-window, older models) |

**Web sources (first-party):** [Cowork is now Claude](https://claude.com/blog/cowork-is-now-claude) · [Projects redesigned](https://claude.com/blog/projects-redesigned) · [Announcements](https://claude.com/blog-category/announcements) · [Claude Code What's new](https://code.claude.com/docs/en/whats-new) · [Platform release notes](https://platform.claude.com/docs/en/release-notes/overview) · [Economic Index June 2026](https://www.anthropic.com/research/economic-index-june-2026-report) · [How people use Cowork](https://claude.com/blog/how-people-are-using-claude-cowork)

**Web sources (third-party):** [BNN Bloomberg / AP on Claude-led R&D](https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/09/18/anthropic-says-its-model-claude-is-helping-to-build-the-next-version-of-itself/) · [BleepingComputer on limits](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-is-cutting-claude-codes-current-weekly-limits-by-17-percent/) · [implicator.ai on limits](https://www.implicator.ai/anthropic-claude-code-weekly-limits-september-14/) · [releasebot Claude Code](https://releasebot.io/updates/anthropic/claude-code) · [ha-mcp](https://github.com/homeassistant-ai/ha-mcp) · [XDA Home Assistant + Cowork](https://www.xda-developers.com/claude-cowork-access-home-assistant-config-unlocked-automations-didnt-know-were-possible/) · [HA community thread](https://community.home-assistant.io/t/building-my-smart-home-from-scratch-with-claude-code-home-assistant/994464) · [ddb-mcp](https://github.com/iamjameslennon/ddb-mcp) · [retro handheld](https://jimchristian.net/blog/2026/03/25-i-plugged-a-games-console-into-claude-code/) · [NES emulator](https://www.tomshardware.com/video-games/retro-gaming/dev-uses-claude-ai-to-write-a-functional-nes-emulator-you-can-test-it-now-playing-donkey-kong-in-your-browser) · [OBD-II dashboard](https://note.com/wise_bee4925/n/n7860794ba328?hl=en) · [CAN-bus RE](https://www.csselectronics.com/pages/can-bus-reverse-engineering-ai-llm-claude) · [ESP32 desk pet](https://blog.adafruit.com/2026/04/17/making-an-esp32-device-which-connects-to-claude-over-bluetooth/) · [pen plotter](https://harmonique.one/posts/i-gave-claude-access-to-my-pen-plotter) · [genealogy](https://fulghum.io/genealogy) · [flag game with son](https://danielbower.com/2026/07/03/game-son-claude-code.html) · [Thomas ABCs](https://robbobobbo.substack.com/p/thomas-the-tank-engine-abcs) · [fantasy football MCP](https://github.com/derekrbreese/fantasy-football-mcp-public) · [fitness coach](https://github.com/BorisBW/claude-fitness-cn) · [Cooking with Claude](https://ellemorrill.substack.com/p/cooking-with-claude) · [Adobe connector](https://petapixel.com/2026/04/28/claude-ai-can-orchestrate-creative-workflows-across-adobe-apps/)

## Methodology

- **Baseline:** auto-detected, `05-Archive/reports/claude-trends-2026-09-02-delta.md`.
- **YouTube MCP:** 8 searches — news: "Claude Code new features" (after 09-02, by date). Hobby: "Claude hobby project maker", "Claude Code Arduino ESP32 home automation build", "Claude MCP Blender OR KiCad OR Ableton OR FreeCAD", "Claude Code music synthesizer MIDI Ableton", "Claude Code SDR ham radio OR telescope OR weather station", "Claude Code laser cutter OR CNC OR pen plotter OR generative art" (0 results), "Claude Code personal project non-programmer built". The default five seed queries were replaced by focused variants per the focus-area argument.
- **Web:** first-party pages fetched directly; hobby lane delegated to one subagent (Sonnet) with instructions to cast wide and not anchor on the requester's interests (redirected mid-run at the user's request).
- **Transcripts:** 16 attempted via `youtube_transcript_api`, **14 succeeded**, 2 had no transcript (`f_Kbux-pH-E`, `Js7Xkt7uQ-Y`). Analysed by one subagent (Sonnet).
- **Filters:** many non-English and Shorts results skipped. Subscriber counts were **not** checked this run — a deviation from the skill's quality gate.
- **Verification:** the weekly-limit claim (initially sourced only to a creator citing an X post) was cross-checked against three outlets before inclusion.
- **Playlist:** not created.
tell
