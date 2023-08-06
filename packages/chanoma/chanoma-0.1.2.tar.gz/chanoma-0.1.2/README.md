# chanoma

chanoma is Characters Normalization library.
文字列正規化処理用のライブラリです。

[Rust 版](https://crates.io/crates/chanoma) の Python バインディングです。

## 使い方

```python
from chanoma import Chanoma

def main():
    chanoma = Chanoma(preset=True)
    print(chanoma.normalize("ﾊﾝｶｸｶﾅは全角カタカナに変換されます"))

if __name__ == '__main__':
    main()
```

## インストール

```sh
pip install chanoma
```

## 設定ファイル

chanoma は設定ファイルを配置することで、結果を調整することが可能です。
設定ファイルを読み込ませるための方法は二種類あります。

- 環境変数 `CHANOMARC` に設定ファイルのパスを指定する。
- 以下のパスのうちのどこかにファイルを配置する。
  - `$HOME/.config/chanoma/chanomarc.{ext}`
  - `$HOME/.config/chanoma/.chanomarc.{ext}`
  - `$HOME/chanomarc.{ext}`
  - `$HOME/.chanomarc.{ext}`
  - `$PWD/chanomarc.{ext}`
  - `$PWD/.chanomarc.{ext}`

上記のどちらの場合でも、`.{ext}` に指定可能な拡張子は `.csv`, `.yaml` (`.yml`) のどれかです。

### CSV ファイルの場合のフォーマット

CSV ファイルでは、一文字から一文字の置換のみ設定が可能です。
最初の列に **置換したい文字**、次の列に **置換後の文字** を記述します。

```csv
from,to
＆,&
```

### YAML ファイルの場合のフォーマット

Yaml ファイルでは、一文字から一文字の置換と、Modifier を指定する二種類の方法があります。

#### 一文字から一文字の置換

ルートキーに `items` を記述し、配列指定で `from` キーの値に **置換したい文字**、`to` キーの値に **置換後の文字** を記述します。

```yaml
items:
  - from: "a"
    to: "A"
```

#### Modifier を指定する

ルートキーに `modifiers` を記述し、一段インデントして Modifier をキーとして記述します。
指定できる Modifire は以下です。

- `character_converter` : 一文字から一文字の置換を設定します。キーに **置換したい文字**、値に **置換後の文字** を記述します。( `items` と同様の処理になります。)
- `character_eliminator` : 指定した文字を削除します。
- `consecutive_character_reducer` : 指定した連続する同じ文字を一つにします。
- `dotted_space_eliminator` : 『「半角英数字」と「半角英数字」の間の半角スペース』以外の半角スペースを削除します。
- `ligature_translator` : 指定した合字をくっつけて一文字にします。
- `trim` : 先頭と末尾の半角スペースを削除します。
- `neologdn` : [neologdn](https://github.com/ikegami-yukino/neologdn) と同様の結果になる処理をします。

```yaml
modifiers:
  character_converter:
    a: A
    b: B
  character_eliminator: ["~", ∼, ∾, 〜, 〰, ～]
  consecutive_character_reducer: ー
  dotted_space_eliminator:
  ligature_translator:
    ハ゜: パ
  trim:
  neologdn:
```

## Development

```sh
docker-compose build chanoma
docker-compose run --rm chanoma bash
cd /app/bindings/python3
python3 ./setup.py develop
./run-test.sh
```

## Build

```sh
docker-compose run --rm build-wheels-for-python ./build-wheels.sh
```

## Publish

```sh
docker-compose run --rm chanoma ./bindings/python3/publish_to_pypi.sh
```
