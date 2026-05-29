"""
Demo: AI draws an architecture diagram step by step.
Record this with Win+Alt+R for your Douyin video.
"""
import win32com.client, time

OUT = r"D:\Code\Claude\skills-collection\examples\demo_arch"
W, H = 14.0, 8.5
def Y(y): return H - y

C = {
    "bbg": "RGB(226,240,252)", "bin": "RGB(190,220,248)", "bout": "RGB(68,150,212)", "bp": "RGB(52,130,195)",
    "obg": "RGB(254,236,210)", "oin": "RGB(250,216,166)", "ofq": "RGB(242,192,120)", "ofc": "RGB(238,152,55)", "odo": "RGB(200,78,10)",
    "xg": "RGB(235,235,240)",  "yg": "RGB(215,220,228)",  "ag": "RGB(150,165,175)",
}
FS = "14 pt"; FB = "16 pt"; FP = "22 pt"

app = win32com.client.Dispatch("Visio.Application")
doc = app.Documents.Add("")
page = doc.Pages.Item(1)
pg = page.PageSheet
pg.Cells("PageWidth").Formula  = f"{W} in"
pg.Cells("PageHeight").Formula = f"{H} in"

def rect(x, y, ww, hh, t, fill, fs=FS, r=0.0):
    s = page.DrawRectangle(x, Y(y+hh), x+ww, Y(y))
    s.Cells("FillForegnd").Formula = fill; s.Cells("FillPattern").Formula = 1
    s.Cells("LineColor").Formula = "RGB(55,55,65)"; s.Cells("LineWeight").Formula = "0.7 pt"
    if r: s.Cells("Rounding").Formula = f"{r} in"
    s.Text = t; s.Cells("Char.Size").Formula = fs; s.Cells("Para.HorzAlign").Formula = 1
    time.sleep(0.2); return s

def rrect(x, y, ww, hh, t, fill, fs=FS):
    return rect(x, y, ww, hh, t, fill, fs, 0.08)

def container(x, y, ww, hh, t, fill):
    s = rect(x, y, ww, hh, t, fill, '')
    s.Cells("LineColor").Formula = "RGB(160,165,175)"; s.Cells("LineWeight").Formula = "1.0 pt"
    s.Cells("VerticalAlign").Formula = 0; s.Cells("Para.HorzAlign").Formula = 0
    return s

def circle(cx, cy, r, sym, fill):
    s = page.DrawOval(cx-r, Y(cy+r), cx+r, Y(cy-r))
    s.Cells("FillForegnd").Formula = fill; s.Cells("FillPattern").Formula = 1
    s.Cells("LineColor").Formula = "RGB(55,55,65)"; s.Cells("LineWeight").Formula = "0.8 pt"
    s.Text = sym; s.Cells("Char.Size").Formula = FP; s.Cells("Para.HorzAlign").Formula = 1
    time.sleep(0.2); return s

def arrow(s1, s2):
    c = page.Drop(page.Application.ConnectorToolDataObject, 0, 0)
    c.Cells("BeginX").GlueTo(s1.Cells("PinX")); c.Cells("EndX").GlueTo(s2.Cells("PinX"))
    c.Cells("LineColor").Formula = "RGB(80,80,90)"; c.Cells("LineWeight").Formula = "0.85 pt"
    c.Cells("EndArrow").Formula = 4
    time.sleep(0.1); return c

# ═══════════════════════════════════════════════
time.sleep(1.0)

# ── INPUT ──
X = rrect(6.0, 0.3, 2.0, 0.55, '', C["xg"], FB)
time.sleep(0.3)

# ── ENCODER CONTAINER ──
ce = container(0.4, 1.3, 6.0, 4.5, '', C["bbg"])
time.sleep(0.2)
e1 = rect(0.8, 1.9, 2.5, 0.7, '', C["bin"])
e2 = rect(3.7, 1.9, 2.5, 0.7, '', C["bin"])
time.sleep(0.2)
e1o = rrect(1.1, 2.9, 1.9, 0.5, '', C["bout"])
e2o = rrect(4.0, 2.9, 1.9, 0.5, '', C["bout"])
time.sleep(0.2)
ep = circle(3.5, 3.7, 0.28, '', C["bp"])
time.sleep(0.2)
eout = rrect(1.8, 4.5, 3.0, 0.55, '', C["bout"], FB)
time.sleep(0.3)

# ── DECODER CONTAINER ──
cd = container(7.0, 1.3, 6.5, 4.5, '', C["obg"])
time.sleep(0.2)
d1 = rect(7.4, 1.9, 5.5, 0.55, '', C["oin"])
time.sleep(0.2)
d2 = rect(7.4, 2.65, 2.5, 0.7, '', C["ofq"])
d3 = rect(10.4, 2.65, 2.5, 0.7, '', C["ofq"])
time.sleep(0.2)
d2o = rect(8.3, 3.55, 3.0, 0.5, '', C["oin"])
time.sleep(0.2)
d4 = rect(7.4, 4.25, 5.5, 0.55, '', C["ofc"])
time.sleep(0.2)
dout = rrect(9.0, 5.0, 2.5, 0.55, '', C["odo"], FB)
time.sleep(0.3)

# ── FINAL ──
fp = circle(7.0, 6.3, 0.28, '', C["ag"])
Y = rrect(5.5, 6.9, 3.0, 0.55, '', C["yg"], FB)
time.sleep(0.5)

# ── CONNECTORS ──
arrow(X, e1); arrow(X, e2); arrow(X, d1)
arrow(e1, e1o); arrow(e2, e2o)
arrow(e1o, ep); arrow(e2o, ep)
arrow(ep, eout)
arrow(d1, d2); arrow(d1, d3)
arrow(d2, d2o); arrow(d3, d2o)
arrow(d2o, d4)
arrow(d4, dout)
arrow(eout, fp); arrow(dout, fp)
arrow(fp, Y)

time.sleep(0.5)
doc.SaveAs(OUT + ".vsdx")
print(f"Saved: {OUT}.vsdx")
try: page.Export(OUT + ".png"); print(f"Saved: {OUT}.png")
except: print("PNG export failed")
doc.Close(); app.Quit()
print("Done — ready for recording!")
