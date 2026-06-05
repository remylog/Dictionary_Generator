import unittest
import os
import tempfile
import plistlib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import convert_dictionary

class TestDictionaryConverter(unittest.TestCase):
    def setUp(self):
        # テストごとに一時的な作業フォルダを作成
        self.test_dir = tempfile.TemporaryDirectory()
        self.tsv_path = os.path.join(self.test_dir.name, "test_input.tsv")
        
        # テスト用のダミーデータを書き込み（順序をバラバラにする）
        with open(self.tsv_path, 'w', encoding='utf-8') as f:
            f.write("よみ\t単語\n")
            f.write("ねるこ\t神芭ねるこ\n")
            f.write("あやめ\t百鬼あやめ\n")

    def tearDown(self):
        # テスト終了後に一時フォルダを削除
        self.test_dir.cleanup()

    def test_conversion_creates_files(self):
        # ファイルが実際に生成されるか検証
        plist_out, win_out = convert_dictionary(self.tsv_path, output_dir=self.test_dir.name)
        self.assertTrue(os.path.exists(plist_out))
        self.assertTrue(os.path.exists(win_out))

    def test_mac_plist_sorting(self):
        # Mac用plistが正しく五十音順にソートされているか検証
        plist_out, _ = convert_dictionary(self.tsv_path, output_dir=self.test_dir.name)
        with open(plist_out, 'rb') as fp:
            data = plistlib.load(fp)
            self.assertEqual(data[0]['shortcut'], 'あやめ')
            self.assertEqual(data[1]['shortcut'], 'ねるこ')

if __name__ == '__main__':
    unittest.main()