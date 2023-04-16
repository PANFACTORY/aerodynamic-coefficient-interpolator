# aerodynamic-coefficient-interpolator
空力係数補間プログラム  
[![Build](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/actions/workflows/build.yml/badge.svg)](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/actions/workflows/build.yml) 
[![Python CI](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/actions/workflows/python-ci.yml/badge.svg)](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/actions/workflows/python-ci.yml)

## 使用方法
### セットアップ
事前に`XFoil`をインストールしておいてください。  
[リリースページ](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/releases)から`interpolator.exe`をダウンロードしてください。  

### 実行方法
以下のコマンドを実行してください。

```
$ interpolator "翼根翼型ファイル名" "翼端翼型ファイル名" "出力ファイル名"
```

プログラムが正常に動作すると以下の様な出力が表示され、空力係数補間関数の係数が`csv`形式でファイルに出力されます。

```
----------Program start----------
  [####################################]  100%
Successfully.
-----------Program end-----------
```

### 環境変数
パラメータは環境変数で指定できます。  

|環境変数名|意味|デフォルト値|
|:--:|:--:|:--:|
|XFOIL_PATH|XFoil.exeのパス|./xfoil.exe|
|PARTITION|翼型混合率分割数|10|
|ALPHA_MIN|最小迎角\[deg\]|0|
|ALPHA_MAX|最大迎角\[deg\]|10|
|ALPHA_STEP|迎角刻み幅\[deg\]|0.1|
|RE_MIN|最小レイノルズ数\[-\]|200000|
|RE_MAX|最大レイノルズ数\[-\]|700000|
|RE_STEP|レイノルズ数刻み幅\[-\]|50000|

これらの値は`.env`ファイルに記載しても適用できます。

```
XFOIL_PATH=path\\to\\xfoil.exe
PARTITION=5
ALPHA_MIN=0
ALPHA_MAX=10
ALPHA_STEP=0.5
RE_MIN=200000
RE_MAX=700000
RE_STEP=100000
```

`.env`ファイルはリポジトリのルートディレクトリか`interpolator.exe`と同じディレクトリに配置してください。

## 開発者向け情報
### セットアップ
リポジトリをクローンした後、`src`ディレクトリに以下の内容で`_version.py`という名前のファイルを作成してください。

```python
VERSION = "develop version"
```

リポジトリ直下のディレクトリに`xfoil.exe`を配置してください。  
`requirements.txt`を用いて依存ライブラリをインストールしてください。  

### 実行方法
[Visual Studio Code](https://code.visualstudio.com/)を利用する場合は  

```
実行とデバッグ > Python: interpolator
```

で実行できます。  
コマンドラインで実行する際にはリポジトリ直下のディレクトリで以下を実行してください。

```
python -m src "翼根翼型ファイル名" "翼端翼型ファイル名" "出力ファイル名"
```

## 依存関係
### プログラム
- [XFoil](https://web.mit.edu/drela/Public/web/xfoil/)

### Pythonパッケージ
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [click](https://github.com/pallets/click)

## ライセンス
- [BSD 3](LICENSE)