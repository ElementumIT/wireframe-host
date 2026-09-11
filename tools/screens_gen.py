"""Scratch generator for viz standalone screens + label-flow click-throughs.
Redundancy-is-fine: self-contained pages. Run: python3 /tmp/screens_gen.py"""
import pathlib

OUT = pathlib.Path("/home/ubuntu/wireframe-host/viz/screens")

CSS = (pathlib.Path(__file__).parent / "wizard_css.txt").read_text()

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f5e8a'/%3E%3Ctext x='32' y='42' font-size='28' text-anchor='middle' fill='white' font-family='sans-serif'%3ES%3C/text%3E%3C/svg%3E">
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>"""

CRUMB = '<nav class="crumb"><a href="../index.html">viz index</a> &rsaquo; {here}</nav>'
FOOT = """<footer class="src"><strong>Source grounding:</strong> <span class="mono">ref-code-20260904/UnitClaimingUI/{src}</span>{extra}. Wireframe only — inputs do not save.</footer>"""

def label_summary(emp="—", model="—", qty="—", serial="—", extra_rows=""):
    return f"""
    <div class="panel"><h2>Label preview (live)</h2>
      <dl class="summary">
        <dt>Employee Badge #:</dt><dd>{emp}</dd>
        <dt>Model #:</dt><dd>{model}</dd>
        <dt>Pallet Qty:</dt><dd>{qty}</dd>
        <dt>Serial #:</dt><dd>{serial}</dd>
        {extra_rows}
      </dl>
      <div class="btnrow"><button type="button">Print Label</button></div>
    </div>"""

def flow_page(num, total, header, title, blurb, left, summ_html, src, note,
              dots, prev_href, prev_off, next_href, next_label, up="../"):
    ds = []
    for j, (nm, href) in enumerate(dots):
        ds.append(f'<span class="cur">{j+1}. {nm}</span>' if j == num - 1
                  else f'<a class="done" href="{href}">{j+1}. {nm}</a>')
    prev = (f'<a class="prev" href="{prev_href}">← Previous</a>'
            if prev_href and not prev_off else '<a class="prev disabled">← Previous</a>')
    crumb = f'<nav class="crumb"><a href="{up}index.html">viz index</a> &rsaquo; {header}</nav>'
    body = f"""{crumb}
<div class="eyebrow">Unit Claiming &middot; {header} &middot; step {num} / {total}</div>
<h1>Step {num} — {title}</h1>
<p>{blurb}</p>
<div class="steps">
{''.join(ds)}
</div>
<div class="mock">
{left}
{summ_html}
</div>
<div class="note">{note}</div>
<div class="navbtns">
{prev}
<a class="next" href="{next_href}">{next_label}</a>
</div>
{FOOT.format(src=src, extra="")}
"""
    return HEAD.format(title=f"{title} — {header} ({num} / {total})", css=CSS, body=body)

def single_page(header, title, blurb, content, src, extra=""):
    body = f"""{CRUMB.format(here=header)}
