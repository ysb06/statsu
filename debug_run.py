import statsu
import pandas as pd

data_1 = pd.DataFrame([
    [1, 3, '52', 7, -91],
    [62, 'Agent', 57, 16, 3],
    ['21a', 29, 10, 3.212, 57],
    [26.921, 102, 19, 3.212, -232],
])

data_2 = pd.DataFrame([
    [4, 5, 6, 7],
    [3, 0, 8, 2],
    [1, 2, 0, 6],
])

data_1.columns = ['You', 'Are', 'So', 'Adorable', 'Really']
data_1.index = [0, 4, 7, 10]

print(data_1)
statsu.show(data_1)
print(data_1)

statsu.show_list_with_name([
    statsu.DataObject(data_1, 'Data 1'),
    statsu.DataObject(data_2, 'Data 2'),
])
