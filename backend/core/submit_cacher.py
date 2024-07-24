_submit_cacher = {}

def PopSubmitInfo(digest: str):
    return _submit_cacher.pop(digest)

def PushSubmitInfo(digest: str, data: ()):
    _submit_cacher[digest] = data
