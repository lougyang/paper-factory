# Visio Draw — Direct COM Architecture Diagram Skill

Draw publication-quality architecture diagrams directly via Microsoft Visio COM
(pywin32). No scene.json, no intermediate layer. Full control over every shape,
color, font, and connector.

## When to Use

- Paper architecture / framework / module diagrams for academic journals
- System architecture diagrams with color-coded sub-modules
- Any box-and-arrow diagram where fills, fonts, and clean routing matter

## Not For

- Exact replicas of existing images (use /visiomaster)
- Statistical plots (use /nature-figure or matplotlib directly)
- Slides (use /nature-paper2ppt)

## Requirements

- Windows + Microsoft Visio desktop (2016 or later)
- Python with `pywin32`:
  ```powershell
  pip install pywin32
  ```

## How It Works

The skill writes and executes a Python script that calls Visio's COM API directly.
Every shape is a `page.DrawRectangle` or `page.DrawOval` call. Colors set via
ShapeSheet cells. Connectors via `ConnectorToolDataObject`.

No scene.json parsing overhead. No style profile conflicts. What you write is what
Visio draws.

## User Interaction Flow

1. **Understand the diagram**: Ask the user what modules/submodules/connections
   they want. Clarify the hierarchy (containers vs inner boxes vs leaf nodes).

2. **Design the layout**: Choose page dimensions. Decide x/y/w/h for each shape.
   Use a top-left coordinate system. The script converts to Visio's bottom-left
   internally.

3. **Pick colors**: 2-3 color families. Each family: container (lightest) →
   inner boxes (mid) → output (darkest). Plus neutral grays for input/output/operators.

4. **Write the script**: Use `R()`, `RR()`, `CT()`, `O()`, `TR()` helpers from
   the template. ~40-60 lines for a typical architecture diagram.

5. **Run + iterate**: The script creates .vsdx + .png. User opens in Visio,
   manually adjusts connector endpoints if needed (Visio auto-snap does most of
   the work).

## Core Functions (from template)

```python
PAGE_W, PAGE_H = 15.0, 9.5  # inches

def Y(y): return PAGE_H - y  # top-left -> bottom-left conversion

def R(x, y, w, h, text, fill, font_size="13 pt", rounding=0.0):
    """Rectangle. rounding=0.08 for rounded corners."""

def RR(x, y, w, h, text, fill, font_size="13 pt"):
    """Rounded rectangle (0.08in corners)."""

def CT(x, y, w, h, text, fill):
    """Container — lighter border, left-aligned title, smaller font."""

def O(cx, cy, r, symbol, fill):
    """Circle with centered symbol (+ , x, etc.). r=0.28 is standard."""

def TR(x, y, w, h, text, fill):
    """Terminator — heavily rounded, larger font."""

def A(src_shape, dst_shape):
    """Dynamic connector arrow. Glues to shape PinX/PinY."""
```

## Color Rules

| Role | RGB Range | Border |
|------|-----------|--------|
| Container | lightest (200-250) | light gray |
| Inner box | mid (160-220) | dark gray 55,55,65 |
| Output | darkest (25-100) | dark gray |
| Input / sum-op | gray (200-235) | dark gray |
| Connector | n/a | 80,80,90 |

Two-family example (blue + orange):
```
Blue family:   bg=226,240,252  inner=190,220,248  mid=68,150,212  dark=26,95,160
Orange family: bg=254,236,210  inner=250,216,166  mid=242,192,120  dark=200,78,10
```

## Font Sizing

| Context | Size |
|---------|------|
| Container title | 10 pt, left-aligned |
| Normal box body | 13-14 pt, centered |
| Important output labels | 15-16 pt, centered |
| Operator symbols (+ , x) | 20-22 pt, centered |
| Final output terminator | 15-16 pt, centered |

For presentation slides: double all font sizes. For posters: triple.

## Layout Principles

1. **Top-down flow**: Input at top, processing in middle, output at bottom
2. **Left-right symmetry**: Parallel sub-modules (e.g. daily/weekly) at same y
3. **Center alignment**: Shared components (e.g. FFT, IFFT) centered above/below
   their split branches
4. **Containers frame related boxes**: Use `CT()` for logical grouping
5. **Junction points**: Use `O()` with small radius for merge/fan-out circles

## Page Dimensions

- Standard paper figure: 15.0 x 9.5 inches (wider than tall for two-column layout)
- Single-column: 7.0 x 8.0 inches
- Full-page: 15.0 x 12.0 inches

## Iterating

1. Run script, open .vsdx in Visio
2. Fix connector endpoints: drag green handles to correct shape edges
3. Adjust any text that wraps awkwardly: make box wider or split text
4. Tune colors if contrast is off
5. Re-run for a clean version, or save-as from Visio

## Export

```python
doc.SaveAs(path + ".vsdx")   # editable
page.Export(path + ".png")    # preview
```

## Troubleshooting

**"只读 / DOS 无效句柄"**: Close the .vsdx file in Visio before re-running.

**Shapes invisible or wrong position**: Check the Y() conversion. Visio uses
bottom-left coordinates; the template's Y() helper handles this. If drawing
directly without the template, always convert y values.

**Connectors look messy**: Visio auto-snaps to the nearest connection point.
Fine-tune manually in Visio by dragging green connector handles.

**Colors don't show**: Set both `FillForegnd` and `FillPattern = 1`. Without
FillPattern, Visio uses the shape's default (often transparent).

**Chinese text not displaying**: The default font may not support CJK. Either
install a CJK font or set `s.Cells("Char.Font")` to an installed CJK font number.

**`pywintypes.com_error`**: Visio COM may need to be registered. Install Visio
desktop (not web/online version). Run the script from the same Python environment
that has pywin32.
