#!/usr/bin/env python3
"""
Module for calculating start and end index for pagination.
"""

from typing import Tuple

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple containing the start and end index based on the page and page_size.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)

