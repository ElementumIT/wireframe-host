# viz generator tools

One-shot generators for the `viz/` wireframe site. They parse the legacy
WinForms source in the ClaimingToWeb vault and emit self-contained HTML.
Re-running any script regenerates its pages deterministically.

| Script | Reads | Writes |
|---|---|---|
| `viz_gen.py` | `ref-code-20260904/UnitClaimingUI/*.Designer.cs` (vault) | `viz/*.html` — screen inventory pages + `viz/index.html` |
| `wizard_gen.py` | `UnitClaimingMainFormController.cs` step chains, `MainMenu.cs` wiring (vault) | `viz/wizard/` — Main Menu hub + 8 variation click-throughs |
| `screens_gen.py` | step/screen Designers (vault) + `wizard_css.txt` | `viz/screens/` — label flows, view-data, config mockup, dialogs |
| `wizard_css.txt` | — | shared stylesheet consumed by `screens_gen.py` |

Vault location on this host: `/home/ubuntu/Documents/Obsidian/ClaimingToWeb/`
(`ref-code-20260904/` inside it). Paths are host-local by design; if the
vault moves, update `SRC` at the top of each script.

Regenerate everything:

```bash
python3 tools/viz_gen.py && python3 tools/wizard_gen.py && python3 tools/screens_gen.py
```

Then verify: no dead links, no blank pages, `git status` shows only intended
`viz/` changes.
