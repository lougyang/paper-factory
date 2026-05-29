# Visio Draw — Claude Code Skill

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%2B%20Visio-lightgrey)]()

一条命令画出论文级架构图。直接调用 Microsoft Visio COM API，颜色、字体、连线全部精准控制。

> 抖音教程 / 使用演示：搜索「Claude Code Skill 学术绘图」

## 30 秒安装

```powershell
# 1. 安装 skill
git clone https://github.com/YOUR_NAME/skills-collection.git
cp -r skills-collection/skills/visio-draw $env:USERPROFILE\.claude\skills\visio-draw

# 2. 安装 Python 依赖
pip install pywin32

# 3. 在 Claude Code 中使用
# 输入: /visio-draw 画一个 GPT 模型架构图
```

## 能画什么

| 图类型 | 示例 |
|--------|------|
| 模型架构框架图 | 双分支网络、编码器-解码器、GAN |
| 系统架构图 | 微服务拓扑、数据流水线 |
| 论文模块图 | 深度学习模型结构、消融分支对比 |
| 流程图 | 算法流程、数据处理管道 |

## 为什么不用 Visiomaster / Draw.io / PPT

| 工具 | 问题 |
|------|------|
| Visiomaster | scene.json 渲染器填色丢失、连线乱飞 |
| Draw.io | 手动拖拽费时，无法程序化复用 |
| PPT | 形状有限，学术风格不够 |
| **Visio Draw** | COM 直连，每个像素都可控，一次写好终身复用 |

## 效果展示

见 `examples/` 目录：

```
examples/
  specflow_arch.png    — SpecFlow 双分支频域架构图（计算机学报论文用）
```

运行示例（需要克隆 SpecFlow 项目到同级目录）：

```powershell
python examples/specflow_arch.py
```

## 自定义你的图

复制 `skills/visio-draw/references/draw_template.py`，修改 `LAYOUT` 部分：

```python
# 定义一个矩形
box = R(x=1.0, y=2.0, w=2.5, h=0.8,
        text="My Module", fill=COLORS["fam1_inner"])

# 定义一个圆角矩形
out = RR(x=1.0, y=5.0, w=2.0, h=0.5,
         text="Output", fill=COLORS["fam1_dark"], font_size="15 pt")

# 画一条连线
A(box, out)
```

完整 API 见 SKILL.md。

## 系统要求

- Windows 10/11
- Microsoft Visio 2016+ 桌面版
- Python 3.10+ + pywin32
- Claude Code（或任何支持 Skill 的 AI 编程助手）

## 路线图

- [ ] 更多内置调色板（Nature/Science/NeurIPS 风格）
- [ ] 自动布局引擎
- [ ] LaTeX 公式支持
- [ ] 批量生成实验对比图

## 贡献

欢迎提 PR 或 Issue。如果你有好的配色方案或布局模板，直接发 PR 到 `skills/visio-draw/`。

## License

MIT — 随便用，注明出处即可。
