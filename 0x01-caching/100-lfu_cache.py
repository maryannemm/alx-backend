#!/usr/bin/env python3
"""
LFU Caching Module
"""

from base_caching import BaseCaching

class LFUCache(BaseCaching):
    """
    LFU caching system
    """

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.usage_count = {}

    def put(self, key, item):
        """Add an item in the cache using LFU"""
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                least_used_key = min(self.usage_count, key=self.usage_count.get)
                print(f"DISCARD: {least_used_key}")
                del self.cache_data[least_used_key]
                del self.usage_count[least_used_key]
            self.cache_data[key] = item
            self.usage_count[key] = self.usage_count.get(key, 0) + 1

    def get(self, key):
        """Retrieve an item by key"""
        if key in self.cache_data:
            self.usage_count[key] += 1
            return self.cache_data[key]
        return None

