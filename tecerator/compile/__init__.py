from tecerator.compile import cpp, exec

def compile(source, root_dir, exec_dir):
    for lang in LANGUAGES:
        if source.suffix in lang.SOURCE_SUFFIXES:
            return lang.compile(source, root_dir, exec_dir)
    raise Exception('unknown extension \'{}\', expected one of {}'.format(source.suffix, SUPPORTED_SUFFIXES))

LANGUAGES = [cpp, exec]

SUPPORTED_SUFFIXES = []
for lang in LANGUAGES:
    SUPPORTED_SUFFIXES.extend(lang.SOURCE_SUFFIXES)