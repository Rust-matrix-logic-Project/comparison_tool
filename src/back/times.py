import csv
from datetime import datetime
import os
class TimeCheker():
    def __init__(self):
            self.flag = False

    def start_checker(self):
        
        if self.flag is True:
            return "終了ボタンが押されていません"
        else:
            start_time = datetime.now()
            self.start = start_time
            self.flag = True
            return start_time

    def end_checker(self):
            if self.flag is False:
                 return "開始ボタンが押されていません"
            else:
                self.endtime = datetime.now()
                self.total = self.endtime - self.start            
                result = self.save_to_csv()
                self.flag = False
                return result
    
    def save_to_csv(self):
        year_month = datetime.now().strftime("%Y-%m")
        path = f"csv/time_{year_month}.csv"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath( __file__)))
        
        full_path = os.path.join(base_dir, path)
        file = os.path.isfile(full_path)
        csv_dir = os.path.isdir(os.path.join(base_dir, "csv"))

        if not csv_dir:
             os.mkdir(os.path.join(base_dir,"csv"))
             
        try:
            with open(full_path, 'a', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file:
                    writer.writerow(["開始日時", "終了日時", "total"])
                start = self.start.strftime("%Y-%m-%d")
                end = self.endtime.strftime("%Y-%m-%d")
                duration = str(self.total).split(".")[0]
                data = [start, end, duration]
                writer.writerow(data)
            
            return str(self.total).split(".")[0]
        except:
             return "csv保存に問題発生"