import inspect
import scipy.stats


def test(a: int, b: str, c: bool=True, *args, **kwrd):
    pass

temp = inspect.getfullargspec(test)
print(temp)
print(test.__annotations__)