"""
SpecFlow — 全部待跑实验, 按逻辑分组, 自动记录结果到 CSV.

Group 1: STFE 骨架补全 (1)
Group 2: 空间频域 k 扫参底限 (2)
Group 3: 图特征注入消融 (1)
Group 4: FPE 秩(r) 扫参 (2)
Group 5: 辅助损失权重扫参 (5)
Group 6: 跨数据集空间频域验证 (6)
------------------------------------------------
Total: 17 experiments
"""
import subprocess, sys, os, time, csv, json, re, glob
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
_run_training = r"D:\Code\Claude\Claude_WorkPlace\HyperD\_run_training.py"
CSV_PATH = os.path.join(ROOT, "results", "experiments.csv")
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

# ── Experiment manifest ──
# (tag, config_rel_path, group, purpose)
MANIFEST = [
    ("F3_spatialOnly",
     "configs/pems04/ablations/F3_spatialOnly_noTemporal.py",
     "STFE骨架2x2",
     "有空间频域+无时间频域, 完成2x2消融右下角"),

    ("C1_svd_k4",
     "configs/pems04/ablations/C1_svd_k4.py",
     "空间SVD秩扫参",
     "空间频域SVD极端压缩(k=4), 验证154频点最小有效秩"),
    ("C1_svd_k6",
     "configs/pems04/ablations/C1_svd_k6.py",
     "空间SVD秩扫参",
     "空间频域SVD(k=6), 已有tm=18.32, 补完整日志"),

    ("C4_no_graphfeat",
     "configs/pems04/ablations/C4_no_graphfeat.py",
     "图特征消融",
     "验证+A图特征注入对FlowGraph的贡献"),

    ("G1_r_low",
     "configs/pems04/ablations/G1_r_low.py",
     "FPE秩扫参",
     "FPE rank半量(rd=6,rw=12), 验证SVD压缩下限, 基线rd=12,rw=24"),
    ("G2_r_high",
     "configs/pems04/ablations/G2_r_high.py",
     "FPE秩扫参",
     "FPE rank双倍(rd=24,rw=48), 验证SVD是否过参数化"),

    ("H1a_L4_w03",
     "configs/pems04/ablations/H1a_L4_w03.py",
     "L4权重扫参",
     "L4时频交叉损失权重=0.3"),
    ("H1b_L4_w05",
     "configs/pems04/ablations/H1b_L4_w05.py",
     "L4权重扫参",
     "L4时频交叉损失权重=0.5"),
    ("H1c_L4_w10",
     "configs/pems04/ablations/H1c_L4_w10.py",
     "L4权重扫参",
     "L4时频交叉损失权重=1.0"),
    ("H2a_L1_w03",
     "configs/pems04/ablations/H2a_L1_w03.py",
     "L1权重扫参",
     "L1周期监督损失权重=0.3"),
    ("H2b_L1_w05",
     "configs/pems04/ablations/H2b_L1_w05.py",
     "L1权重扫参",
     "L1周期监督损失权重=0.5"),

    ("PEMS08_C1",
     "configs/pems08/ablations/C1_no_split.py",
     "跨数据集空间频域",
     "PEMS08(170节点) 有空间频域基线"),
    ("PEMS08_C5",
     "configs/pems08/ablations/C5_no_spatial_freq.py",
     "跨数据集空间频域",
     "PEMS08(170节点) 砍空间频域, 小图预期Delta=0"),
    ("PEMS03_C1",
     "configs/pems03/ablations/C1_no_split.py",
     "跨数据集空间频域",
     "PEMS03(358节点) 有空间频域基线"),
    ("PEMS03_C5",
     "configs/pems03/ablations/C5_no_spatial_freq.py",
     "跨数据集空间频域",
     "PEMS03(358节点) 砍空间频域, 中图预期Delta略增"),
    ("PEMS07_C1",
     "configs/pems07/ablations/C1_no_split.py",
     "跨数据集空间频域",
     "PEMS07(883节点) 有空间频域基线, 关键实验"),
    ("PEMS07_C5",
     "configs/pems07/ablations/C5_no_spatial_freq.py",
     "跨数据集空间频域",
     "PEMS07(883节点) 砍空间频域, 大图预期Delta最大"),
]

CSV_COLS = ['tag', 'group', 'purpose', 'best_test', 'tm_mae', 'best_val', 'fpe',
            'h3', 'h6', 'h12', 'timestamp', 'config_path']


def extract_result(ckpt_name):
    """Parse checkpoint: return {best_test, tm_mae, best_val, fpe, h3, h6, h12} or None."""
    for base in [os.path.join(ROOT, 'checkpoints', 'SpecFlow'),
                 r'D:\Code\Claude\Claude_WorkPlace\HyperD\checkpoints\SpecFlow']:
        ckpt_path = os.path.join(base, ckpt_name)
        if not os.path.isdir(ckpt_path):
            continue
        hash_dirs = [d for d in os.listdir(ckpt_path) if os.path.isdir(os.path.join(ckpt_path, d))]
        for hd in sorted(hash_dirs, reverse=True):
            hpath = os.path.join(ckpt_path, hd)
            logs = sorted(glob.glob(os.path.join(hpath, 'training_log_*.log')))
            if not logs:
                continue
            best_test = 999; best_val = 999; fpe = 0
            with open(logs[-1], encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if 'Result <test>' in line and 'test/MAE' in line:
                        m = re.search(r'test/MAE: ([\d.]+)', line)
                        if m: best_test = min(best_test, float(m.group(1)))
                    if 'Result <val>' in line:
                        m = re.search(r'val/MAE: ([\d.]+)', line)
                        if m: best_val = min(best_val, float(m.group(1)))
                    if 'FPE-only Test MAE:' in line:
                        m = re.search(r'FPE-only Test MAE: ([\d.]+)', line)
                        if m: fpe = float(m.group(1))
            if best_test >= 999:
                continue
            tm_path = os.path.join(hpath, 'test_metrics.json')
            tm = json.load(open(tm_path)) if os.path.exists(tm_path) else {}
            return {
                'best_test': best_test, 'tm_mae': tm.get('overall', {}).get('MAE'),
                'best_val': best_val, 'fpe': fpe,
                'h3': tm.get('horizon_3', {}).get('MAE'),
                'h6': tm.get('horizon_6', {}).get('MAE'),
                'h12': tm.get('horizon_12', {}).get('MAE'),
            }
    return None


def ckpt_name_from_config(rel_path):
    """Infer checkpoint dir name from config path."""
    base = os.path.basename(rel_path).replace('.py', '')
    ds_tag = ''
    for ds in ['PEMS03', 'PEMS07', 'PEMS08']:
        if ds.lower() in rel_path.lower():
            ds_tag = ds + '_'
            break
    # Map known names
    name_map = {
        'F3_spatialOnly_noTemporal': 'F3_spatialOnly',
        'C1_no_split': 'C1',
        'C5_no_spatial_freq': 'C5',
    }
    short = name_map.get(base, base)
    if ds_tag:
        return f'SpecFlow_{ds_tag}{short}_100_12_12'
    return f'SpecFlow_{short}_100_12_12'


def load_csv():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def get_done_tags():
    return {row['tag'] for row in load_csv()}


def append_csv(tag, group, purpose, result, config_path):
    rows = load_csv()
    found = False
    for row in rows:
        if row['tag'] == tag:
            found = True
            break
    if not found:
        rows.append({})  # placeholder; we rebuild
    # Rebuild with updated values
    new_rows = []
    updated = False
    for row in rows:
        if row.get('tag') == tag:
            row.update({
                'tag': tag, 'group': group, 'purpose': purpose,
                'best_test': f"{result['best_test']:.2f}" if result.get('best_test') else '',
                'tm_mae': f"{result['tm_mae']:.2f}" if result.get('tm_mae') else '',
                'best_val': f"{result['best_val']:.2f}" if result.get('best_val') else '',
                'fpe': f"{result['fpe']:.1f}" if result.get('fpe') else '',
                'h3': f"{result['h3']:.2f}" if result.get('h3') else '',
                'h6': f"{result['h6']:.2f}" if result.get('h6') else '',
                'h12': f"{result['h12']:.2f}" if result.get('h12') else '',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'config_path': config_path,
            })
            updated = True
        new_rows.append(row)
    if not updated:
        new_rows.append({
            'tag': tag, 'group': group, 'purpose': purpose,
            'best_test': f"{result['best_test']:.2f}" if result.get('best_test') else '',
            'tm_mae': f"{result['tm_mae']:.2f}" if result.get('tm_mae') else '',
            'best_val': f"{result['best_val']:.2f}" if result.get('best_val') else '',
            'fpe': f"{result['fpe']:.1f}" if result.get('fpe') else '',
            'h3': f"{result['h3']:.2f}" if result.get('h3') else '',
            'h6': f"{result['h6']:.2f}" if result.get('h6') else '',
            'h12': f"{result['h12']:.2f}" if result.get('h12') else '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'config_path': config_path,
        })
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS)
        writer.writeheader()
        writer.writerows(new_rows)


