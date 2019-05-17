class Test:
    def __init__(self, generator, params=None, count=1):
        self.generator = generator
        self.params = params
        self.count = count

    @staticmethod
    def hardcoded(input):
        return Test('cat', params=[input])

    def __rmul__(self, other):
        self.count *= other
        return self


class Group:
    def __init__(self, points, tests, is_example=False):
        self.is_example = is_example
        self.points = points
        self.tests = tests

    @staticmethod
    def example(tests, params=None):
        return Group(None, tests, is_example=True)


class Solution:
    def __init__(self, path, kind):
        self.path = path
        self.kind = kind
        self.inkind_num = None

    @staticmethod
    def good(path):
        return Solution(path, '')

    @staticmethod
    def slow(path):
        return Solution(path, 's')

    @staticmethod
    def bad(path):
        return Solution(path, 'b')

    @staticmethod
    def test_generator(path):
        return Solution(path, 'ingen')

    @staticmethod
    def checker(path):
        return Solution(path, 'chk')