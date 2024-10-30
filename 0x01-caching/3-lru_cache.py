#!/usr/bin/env python3
"""
LRU Caching Module
"""

from base_caching import BaseCaching
from collections import OrderedDict

class LRUCache(BaseCaching):
    """
    LRU caching system
    """

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache using LRU"""
        if key and item:
            if key in self.cache_data:
                self.cache_data.move_to_end(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                first_in_key = next(iter(self.cache_data))
                print(f"DISCARD: {first_in_key}")
                del self.cache_data[first_in_key]
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item by key"""
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return None

