from datetime import datetime
import os, json
from dotenv import load_dotenv
load_dotenv()

class Goals():
    def __init__(self, goal=None, key=None, status=None, limit=None, month=None):
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_file = f"{self.year}_{month}_goals.jsonl"
         self.json_path = os.environ.get("STUDY_JSON_DIR")
         self.goal = goal
         self.key = key
         self.goals = {}
         self.status = status
         self.json_date = None
         self.limit = limit

    def save(self):
        import uuid
        entry = []
        self.json_date = datetime.now().strftime("%Y-%m-%d")
        goal = ",".join(self.goal).split(",")
        
        if len(goal) > 0:
            self.entry1 = (self.json_date, goal[0])
            entry.append(self.entry1)
        else:
            self.entry1 = None
        if len(goal) > 1:
            self.entry2 = (self.json_date, goal[1])
            entry.append(self.entry2)
        else:
            self.entry2 = None

        if len(goal) > 2:
            self.entry3 = (self.json_date, goal[2])
            entry.append(self.entry3)
        else:
            self.entry3 = None
        if len(goal) > 3:
            self.entry4 = (self.json_date, goal[3])
            entry.append(self.entry4)
        else:
            self.entry4 = None
        
        for i in entry:
            recode_id = str(uuid.uuid4())
            if i == "":
                continue
        
            self.goals = {'key': recode_id,'created_at': i[0],"limit": self.limit, 
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
        self.json_date = datetime.now().strftime("%Y-%m-%d")

        if self.status.lstrip('-').isdigit():
            self.status = int(self.status)
        # check
        if isinstance(self.status, str):
            print(isinstance(self.status, str))
            print(f"ステータス更新時に文字列({self.status})が送られました")
            return "ステータス更新時に文字列が送られました"
        
        if self.status > 1 or self.status < -1:
            print("ステータス更新時に不正な値が送られました")
            return "ステータス更新時に不正な値が送られました"
        
        # update
        if self.json_path is None:
            print("環境変数が機能していません")
            return "環境変数が機能していません"
        else:
            full_path = os.path.join(self.json_path, self.json_file)

        with open(full_path, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                except:
                    return "jsonファイルが見つかりません"
                
                if not isinstance(file_data['status'], int) or file_data['status'] > 1 or file_data['status'] < -1:
                        print( "不正な値を検知")
                        continue
                
                if file_data['status'] == 1:
                    print("既に完了済みのタスクです")
                    continue

                if file_data['status'] == -1 or file_data['status'] == 0:
                    update_data.append(file_data)

        target = []
        for i in update_data:
            if not i['key'] == self.key:
                continue
            target.append(i)

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
                    row['limit'] = self.limit
                    row['updated_at'] = self.json_date
                new_data = json.dumps(row, ensure_ascii=False)
                f.write(new_data + '\n')
        
    def leard_to_jsonl(self):
        return_data = []
        if self.json_path is None:
            print("環境変数が機能していません")
            return
        else:
            full_path = os.path.join(self.json_path, self.json_file)
        with open(full_path, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                    return_data.append(file_data)
                except:
                    return "jsonファイルが見つかりません"
        print(return_data)
        return return_data