def verify():
    r = subprocess.run([sys.executable, os.path.join(HERE, 'verify_configs.py')],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode == 0


def print_summary():
    if not os.path.exists(CSV_PATH):
        print("  No results yet.")
        return
    rows = load_csv()
    groups = {}
    for row in rows:
        groups.setdefault(row['group'], []).append(row)
    print(f"\n{'='*90}")
    print(f"  Results Summary ({len(rows)} experiments)")
    print(f"{'='*90}")
    for g, items in groups.items():
        print(f"\n  [{g}]")
        print(f"  {'Experiment':<30s} {'best':>6s} {'tm':>6s} {'val':>6s} {'FPE':>6s}  {'h3':>6s} {'h6':>6s} {'h12':>6s}")
        print(f"  {'-'*78}")
        for r in items:
            print(f"  {r['tag']:<30s} {r['best_test']:>6s} {r['tm_mae']:>6s} {r['best_val']:>6s} {r['fpe']:>6s}  {r['h3']:>6s} {r['h6']:>6s} {r['h12']:>6s}")


if __name__ == '__main__':
    print("=" * 90)
    print("  SpecFlow — Complete Ablation Suite")
    print("=" * 90)
    print(f"  {len(MANIFEST)} experiments, 5 groups")
    print(f"  Results: {CSV_PATH}")
    print()

    for tag, rel, group, purpose in MANIFEST:
        if not os.path.exists(os.path.join(ROOT, rel)):
            print(f"  X MISSING: {tag} ({rel})")
            sys.exit(1)
    print(f"  OK All {len(MANIFEST)} configs found")

    if not verify():
        print("  X Verification failed.")
        sys.exit(1)
    print(f"  OK Verification passed\n")

    done_tags = get_done_tags()
    if done_tags:
        print(f"  Resuming: {len(done_tags)} done, {len(MANIFEST)-len(done_tags)} remaining\n")

    for i, (tag, rel, group, purpose) in enumerate(MANIFEST):
        if tag in done_tags:
            continue
        print(f"\n{'='*60}")
        print(f"  [{i+1}/{len(MANIFEST)}] {tag}  [{group}]")
        print(f"  {purpose}")
        print(f"{'='*60}")
        t0 = time.time()
        env = os.environ.copy()
        env['PYTHONPATH'] = ROOT + os.pathsep + env.get('PYTHONPATH', '')
        ret = subprocess.run([sys.executable, _run_training, rel, "0"], env=env)
        elapsed = time.time() - t0
        if ret.returncode != 0:
            print(f"  FAILED ({elapsed/60:.0f}m)")
            continue
        print(f"  Done ({elapsed/60:.0f}m). Extracting...")
        ckpt_name = ckpt_name_from_config(rel)
        result = extract_result(ckpt_name)
        if result:
            append_csv(tag, group, purpose, result, rel)
            print(f"  best_test={result['best_test']:.2f}  tm={result.get('tm_mae') or '?':.2f}  "
                  f"best_val={result['best_val']:.2f}  FPE={result['fpe']:.1f}")
        else:
            print(f"  WARNING: no results for {ckpt_name}")

    print_summary()
    print(f"\n  Done. Results: {CSV_PATH}")
