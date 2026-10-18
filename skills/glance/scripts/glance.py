#!/usr/bin/env python3
"""glance helper: build, open and manage visual answer pages, and store the user's answer-style preferences.

Standard library only. Works on macOS, Linux, Windows and WSL.

  glance.py prefs get|set|reset|path     read or change saved preferences
  glance.py build  --title T --body FILE write a finished page (does not open it)
  glance.py show   --title T --body FILE build + open in the browser + print the link
  glance.py open   PAGE.html             open an existing page and print the link
  glance.py demo   kitchen-sink|styles   open a built-in demo page
  glance.py prune  [--days 30]           delete old pages

Everything lives in ~/.glance (override with the GLANCE_HOME environment variable).
"""
import argparse
import datetime as dt
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

HOME = Path(os.environ.get("GLANCE_HOME") or (Path.home() / ".glance"))
PAGES = HOME / "pages"
PREFS = HOME / "preferences.json"
SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"

DEFAULTS = {
    "version": 1,
    "chat": {"length": "short", "format": ["bullets", "tables", "code"], "steps": "one_at_a_time",
             "markers": "emoji", "level": "plain"},
    "visual": {"trigger": "complex", "theme": "auto", "density": "airy"},
    "delivery": {"auto_open": "yes", "persist_in_instructions": "no"},
}


def deep_merge(base, extra):
    out = dict(base)
    for key, val in extra.items():
        out[key] = deep_merge(out[key], val) if isinstance(val, dict) and isinstance(out.get(key), dict) else val
    return out


def read_prefs():
    try:
        return json.loads(PREFS.read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def write_prefs(data):
    HOME.mkdir(parents=True, exist_ok=True)
    PREFS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48] or "page"


def cmd_prefs(args):
    if args.action == "path":
        print(PREFS)
    elif args.action == "get":
        print(json.dumps(read_prefs(), indent=2, ensure_ascii=False) if PREFS.exists() else "{}")
    elif args.action == "reset":
        if PREFS.exists():
            PREFS.unlink()
        print("preferences reset")
    elif args.action == "set":
        try:
            patch = json.loads(args.json or "{}")
        except ValueError as err:
            sys.exit(f"invalid JSON: {err}")
        merged = deep_merge(deep_merge(DEFAULTS, read_prefs()), patch)
        write_prefs(merged)
        print(json.dumps(merged, indent=2, ensure_ascii=False))


def assemble(title, body_html, theme, lang, density):
    template = (ASSETS / "template.html").read_text("utf-8")
    css = (ASSETS / "base.css").read_text("utf-8")
    js = (ASSETS / "base.js").read_text("utf-8")
    attrs = ""
    if theme in ("light", "dark"):
        attrs += f' data-theme="{theme}"'
    if density == "compact":
        attrs += ' data-density="compact"'
    page = template
    for key, val in {
        "{{TITLE}}": html.escape(title),
        "{{LANG}}": html.escape(lang),
        "{{ATTRS}}": attrs,
        "{{DATE}}": dt.date.today().isoformat(),
        "{{CSS}}": css,
        "{{JS}}": js,
        "{{BODY}}": body_html,
    }.items():
        page = page.replace(key, val)
    return page


def read_body(args):
    if args.body == "-":
        return sys.stdin.read()
    path = Path(args.body)
    if not path.is_file():
        sys.exit(f"body file not found: {path}")
    return path.read_text("utf-8")


def build(args, body=None):
    prefs = deep_merge(DEFAULTS, read_prefs())
    body = body if body is not None else read_body(args)
    page = assemble(args.title, body, args.theme or prefs["visual"]["theme"], args.lang, prefs["visual"]["density"])
    PAGES.mkdir(parents=True, exist_ok=True)
    out = PAGES / f"{dt.datetime.now():%Y%m%d-%H%M%S}-{slugify(args.slug or args.title)}.html"
    out.write_text(page, "utf-8")
    return out


def is_wsl():
    return "microsoft" in platform.release().lower()


