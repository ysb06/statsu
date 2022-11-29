import statsu
import pandas as pd

data = pd.DataFrame([
    [1, 3, '52', 7, -91],
    [62, 'Agent', 57, 16, 3],
    ['21a', 29, 10, 3.212, 57],
    [26.921, 102, 19, 3.212, -232],
])

statsu.show(data)
