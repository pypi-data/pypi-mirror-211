from socket import AF_INET, SOCK_STREAM, socket, timeout as TimeoutError, SHUT_RDWR
from threading import Thread
from time import sleep, monotonic
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock
from urllib.request import urlopen
from logging import INFO

from pytest import fixture

OOB_CLEANUP_INTERVAL_SECONDS = 0.05
OOB_ITEM_EXPIRY_SECONDS = 0.5
REQUEST_ID = "im-quite-unique!"

from pothead.gating import wait_for_idle_cpus  # noqa: E402 override environ first

from .util import ObjectProxy  # noqa: E402
from .worker import LoadBalancer, Server  # noqa: E402


class Flag:
    def __init__(self) -> None:
        self.v = False

    def set(self):
        self.v = True

    def is_set(self) -> bool:
        return self.v


def make_demo_app(is_terminated: Flag):
    def demo_app(environ, start_response):
        path = environ.get("PATH_INFO")
        try:
            if path == "/":
                start_response("200 OK", ())
                yield b"Hello World!"
            elif path == "/crash":
                raise Exception("Nope nope nope")
            elif path == "/slow_loris":
                sleep(0.05)
                start_response("200 OK", ())
                for byte in b"This might take a while...":
                    sleep(0.1)
                    yield byte
            elif path == "/hang_forever":
                start_response("200 OK", ())
                while True:
                    yield b""
                    sleep(0.01)
            else:
                start_response("404 Not Found", ())
        finally:
            is_terminated.set()

    return demo_app


class WorkerConnection:
    def __init__(self, sock: socket):
        self.sock = sock

    def send_request(self, path="/"):
        self.sock.sendall(
            f"GET {path} HTTP/1.1\r\nx-request-id: {REQUEST_ID}\r\n\r\n".encode("ascii")
        )

    def read_response(self):
        buf = b""
        read = True
        while read:
            read = self.sock.recv(1024)
            buf += read
        return buf

    def disconnect(self):
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()


class DummyBroker:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("localhost", 0))
        self.sock.listen(1)

    def addr(self):
        return self.sock.getsockname()

    def accept(self, timeout) -> Optional[WorkerConnection]:
        self.sock.settimeout(timeout)
        try:
            sock, _ = self.sock.accept()
            return WorkerConnection(sock)
        except TimeoutError:
            return None


def mock_balancer(addresses):
    class MockBalancer(LoadBalancer):
        def refresh(self):
            self._balancer.provision(addresses)

    return MockBalancer


class WorkerTest(TestCase):
    def test_load_balancing(self):
        broker_a, broker_b = (DummyBroker() for _ in range(2))
        app = ObjectProxy(make_demo_app(Flag()))
        app.wait_for_slot = wait_for_idle_cpus(0, max_concurrent=10)

        worker = Server(
            ("", 0),
            app,
            load_balancer=mock_balancer(map(DummyBroker.addr, (broker_a, broker_b))),
        )
        Thread(target=worker.poll_loop, daemon=True).start()

        connection_a = broker_a.accept(0.1)
        connection_b = broker_b.accept(0.1)

        assert broker_a.accept(0.2) is None
        assert broker_b.accept(0.2) is None

        connection_b.send_request()
        assert broker_b.accept(0.2) is not None

        connection_a.send_request()
        assert broker_a.accept(0.2) is not None

    def test_cancel_hung_request(self):
        broker = DummyBroker()
        request_finished = Flag()

        app = ObjectProxy(make_demo_app(request_finished))
        app.wait_for_slot = wait_for_idle_cpus(0, max_concurrent=10)

        server = Server(
            ("", 0),
            app,
            load_balancer=mock_balancer([broker.addr()]),
        )
        Thread(target=server.poll_loop, daemon=True).start()
        connection = broker.accept(0.1)

        connection.send_request("/hang_forever")
        sleep(0.1)
        connection.disconnect()

        sleep(0.1)

        assert request_finished.is_set()


class WaitForFirstSlot:
    def __init__(self, callbacks):
        self.counter = 0
        self.callbacks = callbacks

    def __call__(self, halt):
        self.counter += 1
        if self.counter <= 1:
            return self.callbacks
        else:
            from time import sleep

            while not halt():
                sleep(0.05)


