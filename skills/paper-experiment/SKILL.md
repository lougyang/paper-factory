# Paper Experiment — 实验流水线

消融实验全流程自动化。从 config 创建到结果 CSV，一步到位。

## 工作流

```
设计实验矩阵 → 生成 config → 验证开关 → 顺序运行 → 自动记录 CSV → 分析汇总
```

## 快速使用

```
/paper-experiment 基于 C1 基线设计空间频域消融实验
数据集 PEMS04, 变量 svd_k=[4,6,8,12,16]
```

Skill 自动：
1. 读取基线 config，复制并修改变量
2. 运行 `verify_configs.py` 检查所有消融开关
3. 顺序启动训练（PYTHONPATH 自动注入）
4. 每个实验完成后解析日志 → 写入 CSV
5. 跑完后打印汇总表，按 best_test 排序

## Config 生成

基于模板 config 批量生成变体：

```python
for k in [4, 6, 8, 12, 16]:
    cfg = copy_baseline()
    cfg["svd_k"] = k
    cfg["CKPT_SAVE_DIR"] = f".../C1_svd_k{k}_100_12_12"
    write_config(cfg, f"C1_svd_k{k}.py")
```

## 关键规则

- CKPT_SAVE_DIR 必须用绝对路径（避免 os.chdir 导致的路径泄漏）
- PYTHONPATH 必须注入项目根目录
- 每个 config 必须通过验证才能运行
- 实验结果三值记录：best_test / test_metrics.json / best_val

## 结果 CSV 格式

```
tag, group, purpose, best_test, tm_mae, best_val, fpe, h3, h6, h12
```

## 模板

`references/` 下有完整的 verify / run 脚本模板。
