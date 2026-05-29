"""
SpecFlow architecture diagram — COM drawing script.
Run this to regenerate the .vsdx.
"""
import win32com.client, time
OUT = r"D:\Code\Claude\Claude_WorkPlace\SpecFlow\docs\figures\specflow_arch"
PW, PH = 15.0, 9.5
def Y(y): return PH - y

C = {
    "fpe_bg":"RGB(226,240,252)","fpe_in":"RGB(190,220,248)","fpe_out":"RGB(68,150,212)",
    "fpe_plus":"RGB(52,130,195)","fpe_so":"RGB(26,95,160)","fpe_si":"RGB(140,195,235)",
    "stfe_bg":"RGB(254,236,210)","stfe_in":"RGB(250,216,166)","stfe_fq":"RGB(242,192,120)",
    "stfe_fc":"RGB(238,152,55)","stfe_do":"RGB(200,78,10)","stfe_tp":"RGB(245,200,150)",
    "x_gray":"RGB(235,235,240)","y_gray":"RGB(215,220,228)","add_gray":"RGB(150,165,175)",
    "ln":"RGB(55,55,65)",
}
FS="14 pt"; FS_B="16 pt"; FS_P="22 pt"

app=win32com.client.Dispatch("Visio.Application")
doc=app.Documents.Add("")
page=app.ActivePage
pg=page.PageSheet
pg.Cells("PageWidth").Formula=f"{PW} in"
pg.Cells("PageHeight").Formula=f"{PH} in"

def rect(x,y,w,h,t,fill,fs=FS,r=0.0):
    s=page.DrawRectangle(x,Y(y+h),x+w,Y(y))
    s.Cells("FillForegnd").Formula=fill;s.Cells("FillPattern").Formula=1
    s.Cells("LineColor").Formula=C["ln"];s.Cells("LineWeight").Formula="0.7 pt"
    if r:s.Cells("Rounding").Formula=f"{r} in"
    s.Text=t;s.Cells("Char.Size").Formula=fs;s.Cells("Para.HorzAlign").Formula=1
    time.sleep(0.12);return s

def rrect(x,y,w,h,t,fill,fs=FS):return rect(x,y,w,h,t,fill,fs,0.08)
def container(x,y,w,h,t,fill):
    s=R(x,y,w,h,t,fill,"10 pt");s.Cells("LineColor").Formula="RGB(160,165,175)"
    s.Cells("LineWeight").Formula="1.0 pt";s.Cells("VerticalAlign").Formula=0
    s.Cells("Para.HorzAlign").Formula=0;return s
def circle(cx,cy,r,sym,fill):
    s=page.DrawOval(cx-r,Y(cy+r),cx+r,Y(cy-r))
    s.Cells("FillForegnd").Formula=fill;s.Cells("FillPattern").Formula=1
    s.Cells("LineColor").Formula=C["ln"];s.Cells("LineWeight").Formula="0.8 pt"
    s.Text=sym;s.Cells("Char.Size").Formula=FS_P;s.Cells("Para.HorzAlign").Formula=1
    time.sleep(0.12);return s
def term(x,y,w,h,t,fill):return R(x,y,w,h,t,fill,FS_B,0.12)
def arrow(s1,s2):
    c=page.Drop(page.Application.ConnectorToolDataObject,0,0)
    c.Cells("BeginX").GlueTo(s1.Cells("PinX"));c.Cells("EndX").GlueTo(s2.Cells("PinX"))
    c.Cells("LineColor").Formula="RGB(80,80,90)";c.Cells("LineWeight").Formula="0.85 pt"
    c.Cells("EndArrow").Formula=4;time.sleep(0.06);return c

time.sleep(0.5)
# INPUT
X=RR(6.4,0.3,2.2,0.55,"Input  X",C["x_gray"],FS_B)
time.sleep(0.3)

# FPE
c_fpe=CT(0.3,1.3,6.5,4.3,"  HarmonicPE",C["fpe_bg"])
time.sleep(0.15)
d_enc=R(0.8,1.8,2.5,0.75,"Daily Encoder\nFourier + SVD",C["fpe_in"])
w_enc=R(3.8,1.8,2.7,0.75,"Weekly Encoder\nFourier + SVD",C["fpe_in"])
time.sleep(0.15)
d_out=RR(1.1,2.85,1.9,0.5,"S_daily",C["fpe_out"])
w_out=RR(4.1,2.85,1.9,0.5,"S_weekly",C["fpe_out"])
time.sleep(0.15)
fpe_p=O(3.5,4.0,0.28,"+",C["fpe_plus"])
time.sleep(0.15)
sout=RR(1.3,5.0,2.5,0.55,"S_out",C["fpe_so"],FS_B)
sin=RR(4.6,4.25,2.0,0.5,"S_in",C["fpe_si"])
time.sleep(0.4)

# STFE
c_stfe=CT(7.2,1.3,7.4,6.65,"  FreqSurge",C["stfe_bg"])
time.sleep(0.15)
stfe_in=R(7.7,1.8,6.5,0.55,"Residual  R = X - S_in",C["stfe_in"])
time.sleep(0.15)
smp=R(7.7,2.55,6.5,0.65,"FlowGraph  --  Spatial Message Passing",C["stfe_in"])
time.sleep(0.15)
fft_s=R(9.3,3.45,3.0,0.7,"Spatial FFT\n154 frequency points",C["stfe_fq"])
time.sleep(0.15)
sp_low=R(7.7,4.4,3.4,0.75,"Low-Freq (0~10)\nSVD Bottleneck",C["stfe_fq"])
sp_high=R(11.4,4.4,3.3,0.75,"High-Freq (11~153)\ncMLP",C["stfe_fq"])
time.sleep(0.15)
ifft_s=R(9.5,5.4,3.2,0.5,"Spatial IFFT",C["stfe_in"])
time.sleep(0.15)
temp_f=R(7.7,6.15,6.5,0.65,"Temporal Spectral:  FFT -> cMLP -> IFFT",C["stfe_tp"])
time.sleep(0.15)
fc=R(7.7,7.0,6.5,0.6,"FC Output Mapping",C["stfe_fc"])
time.sleep(0.15)
sdyn=RR(9.8,7.85,2.4,0.5,"S_dyn",C["stfe_do"],FS_B)
time.sleep(0.4)

# FINAL
final_p=O(7.25,8.6,0.28,"+",C["add_gray"])
Y_out=TR(5.5,9.1,3.5,0.55,"Prediction  Y",C["y_gray"])
time.sleep(0.4)

# CONNECTORS
for a,b in [(X,d_enc),(X,w_enc),(X,stfe_in),
    (d_enc,d_out),(w_enc,w_out),
    (d_out,fpe_p),(w_out,fpe_p),
    (fpe_p,sout),(fpe_p,sin),
    (sin,stfe_in),
    (stfe_in,smp),(smp,fft_s),
    (fft_s,sp_low),(fft_s,sp_high),
    (sp_low,ifft_s),(sp_high,ifft_s),
    (ifft_s,temp_f),(temp_f,fc),(fc,sdyn),
    (sout,final_p),(sdyn,final_p),
    (final_p,Y_out)]:
    A(a,b)

time.sleep(0.5)
doc.SaveAs(OUT+".vsdx");print(f"Saved: {OUT}.vsdx")
try:page.Export(OUT+".png");print(f"Saved: {OUT}.png")
except:print("PNG export failed")
doc.Close();app.Quit();print("Done.")
