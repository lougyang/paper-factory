# Paper Figure Pro — 学术论文全类型图表绘制 Skill

覆盖架构图、数据图、流程图、热力图、消融柱状图、收敛曲线、参数散点图。
从设计理念到工具执行，一条命令完成。无 Visio 时自动降级为 matplotlib。

## 快速选择

```
你要画什么？
  架构图/框架图 → Visio COM (主) / matplotlib patches (备)
  数据图(柱/线/散/双Y轴) → matplotlib
  热力图 → matplotlib/seaborn
  流程图 → Visio COM / matplotlib patches
  收敛曲线 → matplotlib
  SVD/特征值衰减 → matplotlib
  信号分解图 → matplotlib
```

## 核心工作流

### 1. 理解需求
- 问清楚：多少模块？什么关系？哪些是容器？哪些并行？
- 确定层级：输入→处理→输出。每层几个节点。
- 确定对称轴：日/周并排？低/高并排？S_out/S_dyn 汇合？

### 2. 选配色 (2-3 色系)
```
蓝色系: bg=226,240,252 → inner=190,220,248 → mid=68,150,212 → dark=26,95,160
橙色系: bg=254,236,210 → inner=250,216,166 → mid=242,192,120 → dark=200,78,10
灰色系: input=235,235,240 → output=215,220,228 → operator=150,165,175
```

### 3. 定尺寸 (内容驱动)
- 盒子宽 = 文字需要的宽度（不是容器宽度）
- 盒子高 = 文字高度 + 少量留白
- 不要拉伸到容器边缘——给白色呼吸空间
- 并行模块等宽等高等 y，体现对称

### 4. 排布局 (格式塔原则)
- **邻近**: 相关模块紧挨 (gap 0.2-0.3in)
- **对齐**: 同层模块同 y，垂直流严格纵向
- **对称**: 日/周镜像、低/高镜像
- **公共区域**: 容器包裹相关模块
- **层次**: 容器(最淡)→内部盒(中)→输出(最深)→终止符

### 5. 画连线 (层级分明)
- 分支内垂直流: 1.0-1.2pt
- 跨分支/输出链路: 1.5pt
- 用 junction 点做分流/汇合，不直接从形状拉多根线
- 输入干线: X→小黑点→三分支

### 6. 检查 (提交前)
- [ ] 所有模块在容器边界内？
- [ ] 无形状重叠？
- [ ] 并行模块等宽等高同 y？
- [ ] 线条交叉最少？无穿脸线？
- [ ] 文字字体大小一致？填满盒子？
- [ ] 重要节点颜色更深/更大？

---

## 工具选择

### Visio COM (首选 — Windows + Visio 桌面版)

```python
import win32com.client

app = win32com.client.Dispatch("Visio.Application")
doc = app.Documents.Add("")
page = doc.Pages.Item(1)

# 坐标系转换 (Visio 用左下角原点)
def Y(y): return PAGE_H - y

# 画矩形
s = page.DrawRectangle(x, Y(y+h), x+w, Y(y))
s.Cells("FillForegnd").Formula = "RGB(226,240,252)"  # 填充色
s.Cells("FillPattern").Formula = 1                     # 实心填充
s.Cells("LineColor").Formula = "RGB(55,55,65)"         # 边框
s.Cells("LineWeight").Formula = "0.7 pt"
s.Cells("Rounding").Formula = "0.08 in"   # 圆角 (可选)
s.Text = "Module Name"
s.Cells("Char.Size").Formula = "16 pt"
s.Cells("Para.HorzAlign").Formula = 1      # 居中

# 画圆形 (运算符)
s = page.DrawOval(cx-r, Y(cy+r), cx+r, Y(cy-r))
s.Text = "+"; s.Cells("Char.Size").Formula = "28 pt"

# 画连线
c = page.Drop(page.Application.ConnectorToolDataObject, 0, 0)
c.Cells("BeginX").GlueTo(src.Cells("PinX"))
c.Cells("EndX").GlueTo(dst.Cells("PinX"))
c.Cells("LineWeight").Formula = "1.2 pt"
c.Cells("EndArrow").Formula = 4  # 实心三角箭头
```

**适用**: 论文架构图、框架图、模块图。输出 .vsdx (可编辑) + .png (预览)。

**模板**: `references/visio_template.py` — 复制替换 LAYOUT 部分即可。

### matplotlib (备选 — 无 Visio 时自动切换)

当 Visio COM 不可用时，用 matplotlib patches 画架构图:

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

fig, ax = plt.subplots(figsize=(15, 10))
ax.set_xlim(0, 15); ax.set_ylim(0, 10)

