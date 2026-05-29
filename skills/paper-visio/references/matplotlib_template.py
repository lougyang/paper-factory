"""
Paper-Visio: matplotlib 论文图模板。
包含全局样式设置、调色板、多类型图速查。
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ── 论文级全局样式 ──────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "SimSun", "STSong"],
    "svg.fonttype": "none",        # SVG editable text
    "pdf.fonttype": 42,             # PDF editable TrueType
    "font.size": 10,                # base font
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

OUTDIR = "./figures"
os.makedirs(OUTDIR, exist_ok=True)

# ── 统一调色板 ──────────────────────────────────────
C = {
    "blue":    "#2E86AB",
    "red":     "#D16666",
    "orange":  "#E07A30",
    "green":   "#27AE60",
    "gray":    "#7BA3B0",
    "dark":    "#404040",
    "light":   "#A8C5D0",
    "purple":  "#8E44AD",
}


def save_pub(fig, name):
    """Save figure in all formats for paper submission."""
    for fmt in ['pdf', 'svg', 'png']:
        fig.savefig(f'{OUTDIR}/{name}.{fmt}', bbox_inches='tight', dpi=300)
    print(f"  Saved {name}.pdf + .svg + .png")


# ═══════════════════════════════════════════════════════
#  图类型速查 (替换数据即可用)
# ═══════════════════════════════════════════════════════

# --- 1. 水平柱状图 (消融实验) ---
def ablation_bars():
    labels = ["Baseline", "No FPE", "No STFE", "No FlowGraph"]
    values = [18.31, 24.62, 20.64, 18.47]
    colors = [C["orange"], C["red"], C["gray"], C["blue"]]
    baseline = 18.31

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.barh(range(len(labels)), values, height=0.55, color=colors,
            edgecolor='white', linewidth=0.4)
    ax.axvline(baseline, color=C["orange"], linestyle='--', alpha=0.5)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("MAE")
    ax.invert_yaxis()
    save_pub(fig, "ablation")


# --- 2. 精度-参数量散点图 ---
def param_scatter():
    models = [
        ("Model A", 18.5, 350, C["gray"]),
        ("Model B", 18.3, 2200, C["gray"]),
        ("Ours", 18.3, 500, C["orange"]),
    ]
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    for name, mae, params, color in models:
        size = 120 if name == "Ours" else 80
        ax.scatter(params, mae, s=size, c=color, edgecolors='white', linewidth=0.5)
        ax.annotate(name, (params + 30, mae), fontsize=9)
    ax.set_xlabel("Parameters (K)")
    ax.set_ylabel("MAE")
    ax.invert_yaxis()
    save_pub(fig, "param_scatter")


# --- 3. 双Y轴图 (损失权重分析) ---
def dual_axis():
    configs = ['w=0', 'w=0.1', 'w=0.3', 'w=0.5', 'w=1.0']
    maes  = [18.40, 18.35, 18.37, 18.38, 18.39]
    fpes  = [29.2, 26.90, 24.90, 24.50, 24.30]

    fig, ax1 = plt.subplots(figsize=(5.0, 2.8))
    x = np.arange(len(configs))
    ax1.bar(x, maes, 0.38, color=[C["orange"]] + [C["gray"]] * 4)
    ax1.set_ylabel("MAE", color="#333")
    ax1.set_ylim(18.25, 18.50)

    ax2 = ax1.twinx()
    ax2.plot(x, fpes, color=C["red"], linewidth=1.2, marker='s', markersize=5)
    ax2.set_ylabel("FPE MAE", color=C["red"])
    ax2.set_ylim(22, 32)

    ax1.set_xticks(x)
    ax1.set_xticklabels(configs)
    save_pub(fig, "dual_axis")


# --- 4. 分组柱状图 (多步预测) ---
def grouped_bars():
    horizons = ['15 min', '30 min', '60 min']
    data = {
        "Ours":     [17.50, 18.39, 19.62],
        "Baseline": [17.47, 18.35, 19.56],
    }
    colors = [C["orange"], C["gray"]]
    width = 0.22

    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    x = np.arange(len(horizons))
    for i, (name, vals) in enumerate(data.items()):
        ax.bar(x + (i - 0.5) * width, vals, width, label=name, color=colors[i])

    ax.set_xticks(x)
    ax.set_xticklabels(horizons)
    ax.set_ylabel("MAE")
    ax.legend()
    save_pub(fig, "grouped_bars")


# --- 5. 收敛曲线 ---
def convergence_curve():
    epochs = range(1, 101)
    val_a = 18.5 - 0.3 * np.log(epochs) + np.random.randn(100) * 0.1
    val_b = 22 - 3 * np.log(epochs) + np.random.randn(100) * 0.3

    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    ax.plot(epochs, val_a, color=C["blue"], linewidth=1.0, label="Ours")
    ax.plot(epochs, val_b, color=C["red"], linewidth=1.0, label="Baseline")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Validation MAE")
    ax.legend()
    save_pub(fig, "convergence")


# --- 6. 三行堆叠图 (信号分解) ---
def decomposition():
    t = np.linspace(0, 168, 2016)  # 2 weeks in hours
    raw = 0.7 * np.sin(2 * np.pi * t / 24) + 0.2 * np.sin(2 * np.pi * t / 168)
    periodic = 0.7 * np.sin(2 * np.pi * t / 24)
    residual = raw - periodic

    fig, axes = plt.subplots(3, 1, figsize=(7.2, 5.5), sharex=True)
    fig.subplots_adjust(hspace=0.12)

    axes[0].plot(t, raw, color=C["dark"], linewidth=0.35)
    axes[0].plot(t, periodic, color=C["blue"], linewidth=0.7)
    axes[0].set_ylabel("Raw")
    axes[0].text(0.01, 0.92, 'A', transform=axes[0].transAxes, fontweight='bold')

    axes[1].fill_between(t, 0, periodic, color=C["blue"], alpha=0.25)
    axes[1].plot(t, periodic, color=C["blue"], linewidth=0.7)
    axes[1].set_ylabel("Periodic")
    axes[1].text(0.01, 0.92, 'B', transform=axes[1].transAxes, fontweight='bold')

    axes[2].fill_between(t, 0, residual, color=C["red"], alpha=0.25)
    axes[2].plot(t, residual, color=C["red"], linewidth=0.35)
    axes[2].set_ylabel("Residual")
    axes[2].set_xlabel("Time (hours)")
    axes[2].text(0.01, 0.92, 'C', transform=axes[2].transAxes, fontweight='bold')

    save_pub(fig, "decomposition")
