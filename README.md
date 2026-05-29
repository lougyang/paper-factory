# Paper Factory — 论文工厂

一个 AI 编程助手的技能包。从实验到论文初稿，全流程覆盖。

> 用户只需要做实验、提供代码、理解自己的模型。剩下的交给 Paper Factory。

## 论文生产流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  实验流水线   │ →  │  图表绘制     │ →  │  LaTeX 写作  │ →  │  论文初稿     │
│  experiment  │    │  figure-pro   │    │    latex     │    │  .tex + .pdf │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## 四个 Skill

| Skill | 做什么 | 输入 | 输出 |
|-------|--------|------|------|
| **paper-experiment** | 实验流水线 | 基线 config + 变量矩阵 | 全部结果 CSV |
| **paper-figure-pro** | 图表绘制 | 模型结构 + 实验数据 | .vsdx / .pdf / .png |
| **paper-latex** | 论文写作 | 模型代码 + CSV + 图表 | .tex + .pdf |
| **visio-draw** | Visio COM 底层 | 坐标和形状定义 | .vsdx |

## 30 秒安装

```bash
git clone https://github.com/YOUR_NAME/paper-factory.git
cp -r paper-factory/skills/* ~/.claude/skills/
pip install pywin32 matplotlib numpy
```

## 支持的图表类型

架构图 / 消融柱状图 / 精度-参数量散点图 / 多步预测误差图 / 收敛曲线 / SVD 奇异值衰减 / 流量分解图 / 损失权重分析 / 热力图 / 流程图

## 支持的论文模板

| 模板 | 语言 | 编译 |
|------|------|------|
| 计算机学报 (cjc.cls) | 中文 | XeLaTeX |
| IEEE Trans | 英文 | PDFLaTeX |
| ACM | 英文 | PDFLaTeX |
| NeurIPS | 英文 | PDFLaTeX |
| 自定义模板 | 任意 | 任意 |

## 设计原则

- Marshall et al. (2025) — 神经网络架构图证据指南
- Jambor (2025) — 科学图表检查清单 (Nature Cell Biology)
- Crameri et al. (2024) — 科学配色标准
- 格式塔原理 — 邻近、对齐、对称、公共区域

## 系统要求

- Python 3.10+
- matplotlib, numpy, pywin32 (Visio 图需要)
- Windows + Visio 桌面版 (架构图，非必需)
- LaTeX 发行版 (XeLaTeX, 论文写作需要)

## License

MIT — 随便用，注明出处即可。
