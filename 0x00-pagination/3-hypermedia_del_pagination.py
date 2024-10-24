#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size."""
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header row

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by original sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns paginated data with the original index and skips over deleted entries.
        """
        indexed_data = self.indexed_dataset()

        # Ensure the index is within valid range
        assert 0 <= index < len(indexed_data)

        data = []
        current_index = index
        next_index = index + page_size

        # Collect data while skipping over any gaps
        while len(data) < page_size and current_index < len(indexed_data):
            item = indexed_data.get(current_index)
            if item is not None:
                data.append(item)
            current_index += 1

        # Set next index to handle gaps in the dataset
        next_index = current_index

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }

