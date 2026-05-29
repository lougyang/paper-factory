# Paper Visio — 学术论文全类型图表 Skill

论文写到哪里，图就画到哪里。覆盖架构图、数据图、热力图、消融柱状图、收敛曲线、参数对比散点图。

## 图类型与工具选择

| 图类型 | 首选工具 | 备选 |
|--------|---------|------|
| 模型架构框架图 | Visio COM | matplotlib patches |
| 消融实验柱状图 (水平/垂直) | matplotlib | — |
| 精度-参数量散点图 | matplotlib | — |
| 多步预测误差分组柱状图 | matplotlib | — |
| 收敛曲线 (训练过程) | matplotlib | — |
| SVD 奇异值衰减 (柱+折线) | matplotlib | — |
| 流量分解 motivation 图 | matplotlib | — |
| 损失权重分析 (双Y轴) | matplotlib | — |
| 热力图 | matplotlib/seaborn | — |
| 实验数据表格 | CSV + LaTeX | paper-tex |
| 流程图 | Visio COM | matplotlib patches |

## 快速开始

### 1. 架构图 (Visio COM)

说需求即可，Skill 自动生成 COM 脚本：

```
/paper-visio 画一个 Transformer 编码器架构图，左侧多头注意力，右侧前馈网络
```

工作原理：直接调用 Visio COM API (pywin32)，每个形状一个 `DrawRectangle`，填色通过 ShapeSheet Cells，连线通过 `ConnectorToolDataObject`。

### 2. 数据图 (matplotlib)

```
/paper-visio 画一个消融实验柱状图
数据: Z0=18.31, C1=18.34, C3=18.47, C5=18.38
```

Skill 使用统一的论文级 matplotlib 配置：
- 字体：Times New Roman 10pt+, serif, PDF/ SVG editable text
- 配色：统一调色板，2-3 色系，高对比
- 输出：PDF + SVG + PNG 三格式，300 DPI
- 风格：去上右边框，细轴线，无图例框

### 3. 热力图

```
/paper-visio 画一个 PEMS04 节点相关性热力图
```

## matplotlib 论文级配置

所有 matplotlib 图使用此配置（内置在模板中）：

```python
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "SimSun"],
    "svg.fonttype": "none",       # editable text in SVG
    "pdf.fonttype": 42,            # editable TrueType in PDF
    "font.size": 10,               # base font size for paper
    "axes.spines.right": False,    # clean academic style
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

def save_pub(fig, name, outdir):
    """Save in all formats for paper submission."""
    for fmt in ['pdf', 'svg', 'png']:
        fig.savefig(f'{outdir}/{name}.{fmt}',
                    bbox_inches='tight', dpi=300)
```

## Visio 架构图模板

```python
import win32com.client, time

PW, PH = 15.0, 9.5  # inches
def Y(y): return PH - y  # top-left -> bottom-left

app = win32com.client.Dispatch("Visio.Application")
doc = app.Documents.Add("")
page = app.ActivePage
# ... use R(), RR(), CT(), O(), TR(), A() helpers
```

完整模板见 `references/visio_template.py`。

## 图类型速查

### 水平柱状图 (消融对比)

```python
fig, ax = plt.subplots(figsize=(5.5, 3.0))
ax.barh(y_pos, values, height=0.55, color=colors)
ax.axvline(baseline, linestyle='--', alpha=0.5)
ax.invert_yaxis()
```

### 精度-参数量散点图

```python
fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.scatter(params, maes, s=80-120, c=colors, marker='o')
ax.invert_yaxis()  # MAE: lower is better
```

### 双Y轴图 (损失分析)

```python
ax2 = ax1.twinx()
ax1.bar(x, values)       # MAE bars
ax2.plot(x, fpe_values)  # FPE line
```

### 分组柱状图 (多步预测)

```python
x = np.arange(n_groups)
for i, offset in enumerate(offsets):
    ax.bar(x + offset, values, width, label=model)
```

### 收敛曲线

```python
ax.plot(epochs, val_mae, linewidth=1.0, label='FFT init')
ax.plot(epochs, val_mae_f0, linewidth=1.0, label='Random init')
# Highlight best epochs with scatter
```

### SVD 衰减 (柱 + 累计折线)

```python
ax1.bar(range(1, len(S)+1), S/S[0], color=colors)
ax2 = ax1.twinx()
ax2.plot(range(1, len(S)+1), cumsum*100, color='red', marker='o')
```

### 流量分解 (三行堆叠)

```python
fig, axes = plt.subplots(3, 1, figsize=(7.2, 5.5), sharex=True)
axes[0].plot(hours, raw, label='Observed')
axes[0].plot(hours, periodic, label='Periodic fit')
axes[1].fill_between(hours, 0, periodic, alpha=0.25)
axes[2].fill_between(hours, 0, residual, alpha=0.25)
```

## 故障切换策略

如果 Visio COM 不可用（Linux / Mac / 无 Visio 许可证），自动降级：

1. **架构图**: 使用 matplotlib patches (`FancyBboxPatch`, `FancyArrowPatch`) 画同样的盒状图。效果不如 Visio 但能用。
2. **流程图**: 使用 `matplotlib.patches` 手动绘制
3. **数据图**: matplotlib 本身就是主力，不受影响

降级检测：
```python
try:
    import win32com.client
    app = win32com.client.Dispatch("Visio.Application")
    VISIO_AVAILABLE = True
except:
    VISIO_AVAILABLE = False
    print("Visio not available, using matplotlib fallback")
```

## 输出规范

所有图统一输出：
- **PDF**: LaTeX 论文直接引用，字体可编辑
- **SVG**: Word/网页嵌入，文字可编辑
- **PNG**: 预览/提交用，300 DPI
- **VSDX**: Visio 源文件，可继续编辑（仅架构图）

## 参考示例

`D:/Code/Claude/Claude_WorkPlace/SpecFlow/scripts/create_figures.py`
— 7 张完整论文图（motivation / SVD / 消融 / 损失 / 参数量 / 多步预测 / 收敛）

`D:/Code/Claude/Claude_WorkPlace/SpecFlow/scripts/draw_arch_visio_draw.py`
— SpecFlow 架构图 Visio COM 完整实现