def open_in_browser(path):
    """Return (opened, note). Never raises."""
    uri = path.resolve().as_uri()
    system = platform.system()
    try:
        if system == "Linux" and not is_wsl() and not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
            return False, "no display available (SSH or headless): open the link yourself"
        if system == "Darwin":
            subprocess.run(["open", str(path)], check=True)
            return True, ""
        if system == "Windows":
            os.startfile(str(path))  # type: ignore[attr-defined]
            return True, ""
        if is_wsl():
            win = subprocess.run(["wslpath", "-w", str(path)], capture_output=True, text=True, check=True).stdout.strip()
            subprocess.run(["explorer.exe", win], check=False)
            return True, ""
        if shutil.which("xdg-open"):
            subprocess.run(["xdg-open", str(path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, ""
        return (True, "") if webbrowser.open(uri) else (False, "no browser found: open the link yourself")
    except Exception as err:  # noqa: BLE001 - opening is best effort
        return (True, "") if webbrowser.open(uri) else (False, f"could not open a browser ({err})")


def finish(path, no_open, as_json):
    prefs = deep_merge(DEFAULTS, read_prefs())
    want_open = not no_open and prefs["delivery"]["auto_open"] == "yes"
    opened, note = (open_in_browser(path) if want_open else (False, "auto-open is off" if not no_open else "not opened (--no-open)"))
    uri = path.resolve().as_uri()
    if as_json:
        print(json.dumps({"link": uri, "path": str(path.resolve()), "opened": opened, "note": note}))
    else:
        print(f"LINK: {uri}")
        print(f"PATH: {path.resolve()}")
        print(f"OPENED: {'yes' if opened else 'no'}" + (f" ({note})" if note else ""))


def cmd_build(args):
    out = build(args)
    print(f"PATH: {out.resolve()}")


def cmd_show(args):
    finish(build(args), args.no_open, args.json)


def cmd_open(args):
    path = Path(args.page)
    if not path.is_file():
        sys.exit(f"page not found: {path}")
    finish(path, args.no_open, args.json)


def cmd_demo(args):
    body = (ASSETS / f"body-{args.which}.html").read_text("utf-8")
    ns = argparse.Namespace(title={"kitchen-sink": "Component gallery", "styles": "Pick your answer style"}[args.which],
                            slug=f"demo-{args.which}", theme=None, lang="en", body=None)
    finish(build(ns, body), args.no_open, args.json)


def cmd_prune(args):
    cutoff = dt.datetime.now().timestamp() - args.days * 86400
    removed = 0
    for page in PAGES.glob("*.html") if PAGES.exists() else []:
        if page.stat().st_mtime < cutoff:
            page.unlink()
            removed += 1
    print(f"removed {removed} page(s) older than {args.days} days")


def main():
    parser = argparse.ArgumentParser(prog="glance", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prefs")
    p.add_argument("action", choices=["get", "set", "reset", "path"])
    p.add_argument("--json", help="JSON object to merge (for 'set')")
    p.set_defaults(fn=cmd_prefs)

    for name, fn in (("build", cmd_build), ("show", cmd_show)):
        p = sub.add_parser(name)
        p.add_argument("--title", required=True, help="short page name (2-4 words)")
        p.add_argument("--body", required=True, help="HTML fragment file for the page body, or - for stdin")
        p.add_argument("--slug")
        p.add_argument("--theme", choices=["auto", "light", "dark"])
        p.add_argument("--lang", default="en")
        p.add_argument("--no-open", action="store_true")
        p.add_argument("--json", action="store_true")
        p.set_defaults(fn=fn)

    p = sub.add_parser("open")
    p.add_argument("page")
    p.add_argument("--no-open", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_open)

    p = sub.add_parser("demo")
    p.add_argument("which", choices=["kitchen-sink", "styles"])
    p.add_argument("--no-open", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_demo)

    p = sub.add_parser("prune")
    p.add_argument("--days", type=int, default=30)
    p.set_defaults(fn=cmd_prune)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
