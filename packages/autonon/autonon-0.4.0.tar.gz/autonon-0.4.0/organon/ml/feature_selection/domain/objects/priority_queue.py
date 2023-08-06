"""Includes PriorityQueue"""


class PriorityQueue:
    """Priority queue implementation using a list"""
    def __init__(self):
        self.queue = []

    def is_empty(self):
        """Returns true if queue is empty"""
        return len(self.queue) == 0

    def push(self, item, priority):
        """
        item already in priority queue with smaller priority:
        -> update its priority
        item already in priority queue with higher priority:
        -> do nothing
        if item not in priority queue:
        -> push it
        """
        for index, (i, i_priority) in enumerate(self.queue):
            if i == item:
                if i_priority >= priority:
                    break
                del self.queue[index]
                self.queue.append((item, priority))
                break
        else:
            self.queue.append((item, priority))

    def pop(self):
        """return item with highest priority value and remove it from queue"""
        if self.is_empty():
            raise ValueError("Queue is empty")
        max_idx = 0
        for index, (_, i_priority) in enumerate(self.queue):
            if self.queue[max_idx][1] < i_priority:
                max_idx = index
        item, priority = self.queue[max_idx]
        del self.queue[max_idx]
        return item, priority