# 矩形
box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                      facecolor="#D6EAF8", edgecolor="#333", linewidth=0.8)
ax.add_patch(box)

# 圆形
circle = Circle((cx, cy), r, facecolor="#5DADE2", edgecolor="#333")
ax.add_patch(circle)

# 箭头
arrow = FancyArrowPatch((x1,y1), (x2,y2), arrowstyle='->',
                         color='#444', linewidth=1.5)
ax.add_patch(arrow)

# 文字
ax.text(x, y, "Label", ha='center', va='center', fontsize=14)

ax.axis('off')
fig.savefig('output.pdf', bbox_inches='tight', dpi=300)
```

**适用**: 无 Visio 许可证、macOS/Linux 环境。输出 PDF/SVG/PNG。

### matplotlib 数据图 (主力)

```python
plt.rcParams.update({
    "font.family": "serif", "font.size": 10,
    "axes.spines.right": False, "axes.spines.top": False,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
```

**模板**: `references/matplotlib_template.py` — 6 种图类型速查。

---

## 图类型速查

### 架构框架图 (Visio COM 或 matplotlib patches)
- 双分支: 左右对称容器，中间留白
- 管道式: 垂直叠放，一层一个模块
- 编码器-解码器: 沙漏型，中间窄两头宽

### 水平柱状图 (消融实验)
```python
ax.barh(y_pos, values, color=colors)
ax.axvline(baseline, linestyle='--')
ax.invert_yaxis()
```

### 精度-参数量散点图
```python
ax.scatter(params, maes, s=120, c=color)
ax.invert_yaxis()  # 越低越好
```

### 双Y轴图 (损失分析)
```python
ax2 = ax1.twinx()
ax1.bar(x, maes); ax2.plot(x, fpes, color='red', marker='s')
```

### 收敛曲线
```python
ax.plot(epochs, val_mae, linewidth=1.0)
ax.scatter([best_ep], [best_val], marker='*', s=80)  # 标记最优
```

### SVD 衰减 (柱+累计折线)
```python
ax1.bar(range(1, len(S)+1), S/S[0], color=colors)
ax2 = ax1.twinx(); ax2.plot(range(1, len(S)+1), cumsum*100, color='red')
```

### 流量分解 (三行堆叠)
```python
fig, axes = plt.subplots(3, 1, sharex=True)
axes[0].plot(t, raw); axes[0].plot(t, periodic)        # 面板A
axes[1].fill_between(t, 0, periodic, alpha=0.25)        # 面板B
axes[2].fill_between(t, 0, residual, color='red', alpha=0.25)  # 面板C
```

---

## 设计禁忌 (Marshall et al. 2025 + Jambor 2025)

| 禁忌 | 原因 |
|------|------|
| 模块拉伸到容器全宽 | 失去形状语义，像是占位符 |
| 等高层模块不同宽 | 破坏对称感 |
| 文字太小留白太多 | 读者无法快速识别模块 |
| 线条穿越模块表面 | 遮挡信息，视觉混乱 |
| 过多颜色 (>4 族) | 认知过载 |
| 红绿配色 | 8% 男性色盲不可读 |
| 只用颜色区分信息 | 必须双编码 (颜色+形状/线型/标签) |
| 容器边框用虚线 | 分散注意力，用浅色实线填充 |
| 不同粗细的并行分支 | 视觉权重不一致 |
| 不标注箭头含义 | 数据流 vs 反馈 vs 残差 必须能区分 |

## 字体规范

- 论文图: 主体 13-16pt, 标题 18-22pt, 运算符 26-30pt
- 最小字号 ≥ 7pt (Jambor 2025)
- 英文: Times New Roman / Georgia / Segoe UI
- 中文: SimSun / Microsoft YaHei
- 全图字体一致

## 输出规范

| 用途 | 格式 | DPI |
|------|------|-----|
| LaTeX 论文 | PDF + SVG | 矢量 |
| Word 论文 | PNG 或 SVG | 300 |
| 提交审查 | PNG | 300 |
| Visio 源文件 | VSDX | — |
| 版本备份 | VSDX (时间戳) | — |

## 故障切换

```
检测 Visio COM 可用?
  YES → Visio COM 画架构图
  NO  → matplotlib patches 画架构图

matplotlib 数据图: 始终可用
```

## 参考

- Marshall et al. (2025) "Evidence-based guidance for neural network diagrams" — PLOS ONE
- Jambor (2025) "Checklist for scientific figures" — Nature Cell Biology
- Crameri et al. (2024) "Scientific colour maps" — Current Protocols
- 格式塔原理: Proximity, Similarity, Continuity, Symmetry, Common Region
