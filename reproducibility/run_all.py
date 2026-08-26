from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"

commands = [
    [sys.executable, str(CODE / "tests/test_exact_bodies.py")],
    [sys.executable, str(CODE / "tests/test_v020_theorems.py")],
    [sys.executable, str(CODE / "tests/test_v030_input_output.py")],
    [sys.executable, str(CODE / "tests/test_v040_green_tensor.py")],
    [sys.executable, str(CODE / "tests/test_v050_operational_support.py")],
    [sys.executable, str(CODE / "tests/test_v060_freeze.py")],
    [sys.executable, str(CODE / "scripts/generate_figures.py")],
    [sys.executable, str(CODE / "scripts/generate_v020_figures.py")],
    [sys.executable, str(CODE / "scripts/generate_v030_figures.py")],
    [sys.executable, str(CODE / "scripts/generate_v040_green_tensor.py")],
    [sys.executable, str(CODE / "scripts/monte_carlo_check.py")],
    [sys.executable, str(CODE / "scripts/theory_checks_v020.py")],
]

for command in commands:
    print("RUN", " ".join(map(str, command)))
    subprocess.run(command, cwd=CODE, check=True)

print("ALL v1.0.0-rc1 REPRODUCIBILITY CHECKS PASSED")
