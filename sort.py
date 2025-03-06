# Advanced Higher Concept - Bubble Sort Algorithm
def ascending_sort(self, key="price"):

    # print unsorted array
    # print("Before: ")
    # print([getattr(p, key) for p in self.products]) # print only the key value of the product e.g only the product prices 

    swapped = True
    n = len(self.products)
    while n > 1 and swapped == True: # Only sort if there are products to sort and if the array is not sorted 
        swapped = False
        for i in range(n-1):
            # Search by the key inputted using getattr: this is instead of self.products[i].key. This means I dont have to write multiple search algorithms
            if getattr(self.products[i], key) > getattr(self.products[i + 1], key):
                self.products[i], self.products[i+1] = self.products[i+1], self.products[i]
                swapped = True

        n -= 1

    # print sorted array
    # print("After: ")
    # print([getattr(p, key) for p in self.products])
    return self.products

# Advanced Higher Concept - Bubble Sort Algorithm
def descending_sort(self, key="price"):

    # print unsorted array
    # print("Before: ")
    # print([getattr(p, key) for p in self.products]) # print only the key value of the product e.g only the product prices 

    swapped = True
    n = len(self.products)
    while n > 1 and swapped == True: # Only sort if there are products to sort and if the array is not sorted 
        swapped = False
        for i in range(n-1):
            # Search by the key inputted using getattr: this is instead of self.products[i].key. This means I dont have to write multiple search algorithms
            if getattr(self.products[i], key) < getattr(self.products[i + 1], key):
                self.products[i], self.products[i+1] = self.products[i+1], self.products[i]
                swapped = True

        n -= 1

    # print sorted array
    # print("After: ")
    # print([getattr(p, key) for p in self.products])
    return self.products