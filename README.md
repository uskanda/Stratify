# Stratify ファイル整理スクリプト

ファイル名の正規表現パターンに基づいてファイルを自動的に整理・移動するPythonスクリプトです。

## 概要

このスクリプトは指定されたディレクトリ内のファイルを、CSV形式のルールファイルに定義された正規表現パターンに従って、対応するディレクトリに移動します。処理内容はログファイルに記録されます。

## 機能

- CSVルールファイルの読み込み
- 正規表現によるファイル名のパターンマッチング
- マッチしたファイルの指定ディレクトリへの移動
- 処理内容のログ記録

## 必要条件

- Python 3.6以上
- 権限:
  - ターゲットディレクトリの読み取り権限
  - ログファイル書き込み権限（`/var/log/`へのアクセス権）
  - 移動先ディレクトリの書き込み権限

## インストール

1. Pythonスクリプトをダウンロードまたはコピー
2. 必要に応じて定数を編集（詳細は下記参照）

## 設定

スクリプト内の以下の定数を適宜変更してください：

```python
RULES_FILE = "rules.csv"        # 移動ルールファイルのパス
TARGET_DIR = "/path/to/target_directory"  # 処理対象のディレクトリ
LOG_FILE = "/var/log/file_transfer.log"  # ログファイルのパス
```

## ルールファイルの形式

CSVファイルを使用し、以下の2つのカラムが必要です：

| カラム名 | 説明 |
|---------|-----|
| regexp | ファイル名にマッチする正規表現パターン |
| dist | ファイルの移動先ディレクトリパス |

### ルールファイルの例

```csv
regexp,dist
.*\.txt$,./text_files
.*\.jpg$,./images
^data_.*\.csv$,./data_files
.*\.log$,./logs
```

この例では：
- `.txt`で終わるファイルは`./text_files`ディレクトリに移動
- `.jpg`で終わるファイルは`./images`ディレクトリに移動
- `data_`で始まり`.csv`で終わるファイルは`./data_files`ディレクトリに移動
- `.log`で終わるファイルは`./logs`ディレクトリに移動

## 使用方法

```bash
python file_organizer.py
```

## ログ

処理内容は`/var/log/file_transfer.log`に記録されます。ログには以下の情報が含まれます：

- 処理開始/終了時間
- 読み込んだルール数
- 各ルールの処理状況
- 移動したファイル名と移動先
- 発生したエラー情報

### ログ例

```
2024-01-01 10:00:00,123 - INFO - ルールファイルを読み込みました: 3件のルール
2024-01-01 10:00:00,456 - INFO - ルール 1 を処理開始: 正規表現='.*\.txt$', 移動先='./text_files'
2024-01-01 10:00:00,789 - INFO - ファイルを移動しました: /target/sample.txt -> ./text_files/sample.txt
```

## 注意事項

- 移動先ディレクトリは自動的に作成されます
- 同名ファイルが移動先に存在する場合、上書きされる可能性があります
- 正規表現はファイル名に対してのみ適用されます（ディレクトリパスは対象外）
- ログファイルの書き込み権限がない場合、スクリプトはエラーになります

## エラーハンドリング

スクリプトは以下のエラーを検知し、ログに記録します：

- ルールファイルが見つからない場合
- 正規表現の構文エラー
- ファイル移動時のIOエラー
- その他の予期しないエラー

エラー発生時は処理を中断し、エラーメッセージをコンソールに表示します。

## ライセンス
Copyright 2025 uskanda

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
