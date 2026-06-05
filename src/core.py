import csv
import plistlib
import os

def convert_dictionary(file_path, output_dir=None, make_mac=True, make_win=True):
    """TSV/CSVファイルを読み込み、指定されたOS向けの辞書を出力する関数"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    # どちらもチェックされていない場合は何もしない
    if not make_mac and not make_win:
        return None, None

    base_dir = output_dir if output_dir else os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    user_dictionary = []
    delimiter = '\t' if file_path.endswith('.tsv') else ','
    
    # 1. ファイルの読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if not row or len(row) < 2:
                continue
            shortcut = row[0].strip()
            phrase = row[1].strip()
            
            if shortcut in ['よみ', 'shortcut'] or phrase in ['単語', 'phrase']:
                continue
            user_dictionary.append({'phrase': phrase, 'shortcut': shortcut})

    output_plist = None
    output_win = None

    # 2. 【Mac用】チェックがある場合のみソートして書き出し
    if make_mac:
        user_dictionary.sort(key=lambda x: x['shortcut'])
        output_plist = os.path.join(base_dir, f"{base_name}.plist")
        with open(output_plist, 'wb') as fp:
            plistlib.dump(user_dictionary, fp, fmt=plistlib.FMT_XML)

    # 3. 【Windows用】チェックがある場合のみ書き出し
    if make_win:
        output_win = os.path.join(base_dir, f"{base_name}_windows.txt")
        with open(output_win, 'w', encoding='shift_jis', errors='ignore') as f:
            for entry in user_dictionary:
                f.write(f"{entry['shortcut']}\t{entry['phrase']}\t名詞\n")

    return output_plist, output_win