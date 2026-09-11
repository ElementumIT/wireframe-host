"""Scratch generator for viz wizard click-throughs. Redundancy-is-fine:
every page fully self-contained. Not committed. Run: python3 /tmp/wizard_gen.py"""
import pathlib

OUT = pathlib.Path("/home/ubuntu/wireframe-host/viz/wizard")

CSS = """
  html { font-size: 16px; }
  :root {
    --bg: #f4f1ea; --surface: #ffffff; --border: rgba(20,40,70,.12);
    --text: #1c2b3a; --text-dim: #5b6b7c;
    --primary: #0f5e8a; --primary-dim: rgba(15,94,138,.08);
    --accent: #b3541e; --ok: #1e7e46;
    --mono: 'Fragment Mono','SF Mono',Consolas,monospace;
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
         max-width: 72rem; margin: 0 auto; padding: 2rem 1.5rem; font-size: 1rem; line-height: 1.5; }
  h1 { font-size: 1.6rem; margin: 0 0 .25rem; }
  .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; color: var(--text-dim); }
  nav.crumb { margin-bottom: 1.25rem; font-size: .9rem; }
  nav.crumb a { color: var(--primary); }
  .steps { display: flex; gap: .4rem; margin: 1rem 0 1.5rem; flex-wrap: wrap; }
  .steps a, .steps span { padding: .35rem .7rem; border: 1px solid var(--border); border-radius: 2rem;
    font-size: .8rem; text-decoration: none; color: var(--text-dim); background: var(--surface); }
  .steps .cur { background: var(--primary); color: #fff; border-color: var(--primary); font-weight: 600; }
  .steps .done { color: var(--primary); border-color: var(--primary); }
  .mock { display: grid; grid-template-columns: 1fr 1.4fr; gap: 1rem; }
  @media (max-width: 60rem) { .mock { grid-template-columns: 1fr; } }
  .panel { background: var(--surface); border: 1px solid var(--border); border-radius: .6rem; padding: 1.25rem 1.4rem; }
  .panel h2 { font-size: 1.15rem; margin: 0 0 .8rem; border-bottom: 2px solid var(--primary); padding-bottom: .35rem; }
  .field { margin: .8rem 0; }
  .field label { display: block; font-size: .85rem; color: var(--text-dim); margin-bottom: .3rem; }
  .field input[type=text] { width: 100%; font-size: 1.1rem; padding: .55rem .7rem;
    border: 2px solid var(--primary); border-radius: .4rem; background: var(--bg); color: var(--text); }
  .field select { width: 100%; font-size: 1.05rem; padding: .55rem .7rem;
    border: 2px solid var(--primary); border-radius: .4rem; background: var(--bg); color: var(--text); }
  .sample { border: 1px dashed var(--border); border-radius: .4rem; padding: .6rem .8rem; margin-top: .8rem; font-size: .85rem; }
  .sample .mono { font-family: var(--mono); }
  .hint { font-size: .82rem; color: var(--text-dim); margin-top: .5rem; }
  .summary { display: grid; grid-template-columns: auto 1fr; gap: .35rem .9rem; font-size: .9rem; }
  .summary dt { color: var(--text-dim); } .summary dd { margin: 0; font-family: var(--mono); font-size: .85rem; }
  .navbtns { display: flex; gap: .8rem; margin-top: 1.5rem; }
  .navbtns a { padding: .7rem 1.6rem; border-radius: .45rem; text-decoration: none; font-weight: 600; }
  .prev { border: 2px solid var(--primary); color: var(--primary); }
  .next { background: var(--primary); color: #fff; }
  .disabled { opacity: .35; pointer-events: none; }
  .note { background: var(--primary-dim); border-left: 4px solid var(--primary);
          padding: .7rem 1rem; border-radius: 0 .5rem .5rem 0; margin: .8rem 0; font-size: .9rem; }
  footer.src { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border);
               font-size: .82rem; color: var(--text-dim); }
  .btnrow { display: flex; gap: .6rem; margin-top: .8rem; flex-wrap: wrap; }
  .btnrow button { padding: .55rem 1.1rem; border-radius: .4rem; border: 2px solid var(--primary);
    background: var(--surface); color: var(--primary); font-weight: 600; cursor: pointer; }
  .diagram-shell { background: var(--surface); border: 1px solid var(--border); border-radius: .6rem; padding: 1rem; margin: 1rem 0; }
  .mermaid-wrap { position: relative; }
  .zoom-controls { display: flex; gap: .4rem; margin-bottom: .5rem; }
  .zoom-controls button { font-size: .8rem; padding: .25rem .6rem; cursor: pointer; }
  .mermaid-viewport { overflow: auto; max-height: 24rem; border: 1px solid var(--border); border-radius: .4rem; }
  .mermaid-canvas { min-height: 6rem; padding: .5rem; }
  .mermaid-canvas svg { max-width: none !important; }
"""

