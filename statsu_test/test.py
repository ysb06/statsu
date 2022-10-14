import unittest
import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, 'statsu'
)
sys.path.append(SOURCE_PATH)


class BaseTests(unittest.TestCase):
    def test_basic(self):
        print()
        print(f'Base Test Ok: {sys.path}')

    def test_import(self):
        print()
        print('Importing...')
        import pandas as pd
        from statsu import statsu

        arr = pd.DataFrame([
            [1, 3, 5, 7, 9],
            [62, 32, 57, 16, 3],
            [21, 29, 10, 43, 57],
        ])

        statsu.show(arr)


if __name__ == '__main__':
    unittest.main()
