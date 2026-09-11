"""Scratch generator for viz-wave1: parse WinForms Designer.cs controls and emit
self-contained visual-explainer-style HTML pages under ~/wireframe-host/viz/.
Not committed to the repo (one-shot, per wireframe pipeline convention)."""
import re, pathlib, html

SRC = pathlib.Path("/home/ubuntu/Documents/Obsidian/ClaimingToWeb/ref-code-20260904/UnitClaimingUI")
OUT = pathlib.Path("/home/ubuntu/wireframe-host/viz")

FORMS = [
    ("MainMenu", "Main menu — entry point with claiming action buttons (opened at startup via ShowMainMenu)."),
    ("UnitClaimingMainForm", "Core unit-claiming wizard flow (ShowUnitClaiming, takes MainFormVariation)."),
    ("Configuration", "Global settings page: Plant / Printing / Scale Interface / IP & Connection. Source defaults IP 172.20.152.226 / port 6671."),
    ("ViewUnitClaimingData", "Grid view of claimed-unit data (menu: View Data). Default sort CreatedDate descending."),
    ("ViewUnitClaimingDataPopup", "Detail popup for a selected ViewUnitClaimingData row."),
    ("ImportFromMTMS", "Import units from MTMS (menu: Import Units from MTMS)."),
    ("LeakingHousingLabel", "HGP leaking-housing label print flow."),
    ("WashedLeakTestedLabel", "Washed / leak-tested label print flow (takes FormVersion: normal vs reprint)."),
    ("SetToleranceFactor", "Set tolerance-factor value dialog."),
    ("ErrorDetail", "Error-detail dialog."),
    ("xxEditPackagingData", "Packaging-data editor (xx prefix suggests WIP; menu hook commented out in MDIParent1)."),
]

CTRL_RE = re.compile(r"this\.(\w+)\s*=\s*new\s+System\.Windows\.Forms\.(\w+)\(", )
TEXT_RE = re.compile(r"this\.(\w+)\.Text\s*=\s*\"([^\"]*)\"", )

def parse_designer(form):
    p = SRC / f"{form}.Designer.cs"
    if not p.exists():
        return []
    t = p.read_text(errors="replace")
    types = dict(CTRL_RE.findall(t))
    texts = dict(TEXT_RE.findall(t))
    rows = []
    for name, ctype in sorted(types.items(), key=lambda kv: kv[0]):
        if name.startswith("_") or ctype in ("IContainer", "ComponentResourceManager"):
            continue
        rows.append((name, ctype, texts.get(name, "")))
    return rows

PAGE_CSS = """
  html { font-size: 16px; }
  :root {
    --bg: #f4f1ea; --surface: #ffffff; --border: rgba(20,40,70,.12);
    --text: #1c2b3a; --text-dim: #5b6b7c;
    --primary: #0f5e8a; --primary-dim: rgba(15,94,138,.08);
    --accent: #b3541e; --ok: #1e7e46; --mono: 'Fragment Mono','SF Mono',Consolas,monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #101820; --surface: #182430; --border: rgba(255,255,255,.1);
      --text: #dbe7f0; --text-dim: #8fa3b5;
      --primary: #4fb0e0; --primary-dim: rgba(79,176,224,.14);
      --accent: #e09a4f; --ok: #4fce7f;
    }
  }
  * { box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif;
         max-width: 68rem; margin: 0 auto; padding: 2rem 1.5rem; line-height: 1.55; font-size: 1rem; }
  h1 { font-size: 1.9rem; text-wrap: balance; margin: 0 0 .25rem; }
  h2 { font-size: 1.25rem; margin: 2rem 0 .75rem; border-bottom: 2px solid var(--primary); padding-bottom: .3rem; }
  .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; color: var(--text-dim); }
  nav.crumb { margin-bottom: 1.5rem; font-size: .9rem; }
  nav.crumb a { color: var(--primary); }
  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr)); gap: 1rem; }
  .ve-card { background: var(--surface); border: 1px solid var(--border); border-radius: .6rem; padding: 1rem 1.1rem; }
  .ve-card h3 { margin: 0 0 .4rem; font-size: 1rem; }
  .ve-card .ctype { font-family: var(--mono); font-size: .75rem; color: var(--primary); }
  table { width: 100%; border-collapse: collapse; background: var(--surface); font-size: .92rem; }
  th, td { text-align: left; padding: .55rem .7rem; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; color: var(--text-dim); }
  td.mono, .mono { font-family: var(--mono); font-size: .82rem; }
  footer.src { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--border);
               font-size: .85rem; color: var(--text-dim); }
  .note { background: var(--primary-dim); border-left: 4px solid var(--primary);
          padding: .7rem 1rem; border-radius: 0 .5rem .5rem 0; margin: .6rem 0; }
"""

