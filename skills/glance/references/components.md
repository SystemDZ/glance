# Page components

Write only the **body**. The script adds the page, the CSS, the JS, both themes and the footer. See every block rendered: `python3 SCRIPT demo kitchen-sink`.

## Frame of a page

```html
<header class="hero">
  <div class="eyebrow">Domain setup · 2 records left</div>
  <h1>Connect fellak.com</h1>
  <p class="lede">One line of context.</p>
</header>

<div class="answer"><small>Short answer</small>The verdict in one sentence.</div>
```

## Progress (optional)

```html
<section class="progress" data-total="5" data-done="3"><div class="segs"></div><div class="progress-label"></div></section>
```
Tick-boxes with `data-persist` add to "done" automatically.

## Steps

```html
<ol class="steps">
  <li class="step done"><div class="badge" aria-hidden="true">✓</div><div><span class="tag t-done">Done</span><h3>Short past-tense title</h3></div></li>
  <li class="step now">
    <div class="badge" aria-hidden="true">4</div>
    <div>
      <span class="tag t-now">Do this now</span>
      <h3>Add two A records</h3>
      <p>Where to click, in one sentence.</p>
      <div class="copyrows" style="margin-top:16px">
        <div class="copyrow"><div><small>A · @</small><b>216.198.79.1</b></div><button class="copy" type="button" data-copy="216.198.79.1">Copy</button></div>
      </div>
      <label class="check" style="margin-top:16px"><input type="checkbox" data-persist="step-4"> I did this</label>
    </div>
  </li>
  <li class="step"><div class="badge" aria-hidden="true">5</div><div><span class="tag t-mute">Then</span><h3>Next step title</h3><p>One sentence.</p></div></li>
</ol>
```
Only one `step now`. Done steps stay one line.

## Callouts

```html
<div class="callout stop"><span class="tag t-stop">Hands off</span><h3>Do not edit these</h3><ul class="chips"><li>MX records</li><li>SPF</li></ul></div>
<div class="callout warn"><span class="tag t-warn">Careful</span><h3>Title</h3><p>Include the undo step.</p></div>
<div class="callout ok"><span class="tag t-done">Safe</span><h3>Title</h3><p>Say why it is safe.</p></div>
<div class="callout info"><span class="tag t-now">Good to know</span><h3>Title</h3><p>Two lines at most.</p></div>
```

## Compare

```html
<div class="compare">
  <div class="option rec"><span class="tag t-done">Recommended</span><h3>Option A</h3><ul><li>Reason</li><li>Reason</li></ul></div>
  <div class="option"><span class="tag t-mute">Alternative</span><h3>Option B</h3><ul><li>Reason</li></ul></div>
</div>
```
Recommend one option, always.

## Table

```html
<div class="tablewrap"><table>
  <thead><tr><th>Item</th><th>Status</th><th class="num">Cost</th></tr></thead>
  <tbody><tr><td>Hosting</td><td><span class="chip done">Live</span></td><td class="num">$0</td></tr></tbody>
</table></div>
```
Chip colors: `done`, `now`, `warn`, `stop`, `mute`.

## Facts, timeline, code, details, later

```html
<dl class="kv"><dt>Owner</dt><dd>You</dd><dt>Status</dt><dd>Live</dd></dl>

<ul class="timeline"><li class="done"><b>Planned</b><span>Monday</span></li><li class="now"><b>Building</b><span>This week</span></li><li><b>Launch</b><span>Friday</span></li></ul>

<div class="code"><pre>npm run build</pre><button class="copy" type="button" data-copy="npm run build">Copy</button></div>

<details class="more"><summary>Details, if you want them</summary><div><p>Long explanation.</p></div></details>

<section class="later">
  <span class="tag t-warn" style="justify-self:start">Later, not today</span>
  <h2>Heading</h2>
  <ol><li><b>First</b> thing.</li></ol>
</section>
```

Wrap groups in `<section class="section"><h2>Heading</h2> ... </section>`.

## Escaping

Inside HTML, write `&amp;`, `&lt;` and `&gt;` for `&`, `<` and `>`. In `data-copy`, use the same escapes.
