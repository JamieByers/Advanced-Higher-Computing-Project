class Searcher:
    def __init__(self, products):
        self.products = products

    def multi_search(self, arr, target, value):
        if not arr:
            return []

        # first binary serach to find the lower value
        left, right = 0, len(arr) - 1
        first = -1
        while left <= right:
            mid = (left + right) // 2
            current = getattr(arr[mid], value) # get the value from the array based on the inputted instance variable
            if current == target:
                first = mid
                right = mid - 1
            elif current < target:
                left = mid + 1
            else:
                right = mid - 1

        # if no lower value is found then end search
        if first == -1:
            return []

        # second binary search for the higher value
        left, right = first, len(arr) - 1 # only search from the lower value as the values before are meaningless
        last = first
        while left <= right:
            mid = (left + right) // 2
            current = getattr(arr[mid], value) # get the value from the array based on the inputted instance variable
            if current == target:
                last = mid
                left = mid + 1
            else:
                right = mid - 1

        # return all of the indices
        return list(range(first, last + 1))


