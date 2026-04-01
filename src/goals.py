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
         self.update_button = ctk.CTkButton(self, text="更新", command=self.update)

         self.option1.set('未着手')
         self.option1.pack()

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
         
         
    def save(self):
        import uuid
        
        entry = [self.entry1, self.entry2]

        for i in entry:
            if i.get() == "":
                continue
            recode_id = str(uuid.uuid4())
            self.goals = {'key': recode_id,'created_at': self.json_date,"date": self.date, 
                        'task': i.get(), "states": -1, "updated_at": None}

            if self.json_path is None:
                print("環境変数が機能していません")
            else:
                full_path = os.path.join(self.json_path, self.json_file)
                
            with open(full_path, 'a', encoding='utf-8') as f:
                data = json.dumps(self.goals, ensure_ascii=False)
                f.write(data + "\n")

    def update(self):
        serch_task = None
        serch_date = None
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
                if file_data['states'] == -1 or file_data['states'] == 0:
                    print(file_data)
                    update_data.append(file_data)
                    print(update_data)

        target = []
        for i in update_data:
            if i['created_at'] != self.json_date:
                continue
            target.append(i)
        print(target)
        if not target: return
        serch_task = target[0]
        serch_date = self.json_date

        val_a = self.pulldown[self.option1.get()]

        for i in update_data:
            if i['key'] == serch_task['key']:
                i['states'] = val_a
                if val_a == 1:
                    i['updated_at'] = serch_date

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
                if row['key'] == serch_task['key']:
                    row = serch_task
                new_data = json.dumps(row, ensure_ascii=False)
                f.write(new_data + '\n')


    def run(self):
        self.mainloop()
if __name__ == "__main__":
    goal = Goals()
    goal.run()