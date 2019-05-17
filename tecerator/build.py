import re
import shutil as _sh
import typing as _ty
import pathlib as _path

import tecerator as _tc
import subprocess as _subprocess


class Context:
    def __init__(self, task, target):
        self.task = task
        self.target = target
        if self.path_for_target().exists():
            _sh.rmtree(self.path_for_target())

    def write(self, text, pseudo_path):
        path = self.path_for_target().joinpath(*pseudo_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(text)

    def copy(self, source, pseudo_path):
        path = self.path_for_target().joinpath(*pseudo_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        _sh.copy2(source, path)

    def make_all(self):
        execs = self._compile_all()
        self._generate_tests(execs)
        self._update_description()
        self._render_description()

    def _compile_all(self):
        sources = self._collect_sources()
        exec_dir = self._exec_dir()
        return {source: _tc.compile.compile(source, self.task.root_dir, exec_dir) for source in sources}

    def _generate_tests(self, execs):
        test_dir = self.tests_dir()
        main_solution = [sol for sol in self.task.solutions if sol.kind == ''][0]
        test_dir.mkdir(parents=True, exist_ok=True)
        for i, group in enumerate(self.task.tests):
            for j, test in enumerate(group.tests):
                in_path = test_dir / '{}_{}.in'.format(i, j)
                out_path = in_path.with_suffix('.out')
                if _subprocess.call([execs[test.generator]] + test.params, stdout=open(in_path, 'w')) != 0:
                    raise Exception('error when generating test in {}_{}'.format(i, j))
                if _subprocess.call([execs[main_solution.path]], stdin=open(in_path, 'r'),
                                    stdout=open(out_path, 'w')) != 0:
                    raise Exception('error when generating test out {}_{}'.format(i, j))

    def _update_description(self):
        with open(self.task.description, 'r') as f:
            latex = f.read()

        def set_field(key, val):
            nonlocal latex
            pattern = f'\\\\{key}{{.*}}'
            replacement = f'\\\\{key}{{{val}}}'
            latex = re.sub(pattern, replacement, latex)

        set_field('title', self.task.title)
        set_field('id', self.task.symbol)
        set_field('signature', self.task.author_id)
        set_field('author', self.task.author)
        set_field('konkurs', self.task.contest)
        set_field('date', self.task.date)
        set_field('RAM', self.task.memory_limit.as_megabytes())
        with open(self.task.description, 'w') as f:
            f.write(latex)

    def _render_description(self):
        ei, example_group = [(i, grp) for i, grp in enumerate(self.task.tests) if grp.is_example][0]
        ej, example_test = 0, example_group.tests[0]
        latex_dir = self._latex_dir()
        latex_dir.mkdir(parents=True, exist_ok=True)
        (latex_dir / 'in').mkdir(parents=True, exist_ok=True)
        (latex_dir / 'out').mkdir(parents=True, exist_ok=True)
        _sh.copy2(self.test_in(ei, ej), latex_dir / 'in' / f'{self.task.symbol}0.in')
        _sh.copy2(self.test_out(ei, ej), latex_dir / 'out' / f'{self.task.symbol}0.out')
        _sh.copy2(self._asset_dir() / 'sio2_staszic' / 'logo.png', latex_dir)
        _sh.copy2(self._asset_dir() / 'sio2_staszic' / 'sinol.cls', latex_dir)
        _sh.copy2(self.task.description, latex_dir / f'{self.task.symbol}zad.tex')
        if _subprocess.call(['pdflatex', f'{self.task.symbol}zad.tex'], cwd=latex_dir) != 0:
            raise Exception('latex rendering failed')

    def _collect_sources(self):
        srcs = set()
        for solution in self.task.solutions:
            srcs.add(solution.path)
        for group in self.task.tests:
            for test in group.tests:
                srcs.add(test.generator)
        return list(srcs)

    def path_for_target(self):
        return self._build_dir() / 'native' / self.target.NAME_PATH

    def _exec_dir(self):
        return self._build_dir() / 'exec'

    def tests_dir(self):
        return self._build_dir() / 'tests'

    def _build_dir(self):
        return self.task.root_dir / 'build'
    def _asset_dir(self):
        return _path.Path(__file__).parent / 'assets'
    def _latex_dir(self):
        return self._build_dir() / 'latex'

    def test_in(self, i, j):
        return self.tests_dir() / f'{i}_{j}.in'
    def test_out(self, i, j):
        return self.test_in(i, j).with_suffix('.out')

    def rendered_description(self):
        return self._latex_dir() / f'{self.task.symbol}zad.pdf'