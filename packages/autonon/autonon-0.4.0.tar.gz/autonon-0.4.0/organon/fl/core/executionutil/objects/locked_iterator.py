"""Includes LockedIterator class"""
import threading


class LockedIterator:
    """Iterator which is locked on iteration (making it thread-safe)"""
    def __init__(self, iterator):
        self.lock = threading.Lock()
        self.iterator = iterator.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.iterator)
