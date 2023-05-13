import _thread
import logging
import multiprocessing
import queue
import socket
import sys
import tempfile
import time
import warnings
from threading import Thread

from . import globals, helpers, native

try:
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
except ModuleNotFoundError:
    pass


def open_window(host: str, port: int, title: str, width: int, height: int, fullscreen: bool,
                message_queue: multiprocessing.Queue) -> None:
    while not helpers.is_port_open(host, port):
        time.sleep(0.1)

    window_kwargs = dict(url=f'http://{host}:{port}', title=title, width=width, height=height, fullscreen=fullscreen)
    window_kwargs.update(globals.app.native.window_args)

    try:
        window = webview.create_window(**window_kwargs)
        print('--------------------starting thread', flush=True)

        def process_bridge():
            time.sleep(1)
            while True:
                try:
                    result = message_queue.get(block=False)
                    print(f'received {result}', flush=True)
                except queue.Empty:
                    print('empty', flush=True)
                    time.sleep(1)
        t = Thread(target=process_bridge)
        t.start()

        webview.start(storage_path=tempfile.mkdtemp(), **globals.app.native.start_args)
    except NameError:
        print('Native mode is not supported in this configuration. Please install pywebview to use it.')
        sys.exit(1)


def activate(host: str, port: int, title: str, width: int, height: int, fullscreen: bool) -> None:
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        globals.server.should_exit = True
        while globals.state != globals.State.STOPPED:
            time.sleep(0.1)
        _thread.interrupt_main()

    multiprocessing.freeze_support()
    process = multiprocessing.Process(
        target=open_window,
        args=(host, port, title, width, height, fullscreen, native.queue),
        daemon=False
    )
    process.start()

    Thread(target=check_shutdown, daemon=True).start()


def find_open_port(start_port: int = 8000, end_port: int = 8999) -> int:
    """Reliably find an open port in a given range.

    This function will actually try to open the port to ensure no firewall blocks it.
    This is better than, e.g., passing port=0 to uvicorn.
    """
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            pass
    raise OSError('No open port found')
