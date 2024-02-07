from src.core.requests.RequestThread import RequestThread

lst = []  # An Expedient Solution


def callback_handler(aux, *args, **kwargs):
    th = RequestThread(*args, **kwargs)
    lst.append(th)
    th.sig_request_response.connect(aux)
    th.start()
