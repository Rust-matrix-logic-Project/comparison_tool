from datetime import datetime
import os, csv
from dotenv import load_dotenv
import customtkinter as ctk
load_dotenv()

class Goals(ctk.CTk):
    def __init__(self):
         super().__init__()
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.csv_date = datetime.now().strftime("%Y-%m-%d")
         self.csv_header = ["キー","日付", "第一目標", "第二目標", "第三目標", "第四目標"]
         self.csv_file = f"{self.year}_{self.month}_goals.csv"
         self.date = datetime.now().strftime("%d日")
         self.csv_path = os.environ.get("STUDY_CSV_DIR")
         self.goals = [self.date]
         
         self.button = ctk.CTkButton(self, text="登録", command=self.save)
         ctk.set_appearance_mode("light")
         ctk.set_default_color_theme("blue")
         self.title('目標管理')
         self.geometry("400x500")
         self.time = datetime.now()
         self.flag = False
         self.button.pack(pady=10)
         self.total = 0
         self.label = ctk.CTkLabel(self, text="")
         self.label.pack(pady=40)
         self.entry1 = ctk.CTkEntry(self)
         self.entry1.pack(pady=10)
         self.entry2 = ctk.CTkEntry(self)
         self.entry2.pack(pady=10)
         self.entry3 = ctk.CTkEntry(self)
         self.entry3.pack(pady=10)
         self.entry4 = ctk.CTkEntry(self)
         self.entry4.pack(pady=10)
         
    def save(self):
        self.goals = [self.csv_date,self.date]
        goal1 = self.entry1.get()
        self.goals.append(goal1)
        goal2 = self.entry2.get()
        self.goals.append(goal2)
        goal3 = self.entry3.get()
        self.goals.append(goal3)
        goal4 = self.entry4.get()
        self.goals.append(goal4)
        if self.csv_path is None:
            print("環境変数が機能していません")
        else:
            full_path = os.path.join(self.csv_path, self.csv_file)
            
        file_exies = not os.path.isfile(full_path) or os.path.getsize(full_path) == 0
        
        with open(full_path, 'a', newline='') as f:
            writer = csv.writer(f)
            
            if  file_exies:
                    writer.writerow(self.csv_header)
            
            writer.writerow(self.goals)

    def run(self):
        self.mainloop()
if __name__ == "__main__":
    goal = Goals()
    goal.run()