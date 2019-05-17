import pprint as _pp
import tecerator as _tc
import yaml as _yaml
import subprocess as _subprocess

NAME_CLI = 'sio2-staszic'
NAME_PATH = 'sio2-staszic'


def _alpha_lower_id(i):
    s = ''
    while i > 0 or len(s) == 0:
        c = chr(ord('a') + i % 26)
        s = c + s
        i //= 26
    return s


def _format_config_yml(ctx, task):
    obj = {
        'title': task.title,
        'memory_limits': {},
        'time_limits': {},
        'points': {},
    }
    for _, gh, group in groups(task):
        for _, th, test in tests(task):
            id = f'{gh}{th}'
            obj['memory_limits'][id] = task.memory_limit.as_kilobytes()
            obj['time_limits'][id] = task.time_limit.as_milliseconds()
        if not group.is_example:
            obj['points'][gh] = group.points
    return _yaml.dump(obj, default_flow_style=False)


def build(task):
    ctx = _tc.build.Context(task, _tc.target.sio2_staszic)
    ctx.make_all()
    ctx.write(_format_config_yml(ctx, task), [task.symbol, 'config.yml'])
    for i, gh, group in groups(task):
        for j, th, test in tests(group):
            ctx.copy(ctx.test_in(i, j), [task.symbol, 'in', f'{task.symbol}{gh}{th}.in'])
            ctx.copy(ctx.test_out(i, j), [task.symbol, 'out', f'{task.symbol}{gh}{th}.out'])

    for solution in task.solutions:
        ctx.copy(solution.path,
                 [task.symbol, 'prog', f'{task.symbol}{solution.kind}{solution.inkind_num}{solution.path.suffix}'])
    ctx.copy(ctx.rendered_description(), [task.symbol, 'doc', f'{task.symbol}zad.pdf'])
    if _subprocess.call(['zip', '-r', f'{task.symbol}.zip', f'{task.symbol}'], cwd=ctx.path_for_target()) != 0:
        raise Exception('zipping errored')

def groups(task):
    group_ord = 0
    for i, group in enumerate(task.tests):
        if group.is_example:
            group_num = 0
        else:
            group_ord += 1
            group_num = group_ord
        yield i, group_num, group


def tests(group):
    for i, test in enumerate(group.tests):
        yield i, _alpha_lower_id(i), test
