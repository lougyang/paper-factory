"""Verify all SpecFlow ablation configs: paths, switches, syntax.

Checks:
  1. CKPT_SAVE_DIR uses absolute path → won't leak to HyperD
  2. Ablation switches are internally consistent
  3. Python syntax is valid
"""
import os, sys, py_compile, re

ROOT = r'D:\Code\Claude\Claude_WorkPlace\SpecFlow'
ABL_DIR = os.path.join(ROOT, 'configs', 'pems04', 'ablations')
SPECFLOW_CKPT = os.path.join(ROOT, 'checkpoints', 'SpecFlow')

# Cross-dataset configs
CROSS_DIRS = {
    'PEMS03': os.path.join(ROOT, 'configs', 'pems03', 'ablations'),
    'PEMS07': os.path.join(ROOT, 'configs', 'pems07', 'ablations'),
    'PEMS08': os.path.join(ROOT, 'configs', 'pems08', 'ablations'),
}

# Expected ablation semantics per config name
# (config_name_keyword, expected_params)
ABLATION_RULES = {
    'C1_no_split':      {'spatial_split': False, 'spatial_type': 'svd', 'no_spatial_freq': False,
                         'use_smp': True, 'use_time_cmlp': True},
    'C3_no_flowgraph':  {'spatial_split': False, 'use_smp': False, 'no_spatial_freq': False,
                         'use_time_cmlp': True},
    'C5_no_spatial':    {'no_spatial_freq': True, 'use_smp': True},
    'F3_spatialOnly':   {'spatial_split': False, 'no_spatial_freq': False,
                         'use_time_cmlp': False, 'use_temporal_svd': False},
    'F2_noFreq':        {'no_spatial_freq': True, 'use_time_cmlp': False,
                         'use_temporal_svd': False, 'use_smp': True},
    'F1_noSpatial':     {'no_spatial_freq': True, 'use_time_cmlp': False,
                         'use_temporal_svd': True, 'temporal_svd_k': 2},
}

errors = []
warnings = []

def check_config(filepath, name, is_cross=False):
    """Check a single config file."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # 1. Check CKPT_SAVE_DIR uses absolute or SpecFlow-relative
    ckpt_matches = re.findall(r"CKPT_SAVE_DIR\s*=\s*os\.path\.join\(([^)]+)\)", content)
    for m in ckpt_matches:
        # Extract the path components
        parts = re.findall(r"'([^']*)'", m)
        if parts and not parts[0].startswith('D:'):
            path_str = '/'.join(parts)
            # Check if it's relative — will end up in HyperD due to chdir
            warnings.append(f"{name}: CKPT_SAVE_DIR is relative ({path_str}) → will save under HyperD/")

    # 2. Check if NO_SPATIAL_FREQ and SPLIT are consistent
    has_no_spatial = 'no_spatial_freq' in content and '"no_spatial_freq": True' in content
    has_split_true = '"spatial_split": True' in content
    if has_no_spatial and has_split_true:
        warnings.append(f"{name}: no_spatial_freq=True but spatial_split=True (split irrelevant when skipped)")

    # 3. Check specific ablation rules that MUST be explicitly set
    #    (defaults like no_spatial_freq=False are handled by getattr in code)
    for rule_name, expected in ABLATION_RULES.items():
        if rule_name in name:
            for key, val in expected.items():
                if isinstance(val, bool):
                    true_pat = f'"{key}": True'
                    false_pat = f'"{key}": False'
                    # Only flag if the WRONG value is explicitly written
                    if val and false_pat in content:
                        errors.append(f"{name}: has {key}=False, expected True (rule {rule_name})")
                    if not val and true_pat in content:
                        errors.append(f"{name}: has {key}=True, expected False (rule {rule_name})")
                else:
                    # For non-boolean, check if a conflicting value is set
                    pat = f'"{key}": '
                    if pat in content:
                        # Extract the value and compare
                        m = re.search(rf'"{key}": (\S+)', content)
                        if m:
                            actual = m.group(1).rstrip(',')
                            expected_str = str(val)
                            if actual != expected_str and actual != f'"{expected_str}"':
                                errors.append(f"{name}: {key}={actual}, expected {val} (rule {rule_name})")

    # 4. Syntax check
    try:
        py_compile.compile(filepath, doraise=True)
    except py_compile.PyCompileError as e:
        errors.append(f"{name}: SYNTAX ERROR: {e}")


# Scan all configs
all_configs = []

# PEMS04 ablations
for f in sorted(os.listdir(ABL_DIR)):
    if f.endswith('.py') and f != '__init__.py' and f != 'generate.py':
        all_configs.append((os.path.join(ABL_DIR, f), f.replace('.py', ''), False))

# Cross-dataset
for ds, d in CROSS_DIRS.items():
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith('.py') and f != '__init__.py':
                all_configs.append((os.path.join(d, f), f'{ds}_{f.replace(".py", "")}', True))

print(f"Checking {len(all_configs)} configs...\n")

for filepath, name, is_cross in all_configs:
    check_config(filepath, name, is_cross)

if errors:
    print(f"\n{'='*60}")
    print(f"  ERRORS ({len(errors)}):")
    print(f"{'='*60}")
    for e in errors:
        print(f"  ✗ {e}")

if warnings:
    print(f"\n{'='*60}")
    print(f"  WARNINGS ({len(warnings)}):")
    print(f"{'='*60}")
    for w in warnings:
        print(f"  ⚠ {w}")

if not errors and not warnings:
    print("  All configs OK!")

print(f"\n  Total: {len(all_configs)} configs, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
