import unittest
import pandas as pd
import statsu


class BaseTests(unittest.TestCase):
    def test_basic(self):
        print()
        print(f'Ready to Unit Test')

    def test_import(self):
        print()
        print('Importing...')

        arr = pd.DataFrame([
            [1, 3, 5, 7, 9],
            [62, 32, 57, 16, 3],
            [21, 29, 10, 43, 57],
        ])

        statsu.show(arr)


if __name__ == '__main__':
    unittest.main()
