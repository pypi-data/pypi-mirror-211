import time


class ColorLog:
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    STYLE_NORMAL = 0
    STYLE_BOLD = 1
    STYLE_UNDERLINE = 4
    STYLE_INVERSE = 7

    COLOR_CYANIC = 36
    COLOR_RED = 31
    COLOR_GREEN = 32
    COLOR_YELLOW = 33
    COLOR_FUCHSIA = 35
    COLOR_NORMAL = 39

    @staticmethod
    def format_message(level, msg):
        timestamp = time.strftime('%H:%M:%S')
        return '\033[0;33;39m[{0}] [{1}] {2}\033[0m'.format(timestamp, level, msg)

    def info(self, msg):
        print(self.format_message(self.INFO, msg))

    def warning(self, msg):
        print(self.format_message(self.WARNING, msg))

    def error(self, msg):
        print(self.format_message(self.ERROR, msg))

    def debug(self, msg):
        print(self.format_message(self.DEBUG, msg))

    @classmethod
    def colorful_text(cls, style, color_num, msg):
        return '\033[{0};33;{1}m{2}\033[0m'.format(style, color_num, msg)


class GetColor:
    @staticmethod
    def score(s):
        if s == '':
            return ColorLog.COLOR_NORMAL
        else:
            s = float(s)
            if s > 9.0:
                return ColorLog.COLOR_FUCHSIA
            elif s > 7.0:
                return ColorLog.COLOR_RED
            elif s > 4.0:
                return ColorLog.COLOR_YELLOW
            elif s > 0:
                return ColorLog.COLOR_GREEN
            else:
                return ColorLog.COLOR_NORMAL

    @staticmethod
    def date(d):
        if not d.count('-'):
            return ColorLog.COLOR_NORMAL
        year = int(d.split('-')[0])
        now_year = int(time.strftime('%Y'))
        if year >= now_year:
            return


if __name__ == '__main__':
    ColorLog.info('info')
    ColorLog.warning('warning')