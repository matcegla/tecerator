class Storage:
    def __init__(self, bytes):
        self.bytes = bytes

    def as_kilobytes(self):
        return self.bytes // 1024
    def as_megabytes(self):
        return self.bytes // (1024 * 1024)

    def __rmul__(self, other):
        return Storage(other * self.bytes)
class Duration:
    def __init__(self, millis):
        self.millis = millis
    def as_milliseconds(self):
        return self.millis
    def __rmul__(self, other):
        return Duration(other * self.millis)

MEGABYTE = Storage(1024 * 1024)
SECOND = Duration(1000)