#!/usr/bin/env python3
"""
Base Caching Module
"""

class BaseCaching:
    """
    BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in self.cache_data)
    """

    MAX_ITEMS = 4

    def __init__(self):
        """Initialize the cache"""
        self.cache_data = {}

    def print_cache(self):
        """Print the cache"""
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print(f"{key}: {self.cache_data[key]}")

    def put(self, key, item):
        """Must be implemented in your inheriting class"""
        raise NotImplementedError("put must be implemented in your cache class")

    def get(self, key):
        """Must be implemented in your inheriting class"""
        raise NotImplementedError("get must be implemented in your cache class")

