class FormatError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidTypeError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FutureTimeError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ItemNotFoundError(Exception):

    def __init__(self, mark):
        """
        :param mark: 标志
        """
        self.mark = mark

    def __str__(self):
        return f"item {self.mark} not found"
