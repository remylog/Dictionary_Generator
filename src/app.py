import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import convert_dictionary

class DictionaryConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("辞書ジェネレーター")
        self.geometry("500x300") # チェックボックス用に少し高さを広げました
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # 1. メインラベル
        self.label = ctk.CTkLabel(self, text="TSV または CSV ファイルを選択してください", font=("Arial", 14))
        self.label.pack(pady=25)

        # 2. チェックボックスを配置するフレーム（横並び用）
        self.checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame.pack(pady=10)

        # Mac用チェックボックス（初期値: ON）
        self.mac_var = ctk.BooleanVar(value=True)
        self.mac_cb = ctk.CTkCheckBox(self.checkbox_frame, text="Mac用 (.plist)", variable=self.mac_var)
        self.mac_cb.pack(side="left", padx=20)

        # Windows用チェックボックス（初期値: ON）
        self.win_var = ctk.BooleanVar(value=True)
        self.win_cb = ctk.CTkCheckBox(self.checkbox_frame, text="Windows用 (_windows.txt)", variable=self.win_var)
        self.win_cb.pack(side="left", padx=20)

        # 3. ファイル選択ボタン
        self.select_btn = ctk.CTkButton(self, text="ファイルを開く", command=self.select_file)
        self.select_btn.pack(pady=25)

    def select_file(self):
        # チェック状態の取得
        make_mac = self.mac_var.get()
        make_win = self.win_var.get()

        # どちらもチェックされていない場合は警告を出して中断
        if not make_mac and not make_win:
            messagebox.showwarning("警告", "出力するOSを少なくとも1つ選択してください。")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Text/CSV files", "*.tsv;*.csv;*.txt")]
        )
        if file_path:
            self.label.configure(text=f"選択中: {os.path.basename(file_path)}")
            
            try:
                # チェックボックスの状態を引数として渡す
                plist_out, win_out = convert_dictionary(
                    file_path, 
                    make_mac=make_mac, 
                    make_win=make_win
                )
                
                # メッセージの組み立て
                msg = "変換が完了しました！\n同じフォルダに出力されました。\n\n"
                if plist_out:
                    msg += f"・{os.path.basename(plist_out)} (Mac用)\n"
                if win_out:
                    msg += f"・{os.path.basename(win_out)} (Win用)"
                
                messagebox.showinfo("成功", msg)
                
            except Exception as e:
                messagebox.showerror("エラー", f"変換に失敗しました:\n{str(e)}")
            finally:
                self.label.configure(text="TSV または CSV ファイルを選択してください")

if __name__ == "__main__":
    app = DictionaryConverterApp()
    app.mainloop()