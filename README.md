# aerodynamic-coefficient-interpolator
空力係数補間プログラム

## セットアップ
事前に`XFoil`をインストールしておいてください。  
[リリースページ](https://github.com/PANFACTORY/aerodynamic-coefficient-interpolator/releases)から`interpolator.exe`をダウンロードしてください。

## 実行方法
以下のコマンドを実行してください。

```
$ interpolator path/to/root_foil.dat path/to/tips_foil.dat path/to/out.csv
```

実行時引数の意味は以下の通りです。

|引数|意味|
|:--:|:--:|
|path/to/root_foil.dat|翼根翼型ファイル名|
|path/to/tips_foil.dat|翼端翼型ファイル名|
|path/to/out.csv|出力ファイル名|

## 環境変数
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

## 依存関係
### プログラム
- [XFoil](https://web.mit.edu/drela/Public/web/xfoil/)

### Pythonパッケージ
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)

## ライセンス
- [BSD 3](LICENSE)