RIGHT_PANEL = """
    <div class="panel"><h2>Skid summary (live)</h2>
      <dl class="summary">
        <dt>Employee Badge #:</dt><dd class="ebadge">{badge}</dd>
        <dt>Model #:</dt><dd>{model}</dd>
        <dt>Pallet Id:</dt><dd>{pallet}</dd>
        <dt>Pallet Qty / Claimed:</dt><dd>{qty}</dd>
        <dt>Unit Weight:</dt><dd>{unitw}</dd>
        <dt>Packaging Mat. Wt:</dt><dd>{pkgw}</dd>
        <dt>Est. Skid Wt (no top):</dt><dd>{est}</dd>
        <dt>Actual Skid Weight:</dt><dd>{actual}</dd>
        <dt>Variance Allowed:</dt><dd>{var}</dd>
        <dt>FAS Cell:</dt><dd>{fas}</dd>
      </dl>
      <div class="btnrow"><button type="button">Print Labels</button></div>
      <p class="hint">Double-clicking a value jumps back to its step (SkipToCollectionStep).</p>
    </div>"""

FULL = dict(badge="11111", model="M100-A", pallet="P-00412", qty="40 / 40",
            unitw="2.50", pkgw="18.0", est="118.0", actual="118.4", var="± 1.25", fas="FAS-G1")
GROW = dict(badge="11111", model="M100-A", pallet="P-00412", qty="40 / 12",
            unitw="2.50", pkgw="18.0", est="118.0", actual="—", var="± 1.25", fas="FAS-G1")
EARLY = dict(badge="11111", model="—", pallet="—", qty="—", unitw="—", pkgw="—",
             est="—", actual="—", var="—", fas="—")
MID = dict(badge="11111", model="M100-A", pallet="—", qty="—", unitw="2.50", pkgw="18.0",
           est="—", actual="—", var="—", fas="—")

