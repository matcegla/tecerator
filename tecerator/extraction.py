import tecerator as _tc
import sys as _sys

def extract_from(module, root_dir):
    return _tc.Task(
        symbol=module.symbol,
        title=module.title,
        author=module.author,
        author_id=module.author_id,
        author_email=module.author_email,
        contest=module.contest,
        date=module.date,
        description=module.description,
        solutions=module.solutions,
        tests=module.tests,
        time_limit=module.time_limit,
        memory_limit=module.memory_limit,
        root_dir=root_dir,
    )


def extract_main():
    return extract_from(__import__('__main__'), _sys.argv[0])
