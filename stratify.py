import os
import csv
import re
import shutil
import logging
from pathlib import Path

# 定数設定
RULES_FILE = "rules.csv"  # 移動ルールファイルA
TARGET_DIR = "/path/to/target_directory"  # ターゲットディレクトリX
LOG_FILE = "/var/log/file_transfer.log"  # ログファイル

# ログ設定
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def load_rules(rules_file):
    """移動ルールファイルを読み込む"""
    rules = []
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rules.append({
                    'regexp': row['regexp'],
                    'dist': row['dist']
                })
    except FileNotFoundError:
        logging.error(f"ルールファイルが見つかりません: {rules_file}")
        raise
    except Exception as e:
        logging.error(f"ルールファイルの読み込みエラー: {e}")
        raise
    return rules

def find_matching_files(target_dir, pattern):
    """正規表現パターンに一致するファイルを検索する"""
    matching_files = []
    try:
        # 正規表現パターンをコンパイル
        regex = re.compile(pattern)
        
        # ターゲットディレクトリのファイルを走査
        for item in Path(target_dir).iterdir():
            if item.is_file() and regex.search(item.name):
                matching_files.append(item)
    except re.error as e:
        logging.error(f"正規表現のコンパイルエラー: {pattern} - {e}")
        raise
    except Exception as e:
        logging.error(f"ファイル検索エラー: {e}")
        raise
    
    return matching_files

def move_files(files, destination_dir):
    """ファイルを指定のディレクトリに移動する"""
    # 移動先ディレクトリが存在しない場合は作成
    os.makedirs(destination_dir, exist_ok=True)
    
    moved_files = []
    for file_path in files:
        try:
            destination_path = os.path.join(destination_dir, file_path.name)
            shutil.move(str(file_path), destination_path)
            moved_files.append(file_path.name)
            logging.info(f"ファイルを移動しました: {file_path} -> {destination_path}")
        except Exception as e:
            logging.error(f"ファイル移動エラー: {file_path} - {e}")
            continue
    
    return moved_files

def main():
    """メイン処理"""
    try:
        # ルールファイルを読み込む
        rules = load_rules(RULES_FILE)
        logging.info(f"ルールファイルを読み込みました: {len(rules)}件のルール")
        
        # 各ルールを処理
        for i, rule in enumerate(rules, 1):
            regexp = rule['regexp']
            dist = rule['dist']
            
            logging.info(f"ルール {i} を処理開始: 正規表現='{regexp}', 移動先='{dist}'")
            
            # 正規表現に一致するファイルを検索
            matching_files = find_matching_files(TARGET_DIR, regexp)
            logging.info(f"ルール {i} で {len(matching_files)} 件のファイルが見つかりました")
            
            if matching_files:
                # ファイルを移動
                moved_files = move_files(matching_files, dist)
                logging.info(f"ルール {i} で {len(moved_files)} 件のファイルを移動しました")
            else:
                logging.info(f"ルール {i} に一致するファイルはありませんでした")
                
    except Exception as e:
        logging.error(f"処理中にエラーが発生しました: {e}")
        print(f"エラーが発生しました。ログファイルを確認してください: {e}")

if __name__ == "__main__":
    main()