DEAD_UI_NOTES = {
    "SetToleranceFactor": "Unreachable in the legacy UI:</strong> the only caller (<span class=\"mono\">setToleranceFactorToolStripMenuItem_Click</span>) has been commented out since 6/1/2012 — \"Leave the admin out of the app.\" Documented here for the web conversion, where it becomes a real admin screen.",
    "xxEditPackagingData": "Unreachable in the legacy UI:</strong> the <span class=\"mono\">editPackagingDataToolStripMenuItem_Click</span> hook in MDIParent1 is commented out — no menu path reaches this editor. Documented here for the web conversion.",
}

def screen_page(form, blurb, rows):
    dead = DEAD_UI_NOTES.get(form)
    dead_note = f'<div class="note"><strong>{dead}</div>' if dead else ''
    table = "\n".join(
        f'      <tr><td class="mono">{html.escape(n)}</td><td class="mono">{html.escape(c)}</td>'
        f'<td>{html.escape(lb)}</td></tr>'
        for n, c, lb in rows
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(form)} — Unit Claiming viz wireframe</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f5e8a'/%3E%3Ctext x='32' y='42' font-size='28' text-anchor='middle' fill='white' font-family='sans-serif'%3EV%3C/text%3E%3C/svg%3E">
<style>{PAGE_CSS}</style>
</head>
<body>
<nav class="crumb"><a href="./index.html">viz index</a> &rsaquo; {html.escape(form)}</nav>
<div class="eyebrow">Unit Claiming &middot; wave-1 UI wireframe (branch experiment)</div>
<h1>{html.escape(form)}</h1>
<p>{html.escape(blurb)}</p>{dead_note}
<div class="note"><strong>Scope:</strong> UI understanding only. Control inventory parsed from
<span class="mono">{html.escape(form)}.Designer.cs</span> ({len(rows)} controls). API / data-layer mapping deferred to wave 2.
<!-- wave-2: api-layer --></div>
<div class="note">Opens as a maximized MDI child of <span class="mono">MDIParent1</span> (prior child closed). Return via the crumb above.</div>
<h2>Controls ({len(rows)})</h2>
<table>
<thead><tr><th>Name</th><th>Type</th><th>Label</th></tr></thead>
<tbody>
{table}
</tbody>
</table>
<footer class="src"><strong>Source grounding:</strong>
<span class="mono">ref-code-20260904/UnitClaimingUI/{html.escape(form)}.cs</span> +
<span class="mono">ref-code-20260904/UnitClaimingUI/{html.escape(form)}.Designer.cs</span>.
Designer inventory is authoritative for fields; behavior notes verified against the <span class="mono">.cs</span> code-behind.</footer>
</body>
</html>
"""

def index_page(nav_edges, form_counts):
    rows = "\n".join(
        f'      <tr><td><a href="./{f}.html">{f}</a></td><td class="mono">{src}</td>'
        f'<td>{c} controls</td><td>{html.escape(b)}</td></tr>'
        for (f, b), c, src in form_counts
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Unit Claiming — viz wireframe overview</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f5e8a'/%3E%3Ctext x='32' y='42' font-size='28' text-anchor='middle' fill='white' font-family='sans-serif'%3EV%3C/text%3E%3C/svg%3E">
<style>{PAGE_CSS}
  .hero {{ background: var(--surface); border: 2px solid var(--primary); border-radius: .8rem;
    padding: 2rem 1.5rem; margin: 1.5rem 0; text-align: center; }}
  .hero h2 {{ border: none; margin: 0 0 .5rem; font-size: 1.5rem; }}
  .hero .cta {{ display: inline-block; margin-top: 1rem; padding: .8rem 2rem; border-radius: .5rem;
    background: var(--primary); color: #fff; text-decoration: none; font-weight: 700; font-size: 1.1rem; }}
  .diagram-shell {{ background: var(--surface); border: 1px solid var(--border); border-radius: .6rem; padding: 1rem; }}
  .mermaid-wrap {{ position: relative; }}
  .zoom-controls {{ display: flex; gap: .4rem; margin-bottom: .5rem; }}
  .zoom-controls button {{ font-size: .8rem; padding: .25rem .6rem; cursor: pointer; }}
  .mermaid-viewport {{ overflow: auto; max-height: 96rem; min-height: 40rem; border: 1px solid var(--border); border-radius: .4rem; }}
  .mermaid-canvas {{ min-height: 12rem; padding: 1rem; }}
  .mermaid-canvas svg {{ max-width: none !important; }}
</style>
</head>
<body>
<nav class="crumb"><a href="../index.html">wireframe-host gallery</a> &rsaquo; viz</nav>
<div class="eyebrow">Unit Claiming &middot; wave-1 UI wireframe (branch experiment)</div>
<h1>Unit Claiming — wireframe overview</h1>
<p>Branch-experiment rebuild of the legacy WinForms UI as self-contained wireframe pages.
Wave 1 covers UI only; API mapping deferred.
<!-- wave-2: api-layer --></p>
<div class="hero">
<h2>Start here: the Main Menu</h2>
<p>Every flow in this spec opens from the app front door — click any button.</p>
<a class="cta" href="./wizard/main-menu.html">Open the Main Menu &rsaquo;</a>
</div>
<h2>Standard wizard click-through</h2>
<p><a href="./wizard/01-employee-auth.html">Start the Standard wizard walkthrough &rsaquo;</a>
(Employee Auth &rarr; Part Number &rarr; Serial &rarr; Pallet Qty &rarr; Skid Weight &rarr; Complete).
CSS mockups with Prev/Next wired per the real nav rules.</p>
<h2>Wizard variation click-throughs</h2>
<table>
<thead><tr><th>Variation</th><th>Steps</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><a href="./wizard/01-employee-auth.html">Standard — Unit Claiming</a></td><td class="mono">6</td><td>Core flow; conditional license-plate + returnable-type branches linked from steps 2–4.</td></tr>
<tr><td><a href="./wizard/reprint/01-employee-auth.html">Standard Reprint</a></td><td class="mono">3</td><td>History mode — nothing saved to the DB.</td></tr>
<tr><td><a href="./wizard/boxlabel/01-employee-auth.html">Box Label</a></td><td class="mono">5</td><td>Quantity before serial.</td></tr>
<tr><td><a href="./wizard/lowvolume/01-employee-auth.html">Low Volume Claiming</a></td><td class="mono">6</td><td>Includes conditional license-plate step.</td></tr>
<tr><td><a href="./wizard/kit/01-employee-auth.html">Kit Claiming (All Plants)</a></td><td class="mono">5</td><td>FAS-cell resolution after part number.</td></tr>
<tr><td><a href="./wizard/machine/01-employee-auth.html">Print Machine Number</a></td><td class="mono">3</td><td>Single-purpose label flow.</td></tr>
<tr><td><a href="./wizard/location/01-employee-auth.html">Location Label (Princeton)</a></td><td class="mono">3</td><td>Single-purpose label flow.</td></tr>
<tr><td><a href="./wizard/combo/01-employee-auth.html">Combo Skid</a></td><td class="mono">7</td><td>Two-skid loop; chain shows one skid pass.</td></tr>
</tbody>
</table>
<h2>Standalone screens</h2>
<table>
<thead><tr><th>Screen</th><th>What</th></tr></thead>
<tbody>
<tr><td><a href="./screens/leaking/01-employee.html">HGP Leaking Housing Label walkthrough</a></td><td>4-step label flow: Employee → Model → Qty → Complete.</td></tr>
<tr><td><a href="./screens/washed/claiming/01-employee.html">Washed/Leak Tested (Claiming) walkthrough</a></td><td>Employee, Serial, Qty, Complete + Non-HG Model/Qty/Lot branch. Disabled in legacy UI; live for the conversion.</td></tr>
<tr><td><a href="./screens/washed/reprint/01-employee.html">Washed/Leak Tested (Reprint) walkthrough</a></td><td>Employee, Serial, Complete. W-suffix serials; reprints the existing label.</td></tr>
<tr><td><a href="./screens/view-data.html">View Claiming Data</a></td><td>Skid grid + paging + plant filters, incl. <a href="./screens/view-data-popup.html">Edit Claimed Qty dialog</a>.</td></tr>
<tr><td><a href="./screens/import-mtms.html">Import Units from MTMS</a></td><td>Import button + results log.</td></tr>
<tr><td><a href="./screens/configuration.html">Configure settings</a></td><td>Full settings mockup: Plant, Printing, Scale, IP groups.</td></tr>
<tr><td><a href="./screens/error-detail.html">Error Detail dialog</a></td><td>Exception text viewer.</td></tr>
<tr><td><a href="./screens/tolerance-factor.html">Set Tolerance Factor (unreachable)</a></td><td>Dead admin dialog, documented for conversion.</td></tr>
<tr><td><a href="./screens/edit-packaging.html">Edit Packaging Data (unreachable)</a></td><td>Dead editor, documented for conversion.</td></tr>
</tbody>
</table>
<h2>Screen inventory</h2>
<table>
<thead><tr><th>Screen</th><th>Source</th><th>Inventory</th><th>Notes</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<footer class="src"><strong>Source grounding:</strong>
<span class="mono">ref-code-20260904/UnitClaimingUI/MDIParent1.cs</span> (Show* nav map) +
per-screen <span class="mono">.cs</span> / <span class="mono">.Designer.cs</span>. Existing excalidraw gallery untouched.</footer>
</body>
</html>
"""

