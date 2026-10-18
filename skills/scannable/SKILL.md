---
name: scannable
description: Stop walls of text. Quizzes the user once about how they like answers (chat length, formats, one step at a time or all at once, when a visual page beats text, theme, auto-open), saves the answers, then applies them to every reply. For complex answers (many steps, comparisons, plans, many values to copy) it builds a clean self-contained HTML page, opens it in the browser and shows the link. Use when the user says answers are too long, confusing or hard to read, asks for something visual, a checklist or a page, wants to set or change how answers look, or types /scannable. Works with any agent that supports SKILL.md skills.
license: MIT
metadata:
  version: "1.0.0"
---

# Scannable

Make answers fast to read. Learn how this user likes to receive information, remember it, and switch between a short text reply and a visual page at the right moment.

`SCRIPT` below means `scripts/scannable.py` inside this skill's folder. Run it with `python3` (use `py` on Windows). It needs only the Python standard library. If Python is missing, see "No Python" at the end.

## 1. Always on: five rules

Apply these even before any quiz, to every reply:

1. **Answer first.** The first line is the verdict or the next action. No preamble, no recap.
2. **One idea per block.** Short blocks, blank lines between them.
3. **Values live in tables or code**, never buried inside sentences.
4. **When the user must act, give one step at a time**, and wait for "done".
5. **If you are about to write more than about 12 lines, build a page instead** (section 4).

## 2. Load preferences, or run the quiz

Run `python3 SCRIPT prefs get`.

- It prints a JSON object with `chat`, `visual` and `delivery` keys: **apply it silently** and go to section 3. Do not mention the skill.
- It prints `{}`: no preferences yet. Run the quiz (below), unless the user clearly declined.
- The user says "change how you answer", "reset", or "/scannable": run the quiz again, showing the current values as the defaults.

### How to run the quiz

- Offer two sizes: **Quick** (4 questions, about 30 seconds) or **Full** (9). Recommend Quick.
- **Skip anything the user already told you** in this conversation (for example "I hate long answers" answers the length question). State what you inferred and ask only the rest.
- Use the host's structured-question tool if there is one. Otherwise ask in **one message**, numbered, with lettered options, the recommended option marked, and tell the user they can answer like `1b 2a 4a` or just say `defaults`.
- Exact wording, options and the mapping to saved values are in `references/quiz.md`. Read it before asking.
- Offer a taste test: `python3 SCRIPT demo styles` opens a page showing the same answer as short text, structured chat and visual page, so the user can point at what feels right.
- After the answers, show a small confirmation table, save with `python3 SCRIPT prefs set --json '<patch>'`, then **immediately prove it**: answer the user's last real question in the chosen style (building a page if the rubric says so).

## 3. Decide: text or page

Read `visual.trigger` from the preferences.

| Trigger | Build a page when |
|---|---|
| `never` | Never. Text only. |
| `complex` (default) | At least one strong signal, or two weak ones |
| `long` | The reply would be longer than the user's chat length |
| `always` | Any technical answer longer than two lines |

**Strong signals:** 4 or more sequential steps the user must perform. A comparison of 3 or more options, or 4 or more criteria. A plan, roadmap, timeline, architecture or report. 4 or more values to copy (DNS records, env vars, commands). Status of a multi-part job. The user asks to "show", "visualize" or "make a page".

**Weak signals:** a table wider than 3 columns. More than about 12 lines of output. 3 or more code blocks. A hand-off meant for someone else.

**Never build a page for:** a yes/no, a one-line answer, a quick fix, an error that needs an immediate reply, or a small code snippet.

When a page is built, the chat message is **three lines at most**: the one-sentence answer, the link on its own line, the single thing to do next.

## 4. Text answers (no page)

Follow `chat` in the preferences.

