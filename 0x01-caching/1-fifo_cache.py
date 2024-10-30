#!/usr/bin/env python3
"""
FIFO Caching Module
"""

from base_caching import BaseCaching

class FIFOCache(BaseCaching):
    """
    FIFO caching system
    """

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.cache_queue = []

    def put(self, key, item):
        """Add an item in the cache using FIFO"""
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                first_in_key = self.cache_queue.pop(0)
                del self.cache_data[first_in_key]
                print(f"DISCARD: {first_in_key}")
            self.cache_data[key] = item
            self.cache_queue.append(key)

    def get(self, key):
        """Retrieve an item by key"""
        return self.cache_data.get(key, None)

