# Paper LaTeX — 论文写作

> **告诉用户**：把你的模型代码、实验 CSV、图表文件夹路径告诉 AI，
> 它会自动写入 LaTeX 模板、插入图表公式、编译出 .pdf 初稿。
> 默认用计算机学报模板，你也可以指定 IEEE/ACM/NeurIPS 或自己的模板。

## 怎么用

```
# 默认模板（计算机学报 中文）
/paper-latex 模型在 D:/Code/SpecFlow/，实验数据在 results/experiments.csv

# 指定模板
/paper-latex 用 IEEE Trans 模板写英文论文

# 只写某个章节
/paper-latex 重写实验部分，更新图3和图4

# 用自己的模板
/paper-latex 模板在 D:/templates/myconf.cls，写英文论文
```

## 做什么

1. 读取模型代码 → 理解架构，生成方法部分的描述和公式
2. 读取实验 CSV → 生成实验部分的表格和数值
3. 读取图表文件夹 → 自动插入 `\includegraphics{}`
4. 按模板格式写全文：摘要→引言→相关工作→方法→实验→结论
5. XeLaTeX 编译 → 输出 .pdf

## 支持的模板

| 模板 | 语言 | 编译 | 获取方式 |
|------|------|------|---------|
| 计算机学报 cjc.cls | 中文 | XeLaTeX | 内置 / CTAN |
| IEEEtran | 英文 | PDFLaTeX | CTAN |
| ACM acmart | 英文 | PDFLaTeX | CTAN |
| NeurIPS | 英文 | PDFLaTeX | 官网 |
| 自定义 | 任意 | 指定 | 用户提供路径 |

## 章节规则

- 摘要：1句背景 + 1句不足 + 1句本文方法 + 关键数据
- 引言：第1段问题→第2-3段现有工作→第4段贡献→第5段组织
- 方法：问题定义→总体框架→各模块→损失函数。公式用 equation 环境
- 实验：数据集+指标+基线+主结果表+消融+可视化。数据从 CSV 读取
- 结论：总结+未来方向，不重复结果部分

## 参考文献

- 从用户 .bib 加载，`\cite{}` 引用的条目必须存在
- 不虚构任何参考文献
- 支持 bibtex/biblatex

## 编译

```bash
xelatex paper.tex && bibtex paper && xelatex paper.tex && xelatex paper.tex
```

## 联动

- **paper-experiment → 这里**：实验数据自动填入表格
- **paper-figure-pro → 这里**：图路径自动写入
- **paper-latex 内部**：模板缺失时自动下载或使用内置副本

## 语言风格

- 中文：简洁直接，不堆砌车轱辘话，不 AI 排比句
- 英文：Nature-leaning academic English
- 所有数据来自用户文件，所有引用来自用户 .bib

## 适用范围

任何需要写学术论文的方向——不仅是 CS，任何有模板的期刊都可以：
- 中文：计算机学报、软件学报、电子学报、自动化学报
- 英文：IEEE/ACM/NeurIPS/ICLR/ICML/CVPR
- 自定义模板直接支持