- **length:** `one_line` = 1 line. `short` = up to 6 lines. `medium` = up to 15. `detailed` = no cap, still structured.
- **steps:** `one_at_a_time` = send only the current step, then wait. `few` = 2 to 3. `all` = everything.
- **markers:** if `emoji`, use a consistent legend: 🟢 do or safe, 🔴 stop or do not touch, 🟡 careful or later, 🔵 now or info. Use bold labels instead if `bold`, nothing if `plain`.
- **format:** use only the formats the user picked. Tables for values and comparisons. If the host cannot render markdown tables, use aligned lists.
- **level:** `plain` = no jargon, say what each thing is for. `technical` = assume expertise.
- Ask **at most one question** per reply.

## 5. Build a page

1. **Write only the body.** A short HTML fragment using the blocks in `references/components.md`. Save it to a temp file. You do not write `<html>`, CSS or JavaScript: the script wraps your body in the finished design system, with both light and dark themes.
2. **Structure, top to bottom:**
   - `hero`: small label, a title of 2 to 4 words, one line of context.
   - `answer`: the verdict in one sentence. This must answer the question on its own.
   - The core block: steps, comparison, table or timeline.
   - Callouts for what to avoid (red) and what to know (amber, green, blue).
   - Long detail inside a `details.more` block, collapsed.
3. **Design rules (do not break them):**
   - One loud element per screen: at most one `step now` card.
   - Color means something and nothing else: blue = now or info, green = done or safe, red = stop, amber = careful or later.
   - Every value the reader must copy gets a copy button.
   - No paragraph longer than 3 lines. Turn it into a list, table or callout.
   - No images, no external links to fonts or scripts, no placeholder text, no emoji decoration.
   - Write in the user's language and level.
4. **Build and open:** `python3 SCRIPT show --title "Short name" --body body.html`.
   - If `delivery.auto_open` is `ask`, build with `--no-open`, show the link, and run `open PAGE` only if the user says yes.
   - It writes the page to `~/.scannable/pages/`, opens it in the default browser (unless `delivery.auto_open` is `no`) and prints `LINK:`, `PATH:` and `OPENED:` lines.
   - **Always show the `LINK:` value to the user**, even when it opened. If `OPENED: no`, say why (for example a headless or SSH session) and give the link.
5. **Update, don't pile up:** if you are revising a page you already made this session, build again with the same title. Old pages are cleaned by `python3 SCRIPT prune`.

Do a last check before sending: does the first screen answer the question? Is there exactly one thing to do next? Is anything redundant? Cut it.

## 6. Make it permanent (optional, ask first)

The preferences file only exists on this machine. If the user wants the style to apply even when this skill is not loaded, offer to add a short block to their agent instructions file (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or the tool's rules file). Show the exact text first (template in `references/quiz.md`) and write it only after a clear yes. Record the choice with `prefs set --json '{"delivery":{"persist_in_instructions":"yes"}}'`.

## 7. Optional, host-specific

- **Sharing a page online:** only if the user asks, and only if the host has a safe way to publish (for example Claude's Artifact tool). Always create the local file first. Never publish silently: pages can contain private details.
- **Privacy:** pages are plain local files. Do not put secrets, tokens or passwords on a page. Show a placeholder like `<your-token>` instead.

## 8. Commands

| Command | Does |
|---|---|
| `prefs get` / `prefs set --json '{...}'` / `prefs reset` / `prefs path` | Read, merge, delete or locate preferences |
| `show --title T --body FILE` | Build, open, print the link |
| `build --title T --body FILE` | Build only |
| `open PAGE.html` | Open an existing page and print its link |
| `demo styles` / `demo kitchen-sink` | Style taste test / component gallery |
| `prune --days 30` | Delete old pages |

Flags: `--no-open` never opens the browser, `--json` prints machine-readable output, `--theme light|dark|auto` overrides the saved theme.

## No Python

If Python is unavailable, write one complete HTML file yourself: copy `assets/template.html`, paste `assets/base.css` and `assets/base.js` where `{{CSS}}` and `{{JS}}` are, put your body at `{{BODY}}`, save it under `~/.scannable/pages/`, then open it with `open` (macOS), `xdg-open` (Linux) or `start ""` (Windows) and show the `file://` link. Read and write `~/.scannable/preferences.json` directly.
