from tecerator.target import sio2_staszic

def select(name):
    for target in TARGETS:
        if target.NAME_CLI == name:
            return target
    raise Exception('unrecognized target {}, should be in {}'.format(name, TARGET_CLI_NAMES))

TARGETS = [
    sio2_staszic,
]

TARGET_CLI_NAMES = list(map(lambda e: e.NAME_CLI, TARGETS))