def main():
    OUT.mkdir(exist_ok=True)
    nav = [
        ("MDI", "startup: loads", "MainMenu"),
        ("MainMenu", "claiming buttons", "UnitClaimingMainForm"),
        ("MainMenu", "btnWashedLeakTested", "WashedLeakTestedLabel"),
        ("MainMenu", "btnLeakingHousingLabel", "LeakingHousingLabel"),
        ("MDI", "menu: View Data", "ViewUnitClaimingData"),
        ("MDI", "menu: Import Units from MTMS", "ImportFromMTMS"),
        ("MDI", "menu: Configure", "Configuration"),
        ("ViewUnitClaimingData", "row detail", "ViewUnitClaimingDataPopup"),
        ("MDI", "various callers", "SetToleranceFactor"),
        ("MDI", "error path", "ErrorDetail"),
        ("MDI", "disabled menu hook", "xxEditPackagingData"),
    ]
    counts = []
    for form, blurb in FORMS:
        rows = parse_designer(form)
        src = f"UnitClaimingUI/{form}.Designer.cs" if (SRC / f"{form}.Designer.cs").exists() else "no Designer.cs (code-only)"
        counts.append(((form, blurb), len(rows), src))
        (OUT / f"{form}.html").write_text(screen_page(form, blurb, rows))
        print(f"{form}: {len(rows)} controls")
    (OUT / "index.html").write_text(index_page(nav, counts))
    print("wrote", OUT / "index.html")

if __name__ == "__main__":
    main()
