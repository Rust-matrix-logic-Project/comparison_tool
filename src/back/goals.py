from datetime import datetime
import os, json
from dotenv import load_dotenv
load_dotenv()

class Goals():
    def __init__(self, date, goal, updated_at, states):
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_date = datetime.now().strftime("%Y-%m-%d")
         self.json_file = f"{self.year}_{self.month}_goals.jsonl"
         self.date = datetime.now().strftime("%d")
         self.json_path = os.environ.get("STUDY_JSON_DIR")
         self.goals = {}

         self.entry1 = date[0], goal[0]
         self.entry2 = date[1], goal[1]
         self.updated_at = updated_at
         self.states = states
         
         
    def save(self):
        import uuid
        
        entry = [self.entry1, self.entry2]

        for i in entry:
            if i[0] == "":
                continue
            if i[1] == "":
                continue

            recode_id = str(uuid.uuid4())
            self.goals = {'key': recode_id,'created_at': self.json_date,"date": self.date, 
                        'task': i[1], "states": -1, "updated_at": None}

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

        val_a = self.states

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

