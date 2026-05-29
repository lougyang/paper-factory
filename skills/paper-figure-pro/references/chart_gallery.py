"""
Paper Figure Pro — 图表类型库 (Chart Gallery)

每种图：用途说明 + 何时用 + 完整可跑示例。用户选风格，AI 改代码适配。

用法：复制需要的函数，替换数据，跑。
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── 论文级全局样式 ──────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "SimSun", "STSong"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 10,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

C = {
    "blue": "#2E86AB", "red": "#D16666", "orange": "#E07A30",
    "green": "#27AE60", "gray": "#7BA3B0", "dark": "#404040",
    "purple": "#8E44AD", "light": "#A8C5D0",
}

OUTDIR = "./figures"


# ═══════════════════════════════════════════════════════
# 1. 水平柱状图 — 消融实验对比
#    何时用：比较多个变体的 MAE/精度，基线用竖虚线标注
# ═══════════════════════════════════════════════════════

def ablation_hbar(labels, values, baseline=None, title="Ablation Study"):
    """
    labels:   ["Z0 Baseline", "No FPE", "No STFE", "No FlowGraph"]
    values:   [18.31, 24.62, 20.64, 18.47]
    baseline: 18.31 (optional reference line)
    """
    fig, ax = plt.subplots(figsize=(6, 3.5))
    colors_list = [C["orange"] if v == min(values) else C["blue"] for v in values]
    ax.barh(range(len(labels)), values, height=0.55, color=colors_list,
            edgecolor='white', linewidth=0.4)
    if baseline:
        ax.axvline(baseline, color=C["orange"], linestyle='--', alpha=0.5,
                   label=f'Baseline ({baseline})')
        ax.legend(fontsize=8)
    for i, v in enumerate(values):
        ax.text(v + 0.1, i, f'{v:.2f}', va='center', fontsize=9, fontweight='bold')
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("MAE", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 2. 精度-参数量散点图
#    何时用：你的模型 vs 其他 baseline，展示 Pareto 前沿
# ═══════════════════════════════════════════════════════

def param_scatter(models, title="Parameter Efficiency"):
    """
    models: [("Name", MAE, params_K, is_ours?)]
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, mae, params, is_ours in models:
        size = 150 if is_ours else 80
        color = C["orange"] if is_ours else C["gray"]
        edge = C["orange"] if is_ours else 'white'
        lw = 2 if is_ours else 0.5
        z = 3 if is_ours else 2
        ax.scatter(params, mae, s=size, c=color, edgecolors=edge,
                   linewidth=lw, zorder=z)
        offset_y = 0.03 if is_ours else -0.03
        ax.annotate(name, (params + 30, mae + offset_y), fontsize=9,
                    fontweight='bold' if is_ours else 'normal',
                    color=C["orange"] if is_ours else '#555')
    ax.set_xlabel("Parameters (K)", fontsize=10)
    ax.set_ylabel("MAE", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 3. 双Y轴图 — 损失权重/超参数分析
#    何时用：两个相关但量级不同的指标，展示 trade-off
# ═══════════════════════════════════════════════════════

def dual_axis(configs, maes, fpes, title="Loss Weight Analysis"):
    """
    configs: ["w=0", "w=0.1", "w=0.3", "w=0.5", "w=1.0"]
    maes:    [18.40, 18.35, 18.37, 18.38, 18.39]
    fpes:    [29.2, 26.90, 24.90, 24.50, 24.30]
    """
    fig, ax1 = plt.subplots(figsize=(6, 3.5))
    x = np.arange(len(configs))
    ax1.bar(x, maes, 0.38, color=[C["orange"] if i == 1 else C["gray"] for i in range(len(x))])
    ax1.set_ylabel("Overall MAE", fontsize=10, color='#333')
    for i, v in enumerate(maes):
        ax1.text(i, v + 0.005, f'{v:.2f}', ha='center', fontsize=8, fontweight='bold')
    ax2 = ax1.twinx()
    ax2.plot(x, fpes, color=C["red"], linewidth=1.5, marker='s', markersize=6,
             markerfacecolor='white', markeredgewidth=1.2)
    ax2.set_ylabel("FPE MAE", fontsize=10, color=C["red"])
    for i, v in enumerate(fpes):
        ax2.text(i, v - 1, f'{v:.1f}', ha='center', fontsize=8, color=C["red"])
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=9)
    ax1.set_title(title, fontsize=11, fontweight='bold', loc='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 4. 分组柱状图 — 多步预测 / 多模型对比
#    何时用：不同 horizon 或不同模型在每个条件下对比
# ═══════════════════════════════════════════════════════

def grouped_bars(groups, data, title="Horizon-wise Error"):
    """
    groups: ["15 min", "30 min", "60 min"]
    data:   {"Ours": [17.5, 18.4, 19.6], "Baseline": [17.5, 18.4, 19.6]}
    """
    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = np.arange(len(groups))
    width = 0.25
    colors_list = [C["orange"], C["blue"], C["gray"], C["green"]]
    for i, (name, vals) in enumerate(data.items()):
        offset = (i - (len(data)-1)/2) * width
        ax.bar(x + offset, vals, width, label=name, color=colors_list[i % len(colors_list)],
               edgecolor='white', linewidth=0.4)
        for j, v in enumerate(vals):
            ax.text(x[j] + offset, v + 0.1, f'{v:.2f}', ha='center', fontsize=7, rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=9)
    ax.set_ylabel("MAE", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    ax.legend(fontsize=8, ncol=len(data))
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 5. 收敛曲线 — 训练过程
#    何时用：对比不同初始化/优化器的收敛速度和最终精度
# ═══════════════════════════════════════════════════════

def convergence(logs, title="Training Convergence"):
    """
    logs: [(epochs, val_mae, label, color), ...]
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    # Panel A: Full convergence
    ax = axes[0]
    for epochs, vals, label, color in logs:
        ax.plot(epochs, vals, color=color, linewidth=1.0, label=label)
    ax.set_xlabel("Epoch", fontsize=9)
    ax.set_ylabel("Validation MAE", fontsize=9)
    ax.legend(fontsize=8)
    ax.text(0.02, 0.95, 'A', transform=ax.transAxes, fontweight='bold')
    # Panel B: Early zoom (first 15 epochs)
    ax = axes[1]
    for epochs, vals, label, color in logs:
        ax.plot(epochs[:15], vals[:15], color=color, linewidth=1.2,
                marker='o', markersize=3, label=label)
    ax.set_xlabel("Epoch", fontsize=9)
    ax.set_ylabel("MAE (first 15 epochs)", fontsize=9)
    ax.legend(fontsize=8)
    ax.text(0.02, 0.95, 'B', transform=ax.transAxes, fontweight='bold')
    fig.suptitle(title, fontsize=11, fontweight='bold', x=0.01, ha='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 6. SVD 奇异值衰减 — 柱+累计折线
#    何时用：展示矩阵低秩特性，证明 SVD 压缩有效
# ═══════════════════════════════════════════════════════

def svd_decay(S, cutoff=12, title="Singular Value Decay"):
    """
    S: singular values array
    cutoff: rank threshold to highlight
    """
    fig, ax1 = plt.subplots(figsize=(6, 3.5))
    cumsum = np.cumsum(S) / np.sum(S)
    colors_sv = [C["blue"] if i < cutoff else C["gray"] for i in range(len(S))]
    ax1.bar(range(1, len(S)+1), S / S[0], width=0.6, color=colors_sv, edgecolor='white')
    ax1.set_xlabel("Singular value index", fontsize=10)
    ax1.set_ylabel("Normalized value", fontsize=10, color=C["blue"])
    ax1.axvline(cutoff + 0.5, color=C["red"], linestyle='--', linewidth=0.8)
    ax1.text(cutoff + 0.8, 0.85, f'r={cutoff}', fontsize=9, color=C["red"], fontweight='bold')
    ax2 = ax1.twinx()
    ax2.plot(range(1, len(S)+1), cumsum * 100, color=C["red"], linewidth=1.2,
             marker='o', markersize=3)
    ax2.set_ylabel("Cumulative energy (%)", fontsize=10, color=C["red"])
    ax1.set_title(title, fontsize=11, fontweight='bold', loc='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 7. 信号分解图 — 三行堆叠 (raw / periodic / residual)
#    何时用：展示周期性+残差分解，motivation 图
# ═══════════════════════════════════════════════════════

def decomposition(t, raw, periodic, residual, title="Signal Decomposition"):
    """
    t: time axis
    raw, periodic, residual: signals of same length
    """
    fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
    fig.subplots_adjust(hspace=0.12)
    # Panel A
    axes[0].plot(t, raw, color=C["dark"], linewidth=0.4, alpha=0.9, label='Observed')
    axes[0].plot(t, periodic, color=C["blue"], linewidth=0.8, label='Periodic fit')
    axes[0].set_ylabel("Norm. flow", fontsize=9)
    axes[0].legend(fontsize=8, ncol=2)
    axes[0].text(0.01, 0.92, 'A', transform=axes[0].transAxes, fontweight='bold')
    # Panel B
    axes[1].fill_between(t, 0, periodic, color=C["blue"], alpha=0.2)
    axes[1].plot(t, periodic, color=C["blue"], linewidth=0.8)
    axes[1].set_ylabel("Periodic", fontsize=9)
    axes[1].text(0.01, 0.92, 'B', transform=axes[1].transAxes, fontweight='bold')
    # Panel C
    axes[2].fill_between(t, 0, residual, color=C["red"], alpha=0.2)
    axes[2].plot(t, residual, color=C["red"], linewidth=0.4)
    axes[2].axhline(0, color='gray', linewidth=0.3)
    axes[2].set_ylabel("Residual", fontsize=9)
    axes[2].set_xlabel("Time (hours)", fontsize=9)
    axes[2].text(0.01, 0.92, 'C', transform=axes[2].transAxes, fontweight='bold')
    fig.align_ylabels()
    fig.suptitle(title, fontsize=11, fontweight='bold', x=0.01, ha='left')
    return fig


# ═══════════════════════════════════════════════════════
# 8. 实验矩阵状态图 — 完成/待跑概览
#    何时用：跑实验前看一眼全局状态
# ═══════════════════════════════════════════════════════

def experiment_matrix(groups, title="Experiment Matrix"):
    """
    groups: {"Group Name": [("exp_tag", value_or_None, is_done?), ...]}
    """
    fig, ax = plt.subplots(figsize=(12, 0.35 * sum(len(v)+0.3 for v in groups.values())))
    y = 0
    for gname, items in groups.items():
        for tag, val, done in items:
            color = C["blue"] if done else '#E0E0E0'
            edge = '#1a5276' if done else '#bbb'
            ax.barh(y, 1, height=0.65, color=color, edgecolor=edge, linewidth=0.5)
            label = f'{tag}'
            if done and val is not None:
                label += f'  {val:.2f}'
            elif not done:
                label += '  ...'
            ax.text(1.02, y, label, va='center', fontsize=9,
                    color='#2c3e50' if done else '#999',
                    fontweight='bold' if (done and val == min(
                        [v for _, v, d in items if d and v is not None], default=0
                    )) else 'normal')
            y += 1
        y += 0.3
    ypos = 0
    for gname, items in groups.items():
        ax.text(-0.08, ypos + len(items)/2 - 0.5, gname, ha='right', va='center',
                fontsize=10, fontweight='bold', color='#2c3e50')
        ypos += len(items) + 0.3
    ax.set_xlim(0, 1.9); ax.set_yticks([]); ax.axis('off')
    done_n = sum(1 for _, items in groups.items() for _, _, d in items if d)
    total = sum(len(items) for _, items in groups.items())
    ax.set_title(f'{title}  ({done_n}/{total} done)', fontsize=12, fontweight='bold', loc='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 9. 热力图 — 相关性矩阵 / 特征图
#    何时用：展示节点间相关性、注意力权重、特征分布
# ═══════════════════════════════════════════════════════

def heatmap(matrix, row_labels=None, col_labels=None, title="Heatmap"):
    """
    matrix: 2D numpy array
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    plt.colorbar(im, ax=ax, shrink=0.8)
    if row_labels:
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels, fontsize=8)
    if col_labels:
        ax.set_xticks(range(len(col_labels)))
        ax.set_xticklabels(col_labels, fontsize=8, rotation=45, ha='right')
    ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 10. 箱线图 — 多次实验分布
#     何时用：展示多次重复实验的稳定性/方差
# ═══════════════════════════════════════════════════════

def boxplot(data, labels, title="Experiment Distribution"):
    """
    data: [ [run1, run2, ...], [...] ] per group
    labels: ["Model A", "Model B", ...]
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(data, labels=labels, patch_artist=True, widths=0.5)
    for patch, color in zip(bp['boxes'], [C["blue"], C["orange"], C["green"], C["red"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_ylabel("MAE", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════
# 通用保存
# ═══════════════════════════════════════════════════════

def save(fig, name, outdir=OUTDIR):
    import os; os.makedirs(outdir, exist_ok=True)
    for fmt in ['pdf', 'svg', 'png']:
        fig.savefig(f'{outdir}/{name}.{fmt}', bbox_inches='tight', dpi=300)
    print(f'Saved: {name}.pdf + .svg + .png')


# ═══════════════════════════════════════════════════════
# 使用说明
# ═══════════════════════════════════════════════════════
if __name__ == '__main__':
    print("""
Paper Figure Pro — Chart Gallery
=================================
10 种图类型，每种都有：用途 + 示例代码

1. ablation_hbar()    — 消融柱状图：比较变体 MAE
2. param_scatter()    — 参数量散点图：Pareto 前沿
3. dual_axis()        — 双Y轴：损失权重 trade-off
4. grouped_bars()     — 分组柱：多 horizon 对比
5. convergence()      — 收敛曲线：训练过程
6. svd_decay()        — SVD 衰减：低秩证明
7. decomposition()    — 信号分解：motivation 图
8. experiment_matrix()— 实验矩阵：done/pending 状态
9. heatmap()          — 热力图：相关性/注意力
10. boxplot()         — 箱线图：稳定性/方差

用法：复制函数 → 替换数据 → 跑 → 得 PDF/SVG/PNG
不喜欢的样式告诉 AI：'把蓝色换成绿色' / '字体大一号'
""")