LIB = {
 "employee-auth": dict(title="Employee Authorization", src="UserControls/EmployeeAuthorization.cs",
   left="""
    <div class="panel"><h2>Scan badge</h2>
      <div class="field"><label>Scan your employee badge</label><input type="text" placeholder="_____"></div>
      <p class="hint">(Use 11111 for testing)</p>
      <div class="note">Any 5-digit integer passes (2/24/2015 decision); unknown badges get default User rights, no Admin, no keyboard entry.</div>
    </div>""",
   summ=EARLY,
   note="Previous disabled on the first step (source: PrepareForm). Badge expiry re-routes here from any step."),
 "part-number": dict(title="Part Number", src="UserControls/PartNumber.cs",
   left="""
    <div class="panel"><h2>Scan part</h2>
      <div class="field"><label>Scan the unit part number or 2D barcode</label><input type="text" placeholder="M100-A"></div>
      <div class="sample"><strong>Sample Part #'s (for testing)</strong><br><span class="mono">M100-A &middot; KIT-9 &middot; …</span></div>
      <div class="field"><label><input type="checkbox"> Flag this as a Product Monitoring Unit</label></div>
    </div>""",
   summ=EARLY,
   note="Part not found shows the 'Part/Model Number not found' error state."),
 "serial-number": dict(title="Serial Number", src="UserControls/SerialNumber.cs",
   left="""
    <div class="panel"><h2>Scan serial</h2>
      <div class="field"><label>Scan the serial number from the unit label</label><input type="text" placeholder="7159D60100"></div>
      <div class="sample"><strong>Sample Serial #'s (for testing)</strong><br><span class="mono">7159D60100 &middot; …</span></div>
      <div class="note">Invalid format shows 'This is an invalid serial number.' Next is blocked until valid (IsValid gate).</div>
    </div>""",
   summ=MID,
   note="Serial decoded for julian production date + line code in the real app; the mock shows the scan state."),
 "pallet-quantity": dict(title="Pallet Quantity", src="UserControls/PalletQuantity.cs",
   left="""
    <div class="panel"><h2>Enter quantity</h2>
      <div class="field"><label>Scan the pallet quantity for this part</label><input type="text" placeholder="40"></div>
    </div>""",
   summ=GROW,
   note="IsPartialClaim resets to No on arrival at this step."),
 "skid-weight": dict(title="Skid Weight", src="UserControls/SkidWeight.cs",
   left="""
    <div class="panel"><h2>Weigh skid</h2>
      <div class="field"><label>Enter in the skid weight</label><input type="text" placeholder="118.4"></div>
      <div class="btnrow"><button type="button">Re-read scale</button></div>
      <div class="field"><label><input type="checkbox"> Partial Claim</label></div>
      <p><strong>Wood Pallet Weight:</strong> <span class="mono">18.0</span> &nbsp; <strong>Claim:</strong> <span class="mono">40 × 2.50</span></p>
      <div class="note">Manual entry allowed only where the machine is configured for it; otherwise the scale feed fills the field.</div>
    </div>""",
   summ=dict(badge="11111", model="M100-A", pallet="P-00412", qty="40 / 40", unitw="2.50",
             pkgw="18.0", est="118.0", actual="118.4", var="± 1.25", fas="FAS-G1"),
   note="Weight variance = Unit Weight × Tolerance Factor; outside variance blocks completion."),
 "skid-complete": dict(title="Skid Complete", src="UserControls/SkidDataEntryComplete.cs",
   left="""
    <div class="panel"><h2>Skid complete</h2>
      <p><strong>Skid P-00412 claimed.</strong> Labels print per configuration; the run is saved and the form resets for the next skid.</p>
      <div class="note">Next is <strong>disabled</strong> on this step (source: PrepareForm). Restart re-enters at Step 1 (AfterSave → Form1_Load).</div>
    </div>""",
   summ=FULL,
   note="Completion state; save happens via the PalletInfoDisplay panel before arrival here."),
 "license-plate": dict(title="Skid ID from License Plate", src="UserControls/SkidIdFromLicensePlate.cs",
   left="""
    <div class="panel"><h2>Scan license plate</h2>
      <div class="field"><label>Scan the Skid Id from the Skid License Plate</label><input type="text" placeholder="Skid Id"></div>
      <div class="btnrow"><button type="button">Generate New Skid Id</button></div>
      <div class="note">Conditional branch: reached only when the part uses 2D labels and a license-plate skid id is required (SkidLicensePlateWiz). Otherwise the flow skips straight past this step.</div>
    </div>""",
   summ=MID,
   note="Branch step — not on the default path. Reached after Part Number (2D label + plate required) and again after Serial; the panel self-skips when no plate is required. Shown here so the click-through covers it."),
 "returnable-type": dict(title="Returnable Type", src="UserControls/ReturnableType.cs",
   left="""
    <div class="panel"><h2>Select returnable type</h2>
      <div class="field"><label>Select the returnable type:</label>
      <select><option>— choose —</option><option>Wood pallet</option><option>Plastic pallet</option><option>Slip sheet</option></select></div>
      <div class="note">Reached only when multiple pallet-type options exist; with a single option the flow skips to Skid Weight. A choice is required to continue.</div>
    </div>""",
   summ=GROW,
   note="Branch step — backing out here clears the weight (2/18/2016 workflow fix)."),
 "fascell": dict(title="FAS Cell", src="UserControls/FasCell.cs",
   left="""
    <div class="panel"><h2>Select FAS cell</h2>
      <div class="field"><label>Select the FAS Cell</label>
      <select><option>— choose —</option><option>FAS-G1</option><option>FAS-G2</option></select></div>
      <div class="note">Unconfigured part numbers show 'No FAS Cell has been configured for this part number.'</div>
    </div>""",
   summ=MID,
   note="Kit-claiming step: resolves the production-line code from the serial via ProductionLineCodeInfo."),
 "machine-number": dict(title="Machine Number", src="UserControls/MachineNumber.cs",
   left="""
    <div class="panel"><h2>Enter machine number</h2>
      <div class="field"><label>Enter the machine number</label><input type="text" placeholder="M-042"></div>
    </div>""",
   summ=EARLY,
   note="Single-purpose flow: badge, machine number, done — prints the machine-number label."),
 "location": dict(title="Location", src="UserControls/Location.cs",
   left="""
    <div class="panel"><h2>Enter location</h2>
      <div class="field"><label>Enter in the location to be printed on the label.</label><input type="text" placeholder="PRINCETON-A12"></div>
    </div>""",
   summ=EARLY,
   note="Single-purpose flow: badge, location, done — prints the Princeton location label."),
}

