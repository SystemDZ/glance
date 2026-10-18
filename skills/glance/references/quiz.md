# The quiz

Ask in this order. Mark the recommended option **(recommended)**. Accept answers like `1b 2a`, `defaults`, or free text. Quick setup = Q1, Q3, Q5, Q8 (the rest take their defaults).

If the host has a structured-question tool, use it. Otherwise send one message like this:

> **Quick setup, 4 questions.** Reply like `1b 2a 3b 4a`, or `defaults`.

## Round 1: chat answers

**Q1. How long should normal chat answers be?**
- a) One line when possible
- b) Short, up to about 6 lines **(recommended)**
- c) Medium, up to about 15 lines
- d) Full detail, but well structured

→ `chat.length`: `one_line` | `short` | `medium` | `detailed`

**Q2. Which formats help you most?** (pick any)
- a) Bullets **(recommended)**
- b) Tables for values and comparisons **(recommended)**
- c) Headings and bold labels
- d) Short paragraphs
- e) Code blocks for anything I can copy **(recommended)**

→ `chat.format`: list of `bullets`, `tables`, `headings`, `prose`, `code`

**Q3. When you have to do something, I should give you:**
- a) One step at a time, then wait for "done" **(recommended)**
- b) Two or three steps at once
- c) Everything at once

→ `chat.steps`: `one_at_a_time` | `few` | `all`

**Q4. How should I mark warnings and steps in chat?**
- a) Bold labels such as **Do**, **Stop**, **Note** **(recommended)**
- b) Plain text, no labels
- c) Coloured emoji, only if you like them

→ `chat.markers`: `bold` | `plain` | `emoji`

## Round 2: visual pages

**Q5. When should I make a visual page instead of text?**
- a) Never, text only
- b) Only for complex things: 4+ steps, comparisons, plans, many values to copy **(recommended)**
- c) Whenever the answer is longer than my chat limit
- d) Always, for any technical answer

→ `visual.trigger`: `never` | `complex` | `long` | `always`

**Q6. How should pages look?**
- Theme: a) match my system **(recommended)** · b) light · c) dark
- Density: a) airy **(recommended)** · b) compact

→ `visual.theme`: `auto` | `light` | `dark`; `visual.density`: `airy` | `compact`

**Q7. How should I explain things?**
- a) Plain language, say what each thing is for **(recommended)**
- b) Technical, I know the field

→ `chat.level`: `plain` | `technical`

## Round 3: delivery

**Q8. After I build a page:**
- a) Open it in my browser and show the link **(recommended)**
- b) Just show me the link
- c) Ask me each time

→ `delivery.auto_open`: `yes` | `no` | `ask`

**Q9. Make this permanent by adding a short "answer style" block to your agent instructions file?**
- a) Yes, show me the text first
- b) No, keep it on this machine only **(recommended)**

→ `delivery.persist_in_instructions`: `yes` | `no`

## Saving

```bash
python3 SCRIPT prefs set --json '{"chat":{"length":"short","format":["bullets","tables","code"],"steps":"one_at_a_time","markers":"bold","level":"plain"},"visual":{"trigger":"complex","theme":"auto","density":"airy"},"delivery":{"auto_open":"yes"}}'
```

## Confirmation table to show after saving

| Setting | Your choice |
|---|---|
| Chat answers | short, bullets + tables + code |
| Steps | one at a time |
| Markers | bold labels |
| Visual page | only for complex things |
| Look | match system, airy |
| After building | open in browser |

Say "Tell me to change this any time", then answer their last question in the new style.

## Block for the instructions file (Q9 = yes)

Show it, then append only after a clear yes:

```markdown
## Answer style (glance)
- Lead with the answer or next action. No preamble, no recap.
- Chat replies: short (about 6 lines), bullets and tables, values in code blocks.
- When I must act, give one step at a time and wait for "done".
- Mark warnings with bold labels: **Do**, **Stop**, **Note**.
- For complex answers (4+ steps, comparisons, plans, many values) build a visual page with the glance skill, open it in my browser, and show the link.
```

Adjust each line to the saved preferences.
