# Paper Figure Pro — 交互式图表绘制

> **告诉用户**：对着 AI 描述你的模型结构或实验数据，它会边画边问你满不满意。
> "字体大一点""颜色换成蓝色""这个框和那个框对齐"——不满意就继续改。
> 不需要写代码。

## 怎么用

```
# 交互模式（默认）— 一步步确认
/paper-figure-pro 画一个双分支模型架构图

# 快速模式 — 直接一步到位
/paper-figure-pro 直接画，不用确认

# 数据图模式 — CSV 扔进来就出图
/paper-figure-pro 用 results/experiments.csv 画消融柱状图

# 继续改 — 基于上次的图调整
/paper-figure-pro 把 S_out 移到右边，字体再大一号
```

## 交互流程

```
1. 问类型 → 架构图/数据图/热力图/流程图？
2. 问结构 → 几个分支？哪些模块？什么关系？
3. 给布局草稿 → 文字描述 + 坐标，等用户确认
4. 选配色 → 蓝+橙 / 蓝+绿 / 自定义
5. 画图 → Visio COM 逐模块出现
6. 问调整 → "哪里要改？"循环到满意
7. 保存 → .vsdx + .png + .svg + 时间戳备份
```

## 跳步随便来

不强制走完整流程。可以随时跳到任何步骤：
- "直接画，配色我后面再调"
- "只生成 matplotlib 代码，我自己跑"
- "用上次那个配色，换一种布局"
- "我没 Visio，用 Python 画"

## 联动（自动）

- **paper-experiment → 这里**：CSV 扔进来，自动出全部数据图
- **这里 → paper-latex**：图路径自动写进 `\includegraphics{}`

## 能画的图

| 类型 | 工具 |
|------|------|
| 模型架构框架图 | Visio COM / matplotlib patches |
| 消融柱状图 | matplotlib |
| 精度-参数量散点图 | matplotlib |
| 多步预测分组柱状图 | matplotlib |
| 收敛曲线 | matplotlib |
| SVD 奇异值衰减 | matplotlib |
| 信号分解图 | matplotlib |
| 损失权重双Y轴 | matplotlib |
| 热力图 | matplotlib/seaborn |
| 流程图 | Visio COM / matplotlib |
| 网络拓扑图 | matplotlib |

## 设计规则（自动遵守）

**布局**：内容定宽、并行等宽等高同y、邻近模块间距0.2-0.3in、短侧向长侧垂直居中

**线条（刚性）**：单junction≤2出线、并列模块间放junction同y水平展开、同源同向共用干线、进junction无箭头出有箭头

**配色**：2-3色系、容器最淡→内盒中→输出最深、无虚线、不红绿配

**字体**：主体16pt、强调18pt、输出22pt、运算符30pt、标题14pt、最小≥7pt

## 无 Visio 自动降级

matplotlib patches 画架构图。数据图不受影响。

## 适用范围

所有需要画论文图的研究方向：ML/DL、交通/土木、生物/医学、物理/化学、社科/经济
