import json

try:
    import orjson
    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False


def dumps_with_builtin(d: dict, **kwargs) -> str:
    return json.dumps(d, **kwargs)


def dumps_with_orjson(d: dict, **kwargs) -> str:
    # orjson already emits valid JSON (UTF-8). Re-encoding with backslashreplace
    # to fake ensure_ascii=True produced \xNN escapes, which are not valid JSON,
    # so any stopword list containing a Latin-1 character (German ß/ä/ö/ü, French
    # é, Spanish ñ, …) wrote a file that the loader could not read back.
    return orjson.dumps(d).decode("utf-8")


if ORJSON_AVAILABLE:
    def dumps(d: dict, **kwargs) -> str:
        return dumps_with_orjson(d, **kwargs)
    loads = orjson.loads
else:
    def dumps(d: dict, **kwargs) -> str:
        return dumps_with_builtin(d, **kwargs)
    loads = json.loads
