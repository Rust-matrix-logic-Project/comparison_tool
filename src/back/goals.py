from datetime import datetime
import os, json
from dotenv import load_dotenv
load_dotenv()

class Goals():
    def __init__(self, goal, status):
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_file = f"{self.year}_{self.month}_goals.jsonl"
         self.date = datetime.now().strftime("%d")
         self.json_path = os.environ.get("STUDY_JSON_DIR")
         self.goal = goal
         self.goals = {}
         self.status = status
         
         
    def save(self):
        import uuid
        entry = []
        self.json_date = datetime.now().strftime("%Y-%m-%d")
        goal = ",".join(self.goal).split(",")
        print(goal)

        if len(goal) > 0:
            self.entry1 = (self.date, goal[0])
            entry.append(self.entry1)
        else:
            self.entry1 = None
        if len(goal) > 1:
            self.entry2 = (self.date, goal[1])
            entry.append(self.entry2)
        else:
            self.entry2 = None

        if len(goal) > 2:
            self.entry3 = (self.date, goal[2])
            entry.append(self.entry3)
        else:
            self.entry3 = None
        if len(goal) > 3:
            self.entry4 = (self.date, goal[3])
            entry.append(self.entry4)
        else:
            self.entry4 = None
        
        for i in entry:
            recode_id = str(uuid.uuid4())
            print(i)
            if i == "":
                continue
        
            self.goals = {'key': recode_id,'created_at': self.json_date,"date": self.date, 
                    'task': i[1], "status": -1, "updated_at": None}
            
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
        self.updated_at = datetime.now()

        if self.json_path is None:
            print("環境変数が機能していません")
            return
        else:
            full_path = os.path.join(self.json_path, self.json_file)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                except:
                    continue
                if file_data['status'] == -1 or file_data['status'] == 0:
                    update_data.append(file_data)

        target = []
        for i in update_data:
            if i['created_at'] != self.json_date:
                continue
            target.append(i)
        print(target)
        if not target: return
        serch_task = target[0]
        serch_date = self.json_date

        val_a = self.status

        for i in update_data:
            if i['key'] == serch_task['key']:
                i['status'] = val_a
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

