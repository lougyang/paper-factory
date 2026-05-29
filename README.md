# Paper Factory — 论文工厂

> 你写代码跑实验，AI 负责剩下的：实验管理、画图、LaTeX 写作。
> 四个 Skill，一条流水线，一篇论文初稿。

[![Skills](https://img.shields.io/badge/skills-4-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Platform](https://img.shields.io/badge/any%20AI%20agent-skill%20compatible-lightgrey)]()

---

## 论文流水线

```
  实验流水线        图表绘制          LaTeX 写作         论文初稿
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│experiment│ →  │figure-pro│ →  │  latex   │ →  │ .tex+pdf │
│ 自动跑实验 │    │ 边聊边画  │    │ 自动写作  │    │  一键编译  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

> 也可以不按流程——缺什么用什么，跳步随便来。没跑实验也能画图，没画图也能写论文。

---

## 安装

```bash
git clone https://github.com/lougyang/paper-factory.git
cp -r paper-factory/skills/* ~/.claude/skills/
pip install pywin32 matplotlib numpy
```

就这三步。不需要 npm、不需要 npx、不需要注册。Skills 就是文件夹，AI 直接读。

---

## 四个 Skill

### paper-experiment — 实验流水线

```
/paper-experiment 基于 C1 基线，变量 svd_k=[4,6,8,12,16]，PEMS04
```

- 读取基线 config → 生成全部变体
- 自动验证消融开关一致性
- 顺序运行，断点续跑，结果自动写入 CSV
- 跑完输出分组汇总 + 实验矩阵状态图

### paper-figure-pro — 交互式图表

```
/paper-figure-pro 画一个双分支模型架构图
```

- 边聊边画：问类型→问结构→给布局→选配色→画→循环调整到满意
- 支持架构图、消融柱状图、参数量散点图、收敛曲线、SVD衰减、信号分解、热力图、流程图等 10+ 种图
- Visio COM 直连（Windows）或 matplotlib（无 Visio 自动降级）
- 设计规则内置：禁止线条聚集、局部分流、内容定宽、并行对称

### paper-latex — 论文写作

```
/paper-latex 模型在 ./model/，实验数据在 results/experiments.csv，图在 docs/figures/
```

- 默认计算机学报模板（cjc.cls 内置），支持 IEEE/ACM/NeurIPS/自定义
- 读模型代码 → 写方法部分；读 CSV → 写实验表格；读图目录 → 插入图表
- 自动 XeLaTeX 编译输出 .pdf
- 缺数据时不编造，用 `% TODO` 占位

### visio-draw — Visio COM 底层

- 通用矩形/圆角/圆形/连线/配色函数模板
- 复制替换 LAYOUT 部分即可画新图
- 坐标系自动转换（top-left → Visio bottom-left）

---

## 对 AI 说人话就行

```
# 跑实验
/paper-experiment 帮我设计空间频域消融，变量是 svd_k

# 画图
/paper-figure-pro 把刚才的实验结果画成柱状图
/paper-figure-pro 字体大一点，颜色换成蓝色系

# 写论文
/paper-latex 用刚才的实验和图表写方法+实验两个章节
```

---

## 设计原则

Marshall et al. (2025, PLOS ONE) + Jambor (2025, Nature Cell Biology) + Crameri et al. (2024, Current Protocols) + 格式塔原理

- 线条禁止多线聚集，单 junction ≤2 出线
- 配色 2-3 色系，容器→内盒→输出由浅入深
- 字体主体 16pt、输出 22pt、运算符 30pt
- 并行模块等宽等高同 y，短侧向长侧垂直居中

---

## 适用范围

ML/DL、交通预测、生物信息、物理模拟、社会科学——任何需要做实验画图写论文的方向。

---

## License

MIT — 随便用，注明出处。
