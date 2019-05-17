import pathlib as _path
import tecerator as _tc
import pprint as _pp

class Task:
    def __init__(self, symbol, title, author, author_id, author_email, contest, date, description, solutions, tests,
                 time_limit, memory_limit, root_dir):
        self.symbol = symbol
        self.title = title
        self.author = author
        self.author_id = author_id
        self.author_email = author_email
        self.contest = contest
        self.date = date
        self.description = description
        self.solutions = clean_solutions(solutions)
        self.tests = clean_tests(tests)
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.root_dir = _path.Path(root_dir).parent

def clean_solutions(solutions):
    kinds = {}
    for solution in solutions:
        solution.path = _path.Path(solution.path)
        if not solution.kind in kinds:
            kinds[solution.kind] = []
        kinds[solution.kind].append(solution)
    for inner in kinds.values():
        for i, solution in enumerate(inner):
            if len(inner) > 1:
                solution.inkind_num = str(i+1)
            else:
                solution.inkind_num = ''
    return solutions

def clean_tests(tests):
    for i in range(len(tests)):
        if type(tests[i]) == _tc.Test:
            tests[i] = _tc.Group(points=None, tests=[tests[i]])
    for group in tests:
        expanded = []
        for test in group.tests:
            if test.params is None:
                test.params = []
            test.generator = _path.Path(test.generator)
            count = test.count
            test.count = 1
            expanded += count * [test]
        group.tests = expanded
    if any(map(lambda group: group.points is None, tests)):
        total_points = 100
        non_example = list(filter(lambda group: not group.is_example, tests))
        cnt = len(non_example)
        for i, group in enumerate(non_example):
            if not group.is_example:
                if group.points is not None:
                    raise Exception('either all test groups should have set points= or none should')
                group.points = total_points // cnt
                if cnt-1-i < total_points % cnt:
                    group.points += 1
    return tests