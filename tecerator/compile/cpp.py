import subprocess as _subprocess
import shutil as _sh
import pathlib as _path

SOURCE_SUFFIXES = ['.cpp', '.cxx', '.cc']

def compile(source, root_dir, exec_dir):
    source = root_dir / source
    exec = (exec_dir / source.relative_to(root_dir)).with_suffix('.e')
    exec.parent.mkdir(parents=True, exist_ok=True)
    if not exec.exists() or exec.stat().st_mtime < source.stat().st_mtime:
        if _subprocess.call(['g++', '-std=c++17', '-Ofast', source, '-o', exec]) != 0:
            raise Exception('failed to compile {}'.format(source))
    return exec