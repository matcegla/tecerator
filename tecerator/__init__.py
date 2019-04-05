import os
import pathlib
import re
import shutil

class TestGroup:
    def __init__(self, id, points, templates, time_limit=None, memory_limit=None, params=None):
        self.id = id
        self.points = points
        self.templates = templates
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.params = [] if params is None else params
    @staticmethod
    def example(templates, time_limit=None, memory_limit=None, params=None):
        return TestGroup('0', None, templates, time_limit=time_limit, memory_limit=memory_limit, params=params)

class Test:
    def __init__(self, generator, time_limit=None, memory_limit=None, params=None, name=None, count=1):
        self.generator = generator
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.params = params
        self.name = name
        self.count = count
    @staticmethod
    def hardcoded(input, time_limit=None, memory_limit=None, name=None):
        return Test('cat', time_limit=time_limit, memory_limit=memory_limit, params=[input], name=name)

class Program:
    def __init__(self, path, kind):
        self.path = path
        self.kind = kind
    @staticmethod
    def good(path):
        return Program(path, '')
    @staticmethod
    def slow(path):
        return Program(path, 's')
    @staticmethod
    def bad(path):
        return Program(path, 'b')
    @staticmethod
    def test_generator(path):
        return Program(path, 'ingen')
    @staticmethod
    def checker(path):
        return Program(path, 'chk')

def seconds(n):
    return n * 1000
def megabytes(n):
    return n

def run():
    manifest = __import__('__main__')

    symbol = manifest.symbol
    title = manifest.title
    author = manifest.author
    author_signature = manifest.author_signature
    contest = manifest.contest
    date = manifest.date
    description = manifest.description
    programs = manifest.programs
    wzo = manifest.wzo
    tests = manifest.tests
    glob_time_limit = manifest.time_limit
    glob_memory_limit = manifest.memory_limit

    build_dir = pathlib.Path('build')
    build_dir.mkdir(parents=False, exist_ok=True)
    package_dir = build_dir.joinpath('package').joinpath(symbol)
    package_dir.mkdir(parents=True, exist_ok=True)

    copy_programs(package_dir, programs, symbol)
    write_config(package_dir, title, tests, glob_time_limit, glob_memory_limit)
    generate_tests(package_dir, symbol, programs, tests, wzo)
    update_latex(description, title, symbol, author_signature, author, contest, date, glob_memory_limit)
    compile_latex(description, build_dir, symbol, tests)
    compress_package(build_dir, symbol)

def copy_programs(package_dir, programs, symbol):
    def copy(src, id):
        src = pathlib.Path(src)
        shutil.copy2(src, path.joinpath(f'{symbol}{id}{src.suffix}'))
    path = package_dir.joinpath('prog')
    path.mkdir(parents=False, exist_ok=True)
    categories = {}
    for prog in programs:
        categories.setdefault(prog.kind, []).append(prog)
    for cat in categories.values():
        if len(cat) == 1:
            copy(cat[0].path, cat[0].kind)
        else:
            for i, prog in enumerate(cat):
                copy(prog.path, f'{prog.kind}{i+1}')

def write_config(package_dir, title, tests, glob_time_limit, glob_memory_limit):
    path = package_dir.joinpath('config.yml')
    with open(path, 'w+') as f:
        f.write(f'title: {title}\n')
        f.write(f'memory_limits:\n')
        for tg, t, name in iter_tests(tests):
            memory_limit = t.memory_limit or tg.memory_limit or glob_memory_limit
            f.write(f'    {tg.id}{name}: {memory_limit*1024}\n')
        f.write(f'time_limits:\n')
        for tg, t, name in iter_tests(tests):
            time_limit = t.time_limit or tg.time_limit or glob_time_limit
            f.write(f'    {tg.id}{name}: {time_limit}\n')
        f.write(f'points:\n')
        for group in tests:
            if group.points is not None:
                f.write(f'    {group.id}: {group.points}\n')

def data_name(symbol, id, name, ext):
    return f'{symbol}{id}{name}.{ext}'
