#!/usr/bin/env python3
"""
MRU Caching Module
"""

from base_caching import BaseCaching

class MRUCache(BaseCaching):
    """
    MRU caching system
    """

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.last_item = None

    def put(self, key, item):
        """Add an item in the cache using MRU"""
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                print(f"DISCARD: {self.last_item}")
                del self.cache_data[self.last_item]
            self.cache_data[key] = item
            self.last_item = key

    def get(self, key):
        """Retrieve an item by key"""
        return self.cache_data.get(key, None)

