"""公開した NCG2 の回路を CLI で評価し、真理値表と照合する。"""

import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ncg2", nargs="?", default="ncg2")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    binary = Path(args.ncg2)
    ncg2 = str(binary.resolve()) if binary.is_file() else args.ncg2
    project = ["--project", "circuitgame2.toml"]
    subprocess.run([ncg2, "check", *project], cwd=root, check=True)

    # library-probe は左入力の否定、論理積、論理和、排他的論理和の順に出力する。
    truth_table = {"00": "1000", "01": "1011", "10": "0011", "11": "0110"}
    for inputs, expected in truth_table.items():
        result = subprocess.run(
            [ncg2, "eval", "--func", "::library-probe", "--input", inputs, *project],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            raise SystemExit(f"入力 {inputs} の評価に失敗した。\n{result.stderr}")
        actual = result.stdout.strip()
        if actual != expected:
            raise SystemExit(f"入力 {inputs} は {expected} を期待したが、{actual!r} を得た。")
    print(f"{len(truth_table)} 通りの入力を確認した。")


if __name__ == "__main__":
    main()
