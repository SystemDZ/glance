# scannable

**AI answers you can actually read.**

Most AI replies are walls of text. `scannable` is an [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that fixes that in two moves:

1. **It asks you once** how you like answers: how long, which formats, one step at a time or all at once, when a visual page beats text, light or dark. It saves your answers.
2. **It then adapts every reply.** Quick things stay short, structured text. Complex things (4+ steps, comparisons, plans, lots of values to copy) become a clean visual page that **opens in your browser**, with the link shown in chat.

## What a page looks like

- Verdict first, in one sentence.
- One loud card: the step you are on. Finished steps shrink, upcoming ones go grey.
- Color means something: 🔵 now or info, 🟢 done or safe, 🔴 stop, 🟡 careful or later.
- Copy buttons on every value, a "do not touch" box for risky things, an undo plan, and a collapsed "details" section.
- Light and dark theme, phone friendly, fully offline (no fonts, scripts or images from the web).

Try the gallery after installing: `python3 <skill-folder>/scripts/scannable.py demo kitchen-sink`

## Install

### Claude Code (plugin)

```text
/plugin marketplace add SystemDZ/scannable
/plugin install scannable@scannable
```

### Claude Code (manual)

```bash
cp -R skills/scannable ~/.claude/skills/scannable
```

### Other agents

Any agent that reads `SKILL.md` skills: copy the `skills/scannable` folder into that agent's skills directory. For an agent without skill support, paste `skills/scannable/SKILL.md` into its instructions and keep the folder somewhere it can run `scripts/scannable.py`.

Requirements: Python 3 (standard library only). No packages, no network.

## Use it

Say `/scannable`, or just complain: "your answers are too long", "make this visual", "give me a checklist".

| You say | It does |
|---|---|
| `/scannable` | Runs the quiz (Quick: 4 questions, or Full: 9) |
| "change how you answer" | Re-runs the quiz with your current choices as defaults |
| "show me a page for this" | Builds a page, opens it, shows the link |
| "reset scannable" | Deletes your saved preferences |

## What it stores

Everything is in `~/.scannable/` (override with `SCANNABLE_HOME`):

- `preferences.json`: your answers.
- `pages/`: the pages it built. `scannable.py prune --days 30` cleans old ones.

Pages are plain local files. The skill is told never to put secrets on them. Nothing is uploaded anywhere. Publishing a page online only happens if you ask.

## How it decides text or page

| Signal | Example |
|---|---|
| 4+ steps you must perform | Connecting a domain |
| 3+ options or 4+ criteria | Picking a database |
| A plan, timeline, architecture or report | A migration plan |
| 4+ values to copy | DNS records, env vars |

Yes/no answers, one-liners, quick fixes and urgent errors always stay as short text. You can change the line in the quiz (never, complex only, longer than my limit, always).

## Layout

```text
skills/scannable/
  SKILL.md                 instructions the agent follows
  scripts/scannable.py     build, open, preferences (stdlib only)
  assets/                  template, design system CSS/JS, demo pages
  references/              quiz wording, component snippets
```

## License

MIT
