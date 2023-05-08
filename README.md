# statsu

## About
Simple GUI Tool for Pandas DataFrame

This project is a GUI tool based on PySide6 that can display and edit Pandas DataFrames. It can be used when you want to visually check the data through a GUI instead of a console window during code execution or when you want users to edit the data directly.

## Installation

```
pip install statsu
```

## Usage

You can perform a simple test by entering the following in the console window:

```
python debug_run.py
```
After running, you can also load data from Excel files or CSV files.

You can view the DataFrame you want to view or edit by entering it as input. After editing, you can get the edited result by saving and closing.

```Python
import pandas as pd
from statsu import show

df = pd.DataFrame({
    'a':[3.2, 'AAA', 9], 
    'b':[441, 3, 1.2], 
    'c':[0.6, 'DTD', 32]})

result = show(df)
```

## More Info.

### Issues, feedback and pull requests are welcome

Feel free to provide additional ideas, opinions, and pull requests.

### Project Goal

This project started as a personal project and currently implements only the most basic functions for manipulating DataFrames. The most important goal is to be a DataFrame Viewer, but I plan to add features such as graphs and statistical analysis based on my needs.

This project aims to be easily utilized in multiple projects through small and easily separable code.

### Comparison with Other Similar Projects

In fact, there are many more alternatives as DataFrame Visualization Tools than this.

[Pandas DataFrame Visualization Tools](https://pbpython.com/dataframe-gui-overview.html)

The advantage of this project at the moment is that the code is small, making it easy to understand quickly and customize. If you want more features, refer to the projects in the link above, and use this project as a base to create your own tools.

### Etc.

Code motivated by [PandasGUI](https://github.com/adamerose/PandasGUI). Past commits of this project includes PandasGUI code.