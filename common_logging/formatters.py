import json
from logging import Formatter, LogRecord
from datetime import date, datetime
from traceback import TracebackException
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Exception):
            tb = TracebackException.from_exception(obj)
            data = dict(
                type=type(obj).__name__,
                message=str(obj),
                traceback="".join(tb.format())
            )
            return data
        return json.JSONEncoder.default(self, obj)


class JSONFormatter(Formatter):
    def format(
        self,
        record: LogRecord
    ) -> str:
        ts = datetime.utcfromtimestamp(record.created)
        data = {
            "level": record.levelname,
            "@timestamp": ts.isoformat(),
            "component": record.module,
            "function": record.funcName,
            "caller": "%s:%s" % (record.filename, record.lineno),
            "message": record.getMessage()
        }
        return json.dumps(data, cls=JSONEncoder)