def generate_tests(package_dir, symbol, programs, tests, wzo):
    ins_path = package_dir.joinpath('in')
    ins_path.mkdir(parents=False, exist_ok=True)
    outs_path = package_dir.joinpath('out')
    outs_path.mkdir(parents=False, exist_ok=True)
    for tg, t, name in iter_tests(tests):
        print(tg.params, t.params)
        params = ' '.join(map(str, (tg.params or []) + (t.params or [])))
        in_path = ins_path.joinpath(data_name(symbol, tg.id, name, 'in'))
        out_path = outs_path.joinpath(data_name(symbol, tg.id, name, 'out'))
        os.system(f'{t.generator} {params} > {in_path}')
        os.system(f'{wzo} < {in_path} > {out_path}')

def update_latex(description, title, symbol, signature, author, contest, date, glob_memory_limit):
    with open(description, 'r') as f:
        latex = f.read()
    def set_field(key, val):
        nonlocal latex
        pattern = f'\\\\{key}{{.*}}'
        replacement = f'\\\\{key}{{{val}}}'
        latex = re.sub(pattern, replacement, latex)
    set_field('title', title)
    set_field('id', symbol)
    set_field('signature', signature)
    set_field('author', author)
    set_field('konkurs', contest)
    set_field('date', date)
    set_field('RAM', glob_memory_limit)
    with open(description, 'w') as f:
        f.write(latex)

def compile_latex(description, build_dir, symbol, tests):
    latex_dir = build_dir.joinpath('latex')
    latex_dir.mkdir(parents=False, exist_ok=True)
    ins_path = latex_dir.joinpath('in')
    ins_path.mkdir(parents=False, exist_ok=True)
    outs_path = latex_dir.joinpath('out')
    outs_path.mkdir(parents=False, exist_ok=True)
    etg, et, en = list(filter(lambda gtn: gtn[0].id == '0', iter_tests(tests)))[0]
    shutil.copy2(build_dir.joinpath('package').joinpath(symbol).joinpath('in').joinpath(data_name(symbol, etg.id, et.name, 'in')), ins_path.joinpath(f'{symbol}0.in'))
    shutil.copy2(build_dir.joinpath('package').joinpath(symbol).joinpath('out').joinpath(data_name(symbol, etg.id, et.name, 'out')), outs_path.joinpath(f'{symbol}0.out'))
    shutil.copy2(pathlib.Path(__file__).parents[0].joinpath('assets').joinpath('logo.png'), latex_dir)
    shutil.copy2(pathlib.Path(__file__).parents[0].joinpath('assets').joinpath('sinol.cls'), latex_dir)
    shutil.copy2(description, latex_dir.joinpath(f'{symbol}zad.tex'))
    os.system(f'cd {latex_dir} && pdflatex {symbol}zad.tex')
    doc_dir = build_dir.joinpath('package').joinpath(symbol).joinpath('doc')
    doc_dir.mkdir(parents=False, exist_ok=True)
    shutil.copy2(latex_dir.joinpath(f'{symbol}zad.pdf'), doc_dir)

def compress_package(build_dir, symbol):
    pkg_dir = build_dir.joinpath('package')
    os.system(f'cd {pkg_dir} && zip -r ../{symbol}.zip {symbol}')

def iter_tests(tests):
    for group in tests:
        yield from iter_test_group(group)
def iter_test_group(group):
    assert all((test.name is None for test in group.templates)) or all((test.name is not None for test in group.templates)), 'mixing custom test names and auto test names is forbidden'
    prev_id = ''
    for test in group.templates:
        for _ in range(test.count):
            prev_id = next_alphaid(prev_id)
            name = test.name if test.name is not None else prev_id
            yield group, test, name

def next_alphaid(s):
    for i in range(1, len(s)+1):
        if s[-i] != 'z':
            return s[:-i] + chr(ord(s[-i])+1) + 'a'*(i-1)
    return 'a'*(len(s)+1)
