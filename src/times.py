import customtkinter as ctk
import csv
from datetime import datetime
import os
class TimeCheker(ctk.CTk):
    def __init__(self):
            super().__init__()
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            self.title('打刻管理')
            self.geometry("400x500")
            self.time = datetime.now()
            self.flag = False
            self.button = ctk.CTkButton(self, text="開始", command=self.checker)
            self.button.pack(pady=10)
            self.total = 0
            self.label = ctk.CTkLabel(self, text="")
            self.label.pack(pady=40)
            
    def checker(self):
        if self.flag is False:
            self.start = datetime.now()
            self.button.configure(text="終了")
            self.label.configure(text=f"開始時刻: {self.start}", font=("MS Gothic", 48))
            self.flag = True
            self.update_timer()
        else:
            self.endtime = datetime.now()
            self.total = self.endtime - self.start
            self.save_to_csv()
            self.label.configure(text="")
            self.button.configure(text="開始")
            self.flag = False
        
    def update_timer(self):
        total = datetime.now() - self.start
        self.label.configure(text=str(total).split(".")[0])
        if self.flag:
            self.after(1000, self.update_timer)
            
    
    def save_to_csv(self):
        path = "/home/yuki/Desktop/Python/tools/comparison_tool/csv/time.csv"
        base_dir = os.path.dirname(os.path.abspath( __file__))
        file = os.path.isfile(path)
        os.path.join(base_dir, path)
        with open(path, 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file:
                writer.writerow(["開始日時", "終了日時", "total"])
            start = self.start.strftime("%Y-%m-%d")
            end = self.endtime.strftime("%Y-%m-%d")
            duration = str(self.total).split(".")[0]
            data = [start, end, duration]
            writer.writerow(data)
    def run(self):
        self.mainloop()
        
if __name__ == "__main__":
    timer = TimeCheker()
    timer.run()