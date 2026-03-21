import pandas as ps

def read_csv():
    print("test")
    list1 = ps.read_csv("comparison_tool/csv/test1.csv",header=None)
    list2 = ps.read_csv("comparison_tool/csv/test2.csv", header=None)
    print(list1)
    print(list2)
    test_eq = list1.equals(list2)
    print(test_eq)
if __name__ == "__main__":
    read_csv()