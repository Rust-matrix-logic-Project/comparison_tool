import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import csv
import os
import subprocess
import psutil

class ShutdownTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title("シャットダウンタイマー")
        self.geometry("400x380")
        self.resizable(False, False)

        self.scheduled_time = None
        self.start_time = None
        self.cancelled = False
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())

        ctk.CTkLabel(self, text="シャットダウン時刻 (HH:MM)",
                     font=("MS Gothic", 14)).pack(pady=(30, 6))
        self.time_entry = ctk.CTkEntry(self, placeholder_text="例: 22:00",
                                       width=160, font=("MS Gothic", 18),
                                       justify="center")
        self.time_entry.pack()

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=14)
        self.set_btn = ctk.CTkButton(btn_row, text="セット", width=150,
                                     command=self.set_timer,
                                     font=("MS Gothic", 14))
        self.set_btn.pack(side="left", padx=8)
        self.cancel_btn = ctk.CTkButton(btn_row, text="キャンセル", width=120,
                                        fg_color="#e05c5c", hover_color="#b03030",
                                        command=self.cancel_timer,
                                        font=("MS Gothic", 14), state="disabled")
        self.cancel_btn.pack(side="left", padx=8)

        self.countdown_label = ctk.CTkLabel(self, text="--:--:--",
                                            font=("MS Gothic", 52, "bold"),
                                            text_color="#1a73e8")
        self.countdown_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="",
                                         font=("MS Gothic", 13), text_color="#555")
        self.status_label.pack()

    # ------------------------------------------------------------------
    def set_timer(self):
        raw = self.time_entry.get().strip()
        try:
            t = datetime.strptime(raw, "%H:%M")
        except ValueError:
            messagebox.showerror("入力エラー", "HH:MM 形式で入力してください。\n例: 22:00")
            return

        now = datetime.now()
        target = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)   # 翌日扱い

        self.scheduled_time = target
        self.start_time = now
        self.cancelled = False

        self.set_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.status_label.configure(
            text=f"シャットダウン予定: {target.strftime('%Y-%m-%d %H:%M')}")
        self._tick()

    # ------------------------------------------------------------------
    def _tick(self):
        if self.cancelled or self.scheduled_time is None:
            return

        remaining = self.scheduled_time - datetime.now()
        total_sec = int(remaining.total_seconds())

        if total_sec <= 0:
            self._do_shutdown()
            return

        h = total_sec // 3600
        m = (total_sec % 3600) // 60
        s = total_sec % 60
        self.countdown_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.after(1000, self._tick)

    # ------------------------------------------------------------------
    def _do_shutdown(self):
        self._save_log("実行")
        self.countdown_label.configure(text="00:00:00")
        self.status_label.configure(text="シャットダウン実行中...", text_color="#e05c5c")
        self.update()
        try:
            subprocess.run(["shutdown", "-h", "now"], check=True)
        except Exception as e:
            messagebox.showerror("エラー",
                f"シャットダウンに失敗しました。\n{e}\n\n"
                "sudoers の設定を確認してください。")
        self._reset()

    # ------------------------------------------------------------------
    def cancel_timer(self):
        if not messagebox.askyesno("確認", "タイマーをキャンセルしますか？"):
            return
        self._save_log("キャンセル")
        self.cancelled = True
        self._reset()
        self.countdown_label.configure(text="--:--:--")
        self.status_label.configure(text="キャンセルしました")

    # ------------------------------------------------------------------
    def _reset(self):
        self.scheduled_time = None
        self.start_time = None
        self.set_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

    # ------------------------------------------------------------------
    def _save_log(self, result: str):
        log_dir = "/home/yuki/Desktop/Python/tools/comparison_tool/csv"
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, "shutdown_log.csv")
        file_exists = os.path.isfile(path)
        with open(path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["起動日時", "セット日時", "予定シャットダウン時刻", "記録日時", "結果"])
            writer.writerow([
                self.boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                self.scheduled_time.strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                result,
            ])

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = ShutdownTimer()
    app.run()
