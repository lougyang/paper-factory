# Paper Factory — 论文工厂

AI 编程助手技能包。从实验到论文初稿，全流程覆盖。
不限于 Claude Code，任何支持 Skill 的 AI 编程助手都能用。

> 你只需要做实验、提供代码、理解自己的模型。剩下的交给 Paper Factory。

## 论文生产流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  实验流水线   │ →  │  图表绘制     │ →  │  LaTeX 写作  │ →  │  论文初稿     │
│  experiment  │    │  figure-pro   │    │    latex     │    │  .tex + .pdf │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      ↓                     ↓                    ↓
   CSV 自动联动         图路径自动联动        模板自动下载
```

> 也可以不按流程来——缺什么用什么，跳步随便来。

## 四个 Skill

| Skill | 一句话 | 输入 | 输出 |
|-------|--------|------|------|
| **paper-experiment** | 实验矩阵自动跑 | 基线 config + 变量 | 全部结果 CSV + 分析 |
| **paper-figure-pro** | 边聊边画图 | 模型结构/CSV 数据 | .vsdx + .pdf + .svg + .png |
| **paper-latex** | 自动写 LaTeX | 模型代码 + CSV + 图 | .tex + .pdf |
| **visio-draw** | Visio COM 底层 | 坐标和形状 | .vsdx |

## 30 秒安装

```bash
git clone https://github.com/YOUR_NAME/paper-factory.git
cp -r paper-factory/skills/* ~/.claude/skills/
pip install pywin32 matplotlib numpy
```

## 怎么用（告诉用户的，不是告诉模型的）

```
# 1. 跑实验
/paper-experiment 基于 C1 基线，变量 svd_k=[4,6,8,12,16]

# 2. 画图（交互式，不满意就改）
/paper-figure-pro 画消融柱状图，数据用 results/experiments.csv

# 3. 写论文
/paper-latex 模型在 D:/Code/SpecFlow/，实验数据在 results/

# 或者直接一步：给模型代码 + CSV → 出论文初稿
```

## 支持的图表

架构图、消融柱状图、精度-参数量散点图、多步预测误差、收敛曲线、
SVD 衰减、信号分解图、损失权重双Y轴、热力图、流程图、网络拓扑图

## 支持的模板

计算机学报(cjc)、IEEE Trans、ACM、NeurIPS、自定义

## 适用范围

ML/DL、交通预测、生物信息学、物理模拟、社会科学——
任何需要做实验 + 画图 + 写论文的研究方向。

## 设计原则

Marshall 2025 + Jambor 2025 + Crameri 2024 + 格式塔原理

## 系统要求

Python 3.10+ | matplotlib, numpy, pywin32
Windows + Visio(架构图，非必需) | LaTeX(论文写作需要)

## License

MIT
