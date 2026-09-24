import json

try:
    import orjson
    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False
    
def dumps_with_builtin(d: dict, **kwargs) -> str:
    return json.dumps(d, **kwargs)

def dumps_with_orjson(d: dict, **kwargs) -> str:
    # orjson already emits valid JSON (UTF-8); re-encoding with
    # backslashreplace produced \xNN escapes, which are not valid JSON, so any
    # non-ASCII stopword list wrote a file that load_stopwords could not read.
    return orjson.dumps(d).decode("utf-8")

if ORJSON_AVAILABLE:
    def dumps(d: dict, **kwargs) -> str:
        return dumps_with_orjson(d, **kwargs)
    loads = orjson.loads
else:
    def dumps(d: dict, **kwargs) -> str:
        return dumps_with_builtin(d, **kwargs)
    loads = json.loads
