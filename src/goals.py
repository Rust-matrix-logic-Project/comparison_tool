from datetime import datetime
import os, json
from dotenv import load_dotenv
import customtkinter as ctk
load_dotenv()

class Goals(ctk.CTk):
    def __init__(self):
         super().__init__()
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_date = datetime.now().strftime("%Y-%m-%d")
         self.json_file = f"{self.year}_{self.month}_goals.jsonl"
         self.date = datetime.now().strftime("%d")
         self.json_path = os.environ.get("STUDY_JSON_DIR")
         self.goals = {}
         
         self.pulldown = {'未着手': -1, '進行中': 0, '完了': 1}
         self.button = ctk.CTkButton(self, text="登録", command=self.save)
         self.option1 = ctk.CTkOptionMenu(self,values=['未着手', '進行中', '完了'])
         self.option2 = ctk.CTkOptionMenu(self,values=['未着手', '進行中', '完了'])
         self.option3 = ctk.CTkOptionMenu(self,values=['未着手', '進行中', '完了'])
         self.option4 = ctk.CTkOptionMenu(self,values=['未着手', '進行中', '完了'])
         self.update_button = ctk.CTkButton(self, text="更新", command=self.update)

         self.option1.set('未着手')
         self.option1.pack()
         self.option2.set('未着手')
         self.option2.pack()
         self.option3.set('未着手')
         self.option3.pack()
         self.option4.set('未着手')
         self.option4.pack()

         ctk.set_appearance_mode("light")
         ctk.set_default_color_theme("blue")
         self.title('目標管理')
         self.geometry("400x500")
         self.time = datetime.now()
         self.flag = False
         self.button.pack(pady=15)
         self.update_button.pack(pady=10)
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
        self.goals = {'key': self.json_date, "date": self.date, 
                      'goal': [
                          {"goals_1": self.entry1.get(), "states": -1},
                          {"goals_2": self.entry2.get(), "states": -1},
                          {"goals_3": self.entry3.get(), "states": -1},
                          {"goals_4": self.entry4.get(), "states": -1}
                          ]}

        if self.json_path is None:
            print("環境変数が機能していません")
        else:
            full_path = os.path.join(self.json_path, self.json_file)
    
        with open(full_path, 'a', encoding='utf-8') as f:
            data = json.dumps(self.goals)
            f.write(data + "\n")

    def update(self):
        update_data = []
        if self.json_path is None:
            print("環境変数が機能していません")
        else:
            full_path = os.path.join(self.json_path, self.json_file)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                except:
                    continue
                if file_data['key'] == self.json_date:
                    print(file_data)
                    update_data.append(file_data)
                    print(update_data)

        val_a = self.pulldown[self.option1.get()]
        val_b = self.pulldown[self.option2.get()]
        val_c = self.pulldown[self.option3.get()]
        val_d = self.pulldown[self.option4.get()]

        if val_a != -1:
            update_data[0]['goal'][0]['states'] = val_a
        if val_b != -1:
            update_data[0]['goal'][1]['states'] = val_b
        if  val_c != -1:
            update_data[0]['goal'][2]['states'] = val_c
        if val_d != -1:
            update_data[0]['goal'][3]['states'] = val_d 
        
        entry_data = []
        with open(full_path, 'r', encoding='utf-8')as f:
            print(len(update_data))
            for data in f.readlines():
                try:
                    datas = json.loads(data)
                    entry_data.append(datas)
                except:
                    continue
        
        with open(full_path, 'w') as f:
            for row in entry_data:
                if row['key'] == self.json_date:
                    row = update_data[0]
                new_data = json.dumps(row)
                f.write(new_data + '\n')


    def run(self):
        self.mainloop()
if __name__ == "__main__":
    goal = Goals()
    goal.run()