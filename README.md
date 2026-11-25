# circuitgame2-lib

Neknaj Circuit Game 2 の回路と補助関数を、利用側のプロジェクトに組み込めるソースとして配布する。

| ソース | 公開名前空間 | 内容 |
| --- | --- | --- |
| `src/ncg2/logic/gates.ncg2` | `::ncg2lib::logic` | 1 ビットの NOT、AND、OR、XOR を計算する `func` |
| `src/ncg2m/bool/logic.ncg2m` | `::ncg2lib::bool` | 真偽値の NOT、AND、OR、XOR を計算する `defn` |

どちらの名前空間も `not`、`and`、`or`、`xor` を公開する。NOT は引数を一つ、ほかは二つ取る。

## プロジェクトに組み込む

利用するソースをプロジェクトルート内に置き、設定ファイルの `sources` に相対パスを列挙する。たとえば回路ライブラリを `vendor/circuitgame2-lib/` に置くときは、次のように指定する。

```toml
sources = ["main.ncg2", "vendor/circuitgame2-lib/src/ncg2/logic/gates.ncg2"]
```

利用側で `(using nor)` をトップレベルに一度書き、公開した回路を完全修飾名で呼ぶ。

```lisp
(using nor)

(func parity (in left right) (out result)
  (def result (::ncg2lib::logic::xor left right)))
```

上の手順と検査コマンドは、現行の `ncg2` CLI で扱える回路ライブラリが対象。NCG2M の補助関数は段階4の Core で型を検査した。実行結果の確認には段階4の評価器が必要になる。

## ライブラリの検査

`ncg2` と Python 3 を用意して実行する。

```sh
python tests/check_gates.py
```

ルートの `circuitgame2.toml` は回路ライブラリの検査用。別の名前空間から公開回路を参照し、2 ビットの全入力について `ncg2 eval` の出力を真理値表と照合する。利用側に取り込むソースは `src/` の下に置き、検査用のソースは `tests/` に置く。

[名前解決の仕様](https://neknaj.github.io/circuitgame2/docs/names.html) · [関数型言語の仕様](https://neknaj.github.io/circuitgame2/docs/functional-types.html)