class RedirectWorkerTest(TestCase):
    @fixture(autouse=True)
    def use_caplog(self, caplog):
        caplog.set_level(INFO)
        self.caplog = caplog

    def setUp(self):
        broker = DummyBroker()
        self.callbacks = MagicMock()

        app = ObjectProxy(make_demo_app(Flag()))
        app.wait_for_slot = WaitForFirstSlot(self.callbacks)

        self.server = Server(
            ("", 0),
            app,
            load_balancer=mock_balancer([broker.addr()]),
            redirect_port=0,
            oob_cleanup_interval_seconds=OOB_CLEANUP_INTERVAL_SECONDS,
            oob_item_expiry_seconds=OOB_ITEM_EXPIRY_SECONDS,
        )
        Thread(target=self.server.poll_loop, daemon=True).start()
        self.connection = broker.accept(0.1)

    def tearDown(self):
        self.server.shutdown()

    def test_response_redirect(self):
        self.connection.send_request()
        resp = self.connection.read_response().split(b"\r\n")

        assert resp[0] == b"HTTP/1.1 303 See Other"
        location = (
            [x for x in resp if x.startswith(b"Location: ")][0].split()[1].decode()
        )
        real_response = urlopen(location)
        assert real_response.status == 200
        assert real_response.read().startswith(b"Hello World!")

    def test_reject_no_redirect(self):
        self.connection.send_request("/nonexisting")
        resp = self.connection.read_response().split(b"\r\n")

        assert resp[0] == b"HTTP/1.1 404 Not Found"
        assert b"Location" not in [x.split(b":") for x in resp]

    def test_fail_no_redirect(self):
        self.connection.send_request("/crash")
        resp = self.connection.read_response().split(b"\r\n")

        assert resp[0] == b"HTTP/1.1 500 INTERNAL SERVER ERROR"
        assert b"Location" not in [x.split(b":") for x in resp]

    def test_ondone_deferred(self):
        self.connection.send_request()
        resp = self.connection.read_response().split(b"\r\n")

        self.callbacks.done.assert_not_called()

        location = (
            [x for x in resp if x.startswith(b"Location: ")][0].split()[1].decode()
        )
        real_response = urlopen(location)
        assert real_response.status == 200
        assert real_response.read().startswith(b"Hello World!")

        self.callbacks.done.assert_called()

    def test_ondone_called_for_crash(self):
        self.connection.send_request("/crash")
        self.connection.read_response()

        self.callbacks.done.assert_called()

    def test_ondone_called_for_reject(self):
        self.connection.send_request("/nonexisting")
        self.connection.read_response()

        self.callbacks.done.assert_called()

    def test_ondone_called_after_timeout(self):
        self.connection.send_request()
        self.connection.read_response()

        self.callbacks.done.assert_not_called()

        sleep(OOB_ITEM_EXPIRY_SECONDS + 2 * OOB_CLEANUP_INTERVAL_SECONDS)

        self.callbacks.done.assert_called()

    def test_log_elapsed_after_success(self):
        self.connection.send_request()
        self.connection.read_response()

        sleep(0.05)

        assert f"[{REQUEST_ID}] Elapsed: " in self.caplog.text

    def test_log_elapsed_after_crash(self):
        self.connection.send_request("/crash")
        self.connection.read_response()

        sleep(0.05)

        assert f"[{REQUEST_ID}] Elapsed: " in self.caplog.text

    def test_log_elapsed_after_disconnect(self):
        self.connection.send_request("/slow_loris")
        self.connection.disconnect()

        sleep(0.2)

        assert f"[{REQUEST_ID}] Elapsed: " in self.caplog.text


class TestShutdown(TestCase):
    DELAY_START_RESPONSE = 0.3
    DELAY_FINISH_RESPONSE = 0.8

    def setUp(self):
        broker = DummyBroker()
        self.callbacks = MagicMock()

        def app(environ, start_response):
            sleep(self.DELAY_START_RESPONSE)
            start_response("200 OK", {})
            yield b" "
            sleep(self.DELAY_FINISH_RESPONSE)
            yield b"done"

        app.wait_for_slot = WaitForFirstSlot(self.callbacks)

        self.server = Server(
            ("", 0),
            app,
            load_balancer=mock_balancer([broker.addr()]),
            redirect_port=0,
            oob_cleanup_interval_seconds=OOB_CLEANUP_INTERVAL_SECONDS,
            oob_item_expiry_seconds=OOB_ITEM_EXPIRY_SECONDS,
        )
        Thread(target=self.server.poll_loop, daemon=True).start()
        self.connection = broker.accept(0.1)

    def test_ptth_finish_before_shutdown(self):
        self.connection.send_request()
        Thread(target=self.connection.read_response).start()
        self.assertGreaterEqual(
            self.shutdown_time(), OOB_ITEM_EXPIRY_SECONDS + self.DELAY_START_RESPONSE
        )

    def test_pending_oob_expire_before_shutdown(self):
        self.connection.send_request()
        self.connection.read_response()
        st = self.shutdown_time()
        self.assertGreaterEqual(st, OOB_ITEM_EXPIRY_SECONDS)
        self.assertLessEqual(st, self.DELAY_FINISH_RESPONSE)

    def test_oob_finish_before_shutdown(self):
        self.connection.send_request()
        resp = self.connection.read_response().split(b"\r\n")

        location = (
            [x for x in resp if x.startswith(b"Location: ")][0].split()[1].decode()
        )
        real_response = urlopen(location)
        assert real_response.status == 200

        self.assertGreaterEqual(self.shutdown_time(), self.DELAY_FINISH_RESPONSE)

    def shutdown_time(self):
        start = monotonic()
        self.server.shutdown()
        return monotonic() - start
