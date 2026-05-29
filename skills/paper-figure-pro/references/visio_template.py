"""
Visio Draw — Generic Architecture Diagram Template.
Copy this file, replace the LAYOUT section, run.

Requirements: pip install pywin32
Windows + Microsoft Visio desktop required.
"""
import win32com.client, time, os

OUT = os.path.expanduser("~/Desktop/diagram")
PW, PH = 15.0, 9.5   # page size in inches

COLORS = {
    "fam1_bg":    "RGB(226,240,252)", "fam1_inner": "RGB(190,220,248)",
    "fam1_mid":   "RGB(68,150,212)",  "fam1_dark":  "RGB(26,95,160)",
    "fam2_bg":    "RGB(254,236,210)", "fam2_inner": "RGB(250,216,166)",
    "fam2_mid":   "RGB(242,192,120)", "fam2_dark":  "RGB(200,78,10)",
    "gray_in":    "RGB(235,235,240)", "gray_out":   "RGB(215,220,228)",
    "gray_plus":  "RGB(150,165,175)",
    "line":       "RGB(55,55,65)",    "conn":       "RGB(80,80,90)",
}
FS = "13 pt"; FS_B = "15 pt"; FS_P = "20 pt"

def Y(y): return PH - y

app = win32com.client.Dispatch("Visio.Application")
doc = app.Documents.Add(""); page = app.ActivePage
pg = page.PageSheet
pg.Cells("PageWidth").Formula = f"{PW} in"
pg.Cells("PageHeight").Formula = f"{PH} in"

def R(x, y, w, h, text, fill, fs=FS, r=0.0):
    s = page.DrawRectangle(x, Y(y+h), x+w, Y(y))
    s.Cells("FillForegnd").Formula = fill; s.Cells("FillPattern").Formula = 1
    s.Cells("LineColor").Formula = COLORS["line"]; s.Cells("LineWeight").Formula = "0.7 pt"
    if r: s.Cells("Rounding").Formula = f"{r} in"
    s.Text = text; s.Cells("Char.Size").Formula = fs; s.Cells("Para.HorzAlign").Formula = 1
    time.sleep(0.1); return s

def RR(x, y, w, h, text, fill, fs=FS):
    return R(x, y, w, h, text, fill, fs, 0.08)

def CT(x, y, w, h, text, fill):
    s = R(x, y, w, h, text, fill, "10 pt", 0.0)
    s.Cells("LineColor").Formula = "RGB(160,165,175)"; s.Cells("LineWeight").Formula = "1.0 pt"
    s.Cells("VerticalAlign").Formula = 0; s.Cells("Para.HorzAlign").Formula = 0
    return s

def O(cx, cy, r, symbol, fill):
    s = page.DrawOval(cx-r, Y(cy+r), cx+r, Y(cy-r))
    s.Cells("FillForegnd").Formula = fill; s.Cells("FillPattern").Formula = 1
    s.Cells("LineColor").Formula = COLORS["line"]; s.Cells("LineWeight").Formula = "0.8 pt"
    s.Text = symbol; s.Cells("Char.Size").Formula = FS_P; s.Cells("Para.HorzAlign").Formula = 1
    time.sleep(0.1); return s

def TR(x, y, w, h, text, fill):
    return R(x, y, w, h, text, fill, FS_B, 0.12)

def A(src, dst):
    c = page.Drop(page.Application.ConnectorToolDataObject, 0, 0)
    c.Cells("BeginX").GlueTo(src.Cells("PinX")); c.Cells("EndX").GlueTo(dst.Cells("PinX"))
    c.Cells("LineColor").Formula = COLORS["conn"]; c.Cells("LineWeight").Formula = "0.85 pt"
    c.Cells("EndArrow").Formula = 4; time.sleep(0.05); return c

# ═══════════════ LAYOUT — Replace below ═══════════════
time.sleep(0.5)
X = RR(6.4, 0.3, 2.2, 0.55, "Input", COLORS["gray_in"], FS_B)
time.sleep(0.3)
# ... your shapes here ...
# ═══════════════════════════════════════════════════════

time.sleep(0.5)
doc.SaveAs(OUT + ".vsdx"); print(f"Saved: {OUT}.vsdx")
try: page.Export(OUT + ".png"); print(f"Saved: {OUT}.png")
except: print("PNG export failed")
doc.Close(); app.Quit(); print("Done.")
