import hashlib
import json
import os
import inspect

from datetime import tzinfo, timedelta, datetime


class TZ(tzinfo):
    def __init__(self, minutes):
        super().__init__()
        self._minutes = minutes

    def utcoffset(self, dt):
        return timedelta(minutes=self._minutes)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, _):
        return 'UTC'


def now(tz_minutes):
    return datetime.now(tz=TZ(tz_minutes))


def now_ZA():
    return now(120)


def write_javascript(klass, fh, indent=0, context=None):
    script = os.path.splitext(inspect.getfile(klass))[0]
    if context:
        script += f'.{context}'
    script += '.js'
    indent = ' ' * indent
    try:
        with open(script, 'rt', encoding="utf8") as in_fh:
            fh.write(f'{indent}<script>\n')
            name = f'{klass.__name__}: {context}' if context else klass.__name__
            fh.write(f'{indent}/* {name} */\n')
            for line in in_fh:
                if indent:
                    fh.write(indent)
                fh.write(line)
            fh.write(f'{indent}</script>\n')
    except FileNotFoundError:
        pass


def write_style(klass, fh, indent=0, context=None):
    script = os.path.splitext(inspect.getfile(klass))[0]
    if context:
        script += f'.{context}'
    script += '.css'
    indent = ' ' * indent
    try:
        with open(script, 'rt', encoding="utf8") as in_fh:
            fh.write(f'{indent}<style>\n')
            name = f'{klass.__name__}: {context}' if context else klass.__name__
            fh.write(f'{indent}/* {name} */\n')
            for line in in_fh:
                if indent:
                    fh.write(indent)
                fh.write(line)
            fh.write(f'{indent}</style>\n')
    except FileNotFoundError:
        pass


def write_html(klass, fh, indent=0, context=None):
    script = os.path.splitext(inspect.getfile(klass))[0]
    if context:
        script += f'.{context}'
    script += '.html'
    indent = ' ' * indent
    try:
        with open(script, 'rt', encoding="utf8") as in_fh:
            name = f'{klass.__name__}: {context}' if context else klass.__name__
            fh.write(f'{indent}<!-- {name} -->\n')
            for line in in_fh:
                if indent:
                    fh.write(indent)
                fh.write(line)
    except FileNotFoundError:
        pass


def blob_hash(blob):
    if not blob:
        return None
    md5 = hashlib.md5()
    md5.update(json.dumps(blob, sort_keys=True).encode())
    return md5.hexdigest()


def pad_string(msg, length, ch):
    return msg + (ch * (length - len(msg)))
