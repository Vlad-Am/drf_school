import re


class TitleValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, field):
        reg = re.compile('^[a-z0-9\.\-\ ]+$')