<div class="eyebrow">Unit Claiming &middot; {header}</div>
<h1>{title}</h1>
<p>{blurb}</p>
{content}
{FOOT.format(src=src, extra=extra)}
"""
    return HEAD.format(title=f"{title} — {header}", css=CSS, body=body)

LEAK_STEPS = [
 ("employee", "Employee Number", "Scan Employee Number:", "tbEmployeeNumber",
  "Badges the operator into this label flow.", '<dt>Employee Badge #:</dt><dd>11111</dd>'),
 ("model", "Part Number", "Scan Part Number:", "tbModelNumber",
  "Model the labels print for.", '<dt>Employee Badge #:</dt><dd>11111</dd><dt>Model #:</dt><dd>M100-A</dd>'),
 ("qty", "Quantity", "Scan Quantity:", "tbQty",
  "How many labels to print.", '<dt>Employee Badge #:</dt><dd>11111</dd><dt>Model #:</dt><dd>M100-A</dd><dt>Pallet Qty:</dt><dd>40</dd>'),
 ("complete", "Complete", None, None,
  "Hit the Print Label button to print.", '<dt>Employee Badge #:</dt><dd>11111</dd><dt>Model #:</dt><dd>M100-A</dd><dt>Pallet Qty:</dt><dd>40</dd>'),
]
LEAK_NAMES = ["Employee", "Model", "Qty", "Complete"]

WASH_STEPS = [
 ("employee", "Employee Number", "Scan Employee Number:", "tbEmployeeNumber",
  "Badges the operator into this label flow.", dict(emp="11111")),
 ("serial", "Serial Number", "Scan Serial Number:", "tbSerialNumber",
  "HG serials resolve model + qty automatically; anything else takes the Non-HG branch.",
  dict(emp="11111", serial="7159D60100", model="M100-A", qty="40")),
 ("complete", "Complete", None, None,
  "Hit the Print Label button to print.", dict(emp="11111", serial="7159D60100", model="M100-A", qty="40")),
]
WASH_NAMES = ["Employee", "Serial", "Complete"]
WASH_NONHG = [
 ("model", "Part Number (Non-HG)", "Scan Part Number:", "tbModelNumber",
  "This step is only necessary for Non-Hydro-Gear labels.", dict(emp="11111", serial="EXT-0099")),
 ("qty", "Quantity (Non-HG)", "Scan Quantity:", "tbQty",
  "This step is only necessary for Non-Hydro-Gear labels.", dict(emp="11111", serial="EXT-0099", model="EXT-MOD", qty="10")),
 ("lot", "Lot (Non-HG)", "Scan Lot:", "tbLot",
  "This step is only necessary for Non-Hydro-Gear labels.", dict(emp="11111", serial="EXT-0099", model="EXT-MOD", qty="10", lot="L-77")),
]
WASH_NONHG_NAMES = ["Non-HG Model", "Non-HG Qty", "Non-HG Lot"]

def summ_html(d):
    rows = [f"<dt>Employee Badge #:</dt><dd>{d.get('emp', '—')}</dd>",
            f"<dt>Model #:</dt><dd>{d.get('model', '—')}</dd>",
            f"<dt>Pallet Qty:</dt><dd>{d.get('qty', '—')}</dd>",
            f"<dt>Serial #:</dt><dd>{d.get('serial', '—')}</dd>"]
    if "lot" in d:
        rows.append(f"<dt>Lot #:</dt><dd>{d['lot']}</dd>")
    return f"""
    <div class="panel"><h2>Label preview (live)</h2>
      <dl class="summary">
        {' '.join(rows)}
      </dl>
      <div class="btnrow"><button type="button">Print Label</button></div>
    </div>"""

def leak_left(slug, label, tb):
    if slug == "complete":
        return """
    <div class="panel"><h2>Done</h2>
      <p><strong>Hit the Print Label button to print.</strong></p>
    </div>"""
    return f"""
    <div class="panel"><h2>{label}</h2>
      <div class="field"><label>{label}</label><input type="text" placeholder="scan…"></div>
    </div>"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # --- Leaking Housing mini-wizard ---
    ld = OUT / "leaking"
    ld.mkdir(exist_ok=True)
    t = len(LEAK_STEPS)
    for k, (slug, title, label, tb, note, _) in enumerate(LEAK_STEPS):
        fn = f"{k+1:02d}-{slug}.html"
        dots = [(LEAK_NAMES[j], f"{j+1:02d}-{s}.html") for j, (s, _, _, _, _, _) in enumerate(LEAK_STEPS)]
        prev = f"{k:02d}-{LEAK_STEPS[k-1][0]}.html" if k > 0 else None
        nxt = f"{k+2:02d}-{LEAK_STEPS[k+1][0]}.html" if k < t - 1 else f"{1:02d}-{LEAK_STEPS[0][0]}.html"
        nlabel = "Print another →" if k == t - 1 else "Next →"
        summ = label_summary(emp="11111",
                             model="M100-A" if k >= 1 else "—",
                             qty="40" if k >= 2 else "—")
        (ld / fn).write_text(flow_page(k+1, t, "HGP Leaking Housing Label", title,
            "Leaking-housing label print flow (Prev/Next step panels).",
            leak_left(slug, label or "", tb or ""), summ,
            "LeakingHousingLabel.cs", note, dots, prev, k == 0, nxt, nlabel, up="../../"))
    print("wrote leaking", t)
    # --- Washed/Leak Tested: claiming / reprint / nonhg ---
    # Source panel chains (WashedLeakTestedLabel.cs):
    #   Claiming: Employee -> Serial -> Qty -> Complete
    #   Reprint:  Employee -> Serial -> Complete (W-suffix stripped; reprints existing label)
    #   NonHG:    Employee -> Serial -> Model -> Qty -> Lot -> Complete
    WQ = dict(title="Quantity", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Confirm quantity</h2>
      <div class="field"><label>Quantity (tbQty, prefilled with the claimed qty)</label><input type="text" value="40"></div>
      <div class="note">Enter accepts here (AcceptButton = Next).</div>
    </div>""",
        summ=dict(emp="11111", serial="7159D60100", model="M100-A", qty="40"),
        note="Claiming-only step: confirm the claimed quantity before completion.")
    WC = dict(title="Complete", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Done</h2>
      <p><strong>Hit the Print Label button to print.</strong></p>
    </div>""",
        summ=dict(emp="11111", serial="7159D60100", model="M100-A", qty="40"),
        note="Completion state; loops back to Employee for the next label.")
    WE = dict(title="Employee Number", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Scan badge</h2>
      <div class="field"><label>Scan Employee Number:</label><input type="text" placeholder="_____"></div>
    </div>""",
        summ=dict(emp="11111"),
        note="Badges the operator into this label flow.")
    WS = dict(title="Serial Number", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Scan serial</h2>
      <div class="field"><label>Scan Serial Number:</label><input type="text" placeholder="7159D60100"></div>
      <div class="btnrow"><button type="button" onclick="location.href='../nonhg/01-model.html'">Continue for Non-HG Serial</button></div>
      <div class="note">Claiming blocks already-printed serials: 'A Washed/Leak Tested label has already been printed for this serial #. Please use the Reprint button on the Main Menu.'</div>
    </div>""",
        summ=dict(emp="11111", serial="7159D60100", model="M100-A", qty="40"),
        note="HG serials resolve model + qty automatically; non-HG serials take the Non-HG branch.")
    WSR = dict(title="Serial Number (Reprint)", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Scan serial to reprint</h2>
      <div class="field"><label>Scan Serial Number:</label><input type="text" placeholder="7159D60100W"></div>
      <div class="note">Reprint strips a trailing W/w (reprint serials carry a W suffix), looks up the existing claim, and reprints — nothing new is saved.</div>
    </div>""",
        summ=dict(emp="11111", serial="7159D60100", model="M100-A", qty="40"),
        note="Reprint-only: no Qty step; Serial goes straight to Complete.")
    WRC = dict(title="Complete (Reprint)", src="WashedLeakTestedLabel.cs",
        left="""
    <div class="panel"><h2>Done</h2>
      <p><strong>Hit the Print Label button to reprint.</strong></p>
    </div>""",
        summ=dict(emp="11111", serial="7159D60100", model="M100-A", qty="40"),
        note="Reprint completion; loops back to Employee.")

    # Build with explicit filename lists to keep hrefs trivially correct.
    def washed_flow2(sub, files, titles, lefts, summs, notes, srcs, header, blurb):
        wd = OUT / "washed" / sub
        wd.mkdir(parents=True, exist_ok=True)
        t = len(files)
        names = titles
        for k in range(t):
            dots = [(names[j], files[j]) for j in range(t)]
            prev = None if k == 0 else files[k-1]
            nxt = files[0] if k == t - 1 else files[k+1]
            nlabel = "Print another →" if k == t - 1 else "Next →"
            (wd / files[k]).write_text(flow_page(k+1, t, header, titles[k], blurb,
                lefts[k], summ_html(summs[k]), srcs, notes[k], dots,
                prev, k == 0, nxt, nlabel, up="../../../"))
        print("wrote washed/" + sub, t)

    WLEFT_E = WE["left"]
    washed_flow2("claiming",
        ["01-employee.html", "02-serial.html", "03-qty.html", "04-complete.html"],
        ["Employee", "Serial", "Qty", "Complete"],
        [WE["left"], WS["left"].replace("../nonhg/01-model.html", "../nonhg/01-model.html"), WQ["left"], WC["left"]],
        [WE["summ"], WS["summ"], WQ["summ"], WC["summ"]],
        [WE["note"], WS["note"], WQ["note"], WC["note"]],
        "WashedLeakTestedLabel.cs",
        "Washed/Leak Tested (Claiming)", "Claiming flow: Employee → Serial → Qty → Complete.")
    washed_flow2("reprint",
        ["01-employee.html", "02-serial.html", "03-complete.html"],
        ["Employee", "Serial", "Complete"],
        [WE["left"], WSR["left"], WRC["left"]],
        [WE["summ"], WSR["summ"], WRC["summ"]],
        [WE["note"], WSR["note"], WRC["note"]],
        "WashedLeakTestedLabel.cs",
        "Washed/Leak Tested (Reprint)", "Reprint flow: Employee → Serial → Complete. No Qty step.")
    print("wrote washed claiming 4 + reprint 3")
    nwd = OUT / 'washed' / 'nonhg'
    nwd.mkdir(parents=True, exist_ok=True)
    for k, (slug, title, label, tb, note, sd) in enumerate(WASH_NONHG):
        fn = '0' + str(k+1) + '-' + slug + '.html'
        dots = [(WASH_NONHG_NAMES[j], '0' + str(j+1) + '-' + s + '.html') for j, (s, a1, a2, a3, a4, a5) in enumerate(WASH_NONHG)]
        prev = ('0' + str(k) + '-' + WASH_NONHG[k-1][0] + '.html') if k > 0 else '../claiming/02-serial.html'
        if k < 2:
            nxt = '0' + str(k+2) + '-' + WASH_NONHG[k+1][0] + '.html'
            nlabel = 'Continue →'
        else:
            nxt = '../claiming/04-complete.html'
            nlabel = 'Back to complete →'
        left = '<div class="panel"><h2>' + label + '</h2><div class="field"><label>' + label + '</label><input type="text" placeholder="scan…"></div></div>'
        (nwd / fn).write_text(flow_page(k+1, 3, 'Washed/Leak Tested (Non-HG branch)', title,
            'Non-Hydro-Gear branch: extra Model / Qty / Lot capture, then back to Claiming Complete.',
            left, summ_html(sd), 'WashedLeakTestedLabel.cs', note, dots, prev, False, nxt, nlabel, up='../../../'))
    print('wrote washed/nonhg 3')
    # --- View Data grid ---
    rows = "\n".join(
        f"<tr><td class='mono'>P-0041{i}</td><td class='mono'>M100-A</td><td>40</td><td>40</td>"
        f"<td class='mono'>7159D6010{i}</td><td>118.4</td><td>Sullivan</td><td>2026-09-0{i}</td></tr>"
        for i in range(1, 6))
    (OUT / "view-data.html").write_text(single_page("View Claiming Data", "View Claiming Data",
        "Menu: View Data. Grid of claimed skids, newest first (CreatedDate desc). Double-click a row to jump back to its step; Edit Claimed Qty opens the popup.",
        f"""
<div class="panel"><h2>Claimed skids</h2>
<table><thead><tr><th>Pallet Id</th><th>Model #</th><th>Skid Qty</th><th>Claimed</th><th>Serial</th><th>Weight</th><th>Plant</th><th>Created</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="btnrow"><button type="button">|&lt;</button><button type="button">&lt;</button><span>Page 1 of 1</span><button type="button">&gt;</button><button type="button">&gt;|</button></div>
</div>
<div class="panel"><h2>Filters</h2>
<p><strong>Plant Location:</strong> <label><input type="checkbox" checked> Sullivan</label> <label><input type="checkbox" checked> Princeton</label> <label><input type="checkbox" checked> Indianapolis</label> <label><input type="checkbox" checked> Huntingdon</label></p>
<p><label><input type="checkbox" checked> Claimed but not yet imported into MTMS</label></p>
<div class="btnrow"><button type="button" onclick="location.href='./view-data-popup.html'">Edit Claimed Qty</button></div>
</div>""",
        "ViewUnitClaimingData.cs"))
    (OUT / "view-data-popup.html").write_text(single_page("Edit Claimed Qty", "Edit Claimed Qty",
        "Dialog from View Data → Edit Claimed Qty. Edits the claimed quantity and the MTMS-send flag for the selected skid.",
        """
<div class="panel"><h2>Claimed Quantity</h2>
<div class="field"><label>Claimed Quantity:</label><input type="text" placeholder="40"></div>
<div class="field"><label><input type="checkbox" checked> Send to MTMS</label></div>
<div class="btnrow"><button type="button" onclick="location.href='./view-data.html'">Save</button><button type="button" onclick="location.href='./view-data.html'">Cancel</button></div>
</div>""",
        "ViewUnitClaimingDataPopup.cs"))
    print("wrote view-data + popup")
    # --- Import from MTMS ---
    (OUT / "import-mtms.html").write_text(single_page("Import Units from MTMS", "Import Units from MTMS",
        "Menu entry. Pulls unit records from MTMS; results log streams into the textbox below.",
        """
<div class="panel"><h2>Import</h2>
<div class="btnrow"><button type="button">Import Units From MTMS</button></div>
<div class="field"><label>Results</label><input type="text" placeholder="import log streams here…" readonly></div>
</div>""",
        "ImportFromMTMS.cs"))
    print("wrote import-mtms")
    # --- Configuration settings mockup ---
    protos = [
        "Use Mettler Scale Protocol (Sullivan HGX)",
        "Use Optima OP-900 Protocol (Indianapolis)",
        "Use Avery Weight-Tronix (Indianapolis)",
        "Use Avery Weight-Tronix via IP (Indianapolis) 172.20.152.226 / 6671",
        "Use Avery Weight-Tronix via IP (Sullivan) 172.20.1.88 / 1702",
        "Use Avery Weight-Tronix via IP (Huntingdon) 172.20.1.232.129 / 1702",
        "Use Avery Weight-Tronix via IP (Scale IP) / (Scale Port)",
        "Use Mettler Scale via IP (Princeton) 172.20.100.215 / 1702",
    ]
    plist = "\n".join(f'<div class="field"><label><input type="radio" name="proto"{" checked" if i == 3 else ""}> {p}</label></div>'
                       for i, p in enumerate(protos))
    (OUT / "configuration.html").write_text(single_page("Configure", "Configure — settings",
        "Menu: Configure. Global settings page (also covered as an excalidraw wireframe in the main gallery).",
        f"""
<div class="panel"><h2>Plant Location</h2>
<label><input type="radio" name="plant" checked> Sullivan</label> <label><input type="radio" name="plant"> Princeton</label> <label><input type="radio" name="plant"> Indianapolis</label> <label><input type="radio" name="plant"> Huntingdon</label>
</div>
<div class="panel"><h2>Printing</h2>
<div class="field"><label><input type="checkbox"> Printing Disabled</label></div>
<div class="field"><label>Printer override - Always print to:</label><select><option>— unselected —</option><option>Zebra-01</option></select></div>
<p class="hint">Leave this unselected unless you've been instructed to set it.</p>
<div class="field"><label><input type="checkbox"> Disable First Claim in Shift Message</label></div>
</div>
<div class="panel"><h2>Scale Interface</h2>
<div class="field"><label>Read scale data from this COM port (COM1, COM2, etc):</label><input type="text" placeholder="COM1"></div>
{plist}
<p class="hint">Note: Use PuTTY to establish/test communication with scales.</p>
</div>
<div class="panel"><h2>IP Connection Info</h2>
<p class="hint">Enabled only when an IP-based protocol is checked. IP and Port must be set manually!</p>
<div class="field"><label>IP:</label><input type="text" value="172.20.152.226"></div>
<div class="field"><label>Port:</label><input type="text" value="6671"></div>
<div class="btnrow"><button type="button" onclick="location.href='../wizard/main-menu.html'">Save and Exit</button></div>
</div>""",
        "Configuration.cs"))
    print("wrote configuration")
    # --- Error detail dialog ---
    (OUT / "error-detail.html").write_text(single_page("Error Detail", "Error Detail",
        "Dialog opened by clicking the error label after an exception. Shows the full error text for support.",
        """
<div class="panel"><h2>Error text</h2>
<div class="field"><label>Detail (tbError, read-only, scrollable)</label><input type="text" value="System.Exception: …" readonly></div>
</div>""",
        "ErrorDetail.cs"))
    print("wrote error-detail")
    # --- Dead UI: tolerance + packaging ---
    (OUT / "tolerance-factor.html").write_text(single_page("Set Tolerance Factor", "Set Tolerance Factor (unreachable)",
        "ADMIN DIALOG, unreachable: the only caller has been commented out since 6/1/2012 ('Leave the admin out of the app'). Documented for the web conversion, where it becomes a real admin screen.",
        """
<div class="panel"><h2>Tolerance Factor</h2>
<div class="field"><label>Tolerance Factor:</label><input type="text" placeholder="0.025"></div>
<div class="btnrow"><button type="button">Save</button><button type="button">Cancel</button></div>
</div>""",
        "SetToleranceFactor.cs"))
    (OUT / "edit-packaging.html").write_text(single_page("Edit Packaging Data", "Edit Packaging Data (unreachable)",
        "EDITOR, unreachable: the MDIParent1 menu hook is commented out. Grid of product groups → packaging types; click a column header to sort, double-click a row to edit.",
        """
<div class="panel"><h2>Product groups</h2>
<table><thead><tr><th>ProductGroupName</th><th>PackagingTypeDisplayString</th></tr></thead>
<tbody><tr><td class="mono">HGX-Series</td><td>Wood pallet + top</td></tr><tr><td class="mono">KIT-Line</td><td>Slip sheet</td></tr></tbody></table>
</div>""",
        "xxEditPackagingData.cs"))
    print("wrote dead-ui pair")
    # --- Denied access error state ---
    (OUT / "denied-access.html").write_text(single_page("Access Denied", "Access Denied",
        "Error state when a badge has no Unit Claiming rights: 'This employee badge number has not been given rights to use this application.' Previous is disabled; the only path is a different badge.",
        """
<div class="panel"><h2>Not authorized</h2>
<p><strong>This employee badge number has not been given rights to use this application.</strong></p>
<div class="btnrow"><button type="button" onclick="location.href='../wizard/01-employee-auth.html'">Try a different badge</button></div>
</div>""",
        "UnitClaimingMainForm.cs",
        extra=" + <span class='mono'>UnitClaimingMainFormController.DataCollectionSteps.DeniedAccess</span>"))
    print("wrote denied-access")

if __name__ == "__main__":
    if not CSS:
        raise SystemExit("missing /tmp/wizard_css.txt — export CSS from wizard_gen first")
    main()