# Legacy flat-file Standard flow (live links preserved).
FLAT_STANDARD = [
    ("01-employee-auth.html", "employee-auth", True, "02-part-number.html", "Next →"),
    ("02-part-number.html", "part-number", False, "03-serial-number.html", "Next →"),
    ("03-serial-number.html", "serial-number", False, "04-pallet-quantity.html", "Next →"),
    ("04-pallet-quantity.html", "pallet-quantity", True, "05-skid-weight.html", "Next →"),
    ("05-skid-weight.html", "skid-weight", False, "06-skid-complete.html", "Next →"),
    ("06-skid-complete.html", "skid-complete", False, "01-employee-auth.html", "Start new skid →"),
]
FLAT_NAMES = ["Employee Auth", "Part Number", "Serial Number", "Pallet Qty", "Skid Weight", "Complete"]

VARIATIONS = {
 "reprint": dict(header="Unit Claiming (Reprint)", blurb="History-mode reprint: nothing is saved to the DB.",
   chain=["employee-auth", "serial-number", "skid-complete"],
   names=["Employee Auth", "Serial Number", "Complete"],
   prev_off={0}, final_label="Start new reprint →"),
 "boxlabel": dict(header="Box Label", blurb="Box-label flow: quantity before serial.",
   chain=["employee-auth", "part-number", "pallet-quantity", "serial-number", "skid-complete"],
   names=["Employee Auth", "Part Number", "Pallet Qty", "Serial Number", "Complete"],
   prev_off={0}, final_label="Start new box label →"),
 "lowvolume": dict(header="Low Volume Claiming", blurb="Low-volume flow with conditional license-plate branch.",
   chain=["employee-auth", "part-number", "license-plate", "serial-number", "pallet-quantity", "skid-complete"],
   names=["Employee Auth", "Part Number", "License Plate*", "Serial Number", "Pallet Qty", "Complete"],
   prev_off={0}, final_label="Start new claim →"),
 "kit": dict(header="Kit Claiming (All Plants)", blurb="Kit flow: FAS-cell resolution after part number.",
   chain=["employee-auth", "part-number", "fascell", "pallet-quantity", "skid-complete"],
   names=["Employee Auth", "Part Number", "FAS Cell", "Pallet Qty", "Complete"],
   prev_off={0}, final_label="Start new kit →"),
 "machine": dict(header="Print Machine Number", blurb="Single-purpose machine-number label flow.",
   chain=["employee-auth", "machine-number", "skid-complete"],
   names=["Employee Auth", "Machine Number", "Complete"],
   prev_off={0}, final_label="Print another →"),
 "location": dict(header="Location Label (Princeton)", blurb="Single-purpose Princeton location-label flow.",
   chain=["employee-auth", "location", "skid-complete"],
   names=["Employee Auth", "Location", "Complete"],
   prev_off={0}, final_label="Print another →"),
 "combo": dict(header="Unit Claiming - Combo Skid", blurb="Two-skid loop: the chain below is one skid pass; the app repeats it for skid 2, then weighs once.",
   chain=["employee-auth", "part-number", "pallet-quantity", "license-plate", "serial-number", "skid-weight", "skid-complete"],
   names=["Employee Auth", "Part Number", "Pallet Qty", "License Plate", "Serial Number", "Skid Weight", "Complete"],
   prev_off={0}, final_label="Start new combo →"),
}

def mermaid_strip(chain, names, cur):
    nodes = "\n".join(f"    T{j+1}[{nm}]" for j, nm in enumerate(names))
    links = " --> ".join(f"T{j+1}" for j in range(len(chain)))
    hl = f"    style T{cur} fill:#0f5e8a,color:#fff" if cur and 1 <= cur <= len(chain) else ""
    clicks = "\n".join(f'    click T{j+1} "./{j+1:02d}-{s}.html" "Open step"' for j, s in enumerate(chain))
    return f"""<div class="diagram-shell"><div class="mermaid-wrap">
<div class="zoom-controls"><button data-z="in">+</button><button data-z="out">&minus;</button><button data-z="reset">reset</button></div>
<div class="mermaid-viewport"><div class="mermaid-canvas flowmini">
<pre class="mermaid">
flowchart LR
{nodes}
    {links}
{hl}
{clicks}
</pre>
</div></div></div></div>"""

def render(num, total, title, header, blurb, left, summ, src, note,
           crumbs, prev_href, prev_off, next_href, next_label, home="../index.html", up="../",
           chain=None, names=None):
    dots = []
    for j, (nm, href) in enumerate(crumbs):
        dots.append(f'<span class="cur">{j+1}. {nm}</span>' if j == num - 1
                    else f'<a class="done" href="{href}">{j+1}. {nm}</a>')
    prev = (f'<a class="prev" href="{prev_href}">← Previous</a>'
            if prev_href and not prev_off else '<a class="prev disabled">← Previous</a>')
    strip = mermaid_strip(chain, names, num) if chain and names else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {header} ({num} / {total})</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f5e8a'/%3E%3Ctext x='32' y='42' font-size='28' text-anchor='middle' fill='white' font-family='sans-serif'%3EW%3C/text%3E%3C/svg%3E">
