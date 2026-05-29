# Paper Experiment — 实验流水线

> **告诉用户**：把你设计好的实验矩阵告诉 AI，它会生成所有 config、验证消融开关、顺序运行、自动记录 CSV、跑完输出分析报告。你只需要写基线 config，其余自动完成。

## 怎么用

```
# 用法 1：给定基线和变量矩阵
/paper-experiment 基于 C1 基线，变量 svd_k=[4,6,8,12,16]，PEMS04 数据集

# 用法 2：只做验证和运行（config 已写好了）
/paper-experiment 跑 configs/pems04/ablations/ 下所有待跑实验

# 用法 3：只看已有结果
/paper-experiment 分析 results/experiments.csv 并输出汇总
```

## 做什么

1. 读取基线 config → 按变量矩阵生成所有变体
2. 运行验证脚本检查每个 config 的消融开关一致性
3. 顺序启动训练（自动注入 PYTHONPATH，处理路径泄漏）
4. 每完成一个实验：解析训练日志 → 提取 best_test、tm_mae、best_val → 写入 CSV
5. 支持断点续跑（已完成的自动跳过）
6. 跑完后按 group 分组输出汇总表

## 输出

`results/experiments.csv`：
```
tag, group, purpose, best_test, tm_mae, best_val, fpe, h3, h6, h12, timestamp
```

## 关键规则

- CKPT_SAVE_DIR 必须绝对路径
- PYTHONPATH 注入项目根目录
- 三值记录：best_test / test_metrics.json / best_val
- 按 best_test 排序，标出最优

## 联动

- **→ paper-figure-pro**：CSV 数据自动生成消融柱状图、参数量散点图
- **→ paper-latex**：实验结果数值自动填入 LaTeX 表格

## 适用范围

不仅限于 ML。任何需要批量跑实验的研究方向：
- 交通预测、CV、NLP → 消融实验
- 生物信息学 → 参数扫参
- 物理模拟 → 条件对比
- 社会科学 → 假设检验
