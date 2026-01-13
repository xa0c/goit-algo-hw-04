def merge_k_lists(lists: list[list[int]]) -> list[int]:
    """Merge sorted lists into one sorted list.

    Args:
        lists (list[list[int]]): List of sorted lists.

    Returns:
        list[int]: Merged sorted list.
    """
    merged: list[int] = []
    indexes = [0] * len(lists)

    # Lists traversal loop
    while True:
        min_item = None
        list_i_with_min_item = None
        for i, shift in enumerate(indexes):
            # Skip lists which reached their end
            if shift == len(lists[i]):
                continue
            # Determine minimum item and its list
            if min_item is None or lists[i][shift] < min_item:
                min_item = lists[i][shift]
                list_i_with_min_item = i
        # Leave traversal loop if nothing left to sort
        if min_item is None:
            break
        # Add minimum value to the merged list and continue with remaning items
        merged.append(min_item)
        indexes[list_i_with_min_item] += 1

    return merged


if __name__ == "__main__":
    samples = [
        [[1, 4, 5], [1, 3, 4], [2, 6]],
        [[1, 4, 5], [-1, 3, 4], [-2, 6]],
        [[1, 4, 5], [], [2, 6]],
        [[], [], []],
        [[]],
        [],
    ]

    for sample in samples:
        print("Initial lists:", sample)
        print("Merged result:", merge_k_lists(sample))
        print()