<style>{CSS}</style>
</head>
<body>
<nav class="crumb"><a href="{home}">viz index</a> &rsaquo; <a href="{up}UnitClaimingMainForm.html">UnitClaimingMainForm</a> &rsaquo; {header}</nav>
<div class="eyebrow">Unit Claiming &middot; {header} &middot; step {num} / {total}</div>
<h1>Step {num} — {title}</h1>
<p>{blurb}</p>
<div class="steps">
{''.join(dots)}
</div>
{strip}
<div class="mock">
{left}
{RIGHT_PANEL.format(**summ)}
</div>
<div class="note">{note}</div>
<div class="navbtns">
{prev}
<a class="next" href="{next_href}">{next_label}</a>
</div>
<footer class="src"><strong>Source grounding:</strong>
<span class="mono">ref-code-20260904/UnitClaimingUI/{src}</span> (step panel) +
<span class="mono">UnitClaimingMainForm.cs PrepareForm/btnNext_Click</span> (nav rules) +
<span class="mono">UnitClaimingMainFormController.DataCollectionSteps</span> (sequence).
Wireframe only — inputs do not validate or save.</footer>
<script type="importmap">{{"imports": {{"mermaid": "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"}}}}</script>
<script type="module">
import mermaid from 'mermaid';
mermaid.initialize({{ startOnLoad: true, theme: 'base', themeVariables: {{ primaryColor: '#0f5e8a', fontSize: '15px' }} }});
document.querySelectorAll('.flowmini').forEach(cv => {{
  let z = 1.2, tries = 0;
  const apply = () => {{
    const svg = cv.querySelector('svg');
    if (svg) {{ svg.style.transform = `scale(${{z}})`; svg.style.transformOrigin = 'top left'; return true; }}
    return false;
  }};
  const ready = setInterval(() => {{ if (apply() || ++tries > 40) clearInterval(ready); }}, 250);
  cv.closest('.mermaid-wrap').querySelectorAll('.zoom-controls button').forEach(b => b.addEventListener('click', () => {{
    const k = b.dataset.z;
    z = k === 'in' ? Math.min(z + .2, 3) : k === 'out' ? Math.max(z - .2, .4) : 1.2;
    apply();
  }}));
}});
</script>
</body>
</html>"""

def main_menu_hub():
    btn = lambda label, href: f'<a class="mbtn" href="{href}">{label}</a>'
    dis = lambda label: f'<span class="mbtn off">{label}</span>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Main Menu — wizard hub</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f5e8a'/%3E%3Ctext x='32' y='42' font-size='28' text-anchor='middle' fill='white' font-family='sans-serif'%3EM%3C/text%3E%3C/svg%3E">
<style>{CSS}
  .menustrip {{ display: flex; gap: 0; background: var(--surface); border: 1px solid var(--border);
    border-radius: .5rem; overflow: hidden; margin-bottom: 1.25rem; flex-wrap: wrap; }}
  .menustrip a {{ padding: .6rem 1.1rem; text-decoration: none; color: var(--text); font-size: .9rem;
    border-right: 1px solid var(--border); }}
  .menustrip a:hover {{ background: var(--primary-dim); }}
  .btngrid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr)); gap: .8rem; }}
  .mbtn {{ display: block; padding: 1rem; text-align: center; background: var(--primary); color: #fff;
    border-radius: .5rem; text-decoration: none; font-weight: 600; }}
  .mbtn.off {{ background: var(--surface); color: var(--text-dim); border: 2px dashed var(--border);
    pointer-events: none; }}
  .washed {{ border: 2px solid var(--border); border-radius: .6rem; padding: 1rem; margin-top: 1rem; }}
  .washed h3 {{ margin: 0 0 .2rem; font-size: .95rem; color: var(--text-dim); }}
</style>
</head>
<body>
<nav class="crumb"><a href="../index.html">viz index</a> &rsaquo; Main Menu</nav>
<div class="eyebrow">Unit Claiming &middot; main menu (entry point)</div>
<h1>Main Menu</h1>
<p>Opened at startup via <span class="mono">ShowMainMenu</span>. Every button below opens its flow — click through.</p>
<div class="menustrip">
<a href="../screens/view-data.html">View Data</a>
<a href="../screens/import-mtms.html">Import Units from MTMS</a>
<a href="../screens/configuration.html">Configure</a>
</div>
<div class="btngrid">
{btn("Unit Claiming", "./01-employee-auth.html")}
{btn("Low Volume Claiming", "./lowvolume/01-employee-auth.html")}
{btn("Box Label", "./boxlabel/01-employee-auth.html")}
{btn("Unit Claiming - Combo Skid", "./combo/01-employee-auth.html")}
{btn("Print Machine Number", "./machine/01-employee-auth.html")}
{btn("Location Label (Princeton)", "./location/01-employee-auth.html")}
{btn("HGP Leaking Housing Label", "../LeakingHousingLabel.html")}
{btn("Kit Claiming (All Plants)", "./kit/01-employee-auth.html")}
{btn("Unit Claiming Reprint", "./reprint/01-employee-auth.html")}
</div>
<div class="washed"><h3>Disabled 6/8/2026</h3>
<div class="btngrid">
{dis("Washed/Leak Tested Label")}
{dis("Washed/Leak Tested Label (Reprint)")}
</div>
<p class="hint">I.T. suspects these buttons are no longer used (<span class="mono">Visible = false</span> in source). If re-enabled, they open the Washed/Leak Tested form — walk it anyway: <a href="../screens/washed/claiming/01-employee.html">Claiming walkthrough</a> + <a href="../screens/washed/reprint/01-employee.html">Reprint walkthrough</a> (spec: <a href="../WashedLeakTestedLabel.html">inventory</a>).</p>
</div>
<footer class="src"><strong>Source grounding:</strong>
<span class="mono">ref-code-20260904/UnitClaimingUI/MainMenu.cs</span> (button → ShowUnitClaiming variation wiring) +
<span class="mono">MainMenu.Designer.cs</span> (13 controls, washed pair hidden).
Wireframe only — buttons navigate, nothing saves.</footer>
</body>
</html>"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "main-menu.html").write_text(main_menu_hub())
    print("wrote main-menu.html")
    # Legacy flat Standard pages (live links preserved).
    n = len(FLAT_STANDARD)
    flat_chain = [s for _, s, _, _, _ in FLAT_STANDARD]
    for k, (fname, slug, poff, nxt, nlabel) in enumerate(FLAT_STANDARD):
        d = LIB[slug]
        crumbs = [(FLAT_NAMES[j], f) for j, (f, _, _, _, _) in enumerate(FLAT_STANDARD)]
        prev = FLAT_STANDARD[k-1][0] if k > 0 else None
        extra = ""
        if slug == "employee-auth":
            extra = ' No-rights badges land on the <a href="../screens/denied-access.html">Denied Access</a> state (rare since the 2015 default-rights decision).'
        if slug == "part-number":
            extra = ' <a href="./branch-license-plate.html">Conditional branch: 2D label + license-plate required → Skid ID from License Plate.</a>'
        if slug == "pallet-quantity":
            extra = ' Previous is <strong>disabled</strong> here in the Standard variation (helpdesk 84304, 7/3/2023). <a href="./branch-returnable-type.html">Multiple pallet-type options → Returnable Type.</a>'
        (OUT / fname).write_text(render(k+1, n, d["title"], "Unit Claiming", "Standard variation.",
            d["left"], d["summ"], d["src"], d["note"] + extra, crumbs, prev, poff, nxt, nlabel,
            chain=flat_chain, names=FLAT_NAMES))
        print("wrote", fname)
    # Conditional branch pages shared by Standard notes.
    for fname, slug in [("branch-license-plate.html", "license-plate"),
                        ("branch-returnable-type.html", "returnable-type")]:
        d = LIB[slug]
        crumbs = [(FLAT_NAMES[j], f) for j, (f, _, _, _, _) in enumerate(FLAT_STANDARD)]
        (OUT / fname).write_text(render(0, n, d["title"], "Unit Claiming (branch step)",
            "Conditional Standard branch — returns to the main chain after this step.",
            d["left"], d["summ"], d["src"], d["note"], crumbs,
            "02-part-number.html", False, "03-serial-number.html", "Continue →",
            chain=flat_chain, names=FLAT_NAMES))
        print("wrote", fname)
    # Per-variation folders.
    for var, v in VARIATIONS.items():
        vd = OUT / var
        vd.mkdir(exist_ok=True)
        chain = v["chain"]
        t = len(chain)
        for k, slug in enumerate(chain):
            d = LIB[slug]
            fn = f"{k+1:02d}-{slug}.html"
            crumbs = [(v["names"][j], f"{j+1:02d}-{s}.html") for j, s in enumerate(chain)]
            prev = f"{k:02d}-{chain[k-1]}.html" if k > 0 else None
            is_last = k == t - 1
            nxt = f"{1:02d}-{chain[0]}.html" if is_last else f"{k+2:02d}-{chain[k+1]}.html"
            nlabel = v["final_label"] if is_last else "Next →"
            poff = (k in v["prev_off"]) or (slug == "pallet-quantity" and var in ("standard",))
            (vd / fn).write_text(render(k+1, t, d["title"], v["header"], v["blurb"],
                d["left"], d["summ"], d["src"], d["note"], crumbs, prev, poff, nxt, nlabel,
                home="../../index.html", up="../../", chain=chain, names=v["names"]))
        print("wrote", var, t, "pages")

if __name__ == "__main__":
    main()
