import threading
from abc import abstractmethod
from contextlib import contextmanager


class ILockObject(object):
    @abstractmethod
    def try_acquire(self, blocking=True) -> bool:
        pass

    @abstractmethod
    def release(self) -> None:
        pass


class Locker:
    @staticmethod
    @contextmanager
    def acquire(lock: ILockObject, blocking=True) -> bool:
        lock_acquired = lock.try_acquire(blocking=blocking)
        try:
            yield lock_acquired
        finally:
            if lock_acquired:
                lock.release()


class CriticalSection(ILockObject):
    def __init__(self):
        self._lock = threading.RLock()

    def try_acquire(self, blocking=True) -> bool:
        return self._lock.acquire(blocking=blocking)

    def release(self) -> None:
        self._lock.release()


class OneTimeLock(ILockObject):

    def __init__(self):
        self._lock = threading.RLock()
        self._acquired = False

    def try_acquire(self, blocking=True) -> bool:
        with self._lock:
            if not self._acquired:
                self._acquired = True
            return self._acquired

    def release(self) -> None:
        pass
