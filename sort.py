# Advanced Higher Concept - Bubble Sort Algorithm (Ascending order)
def ascending_sort(products, key="price"):
    swapped = True # initially set swapped to true 
    n = len(products) # get the length of the array and store it in the variable n 

    while n > 1 and swapped == True: # Only sort if there are products to sort and if the array is not sorted 
        swapped = False
        for i in range(n-1):
            # Search by the key inputted using getattr: this is instead of products[i].key. This means I dont have to write multiple search algorithms
            if getattr(products[i], key) > getattr(products[i + 1], key):
                products[i], products[i+1] = products[i+1], products[i]
                swapped = True

        n -= 1

    return products # return the sorted products

# Advanced Higher Concept - Bubble Sort Algorithm (Descending order)
def descending_sort(products, key="price"):
    swapped = True # initially set swapped to true 
    n = len(products) # get the length of the array and store it in the variable n 

    while n > 1 and swapped == True: # Only sort if there are products to sort and if the array is not sorted 
        swapped = False
        for i in range(n-1):
            # Search by the key inputted using getattr: this is instead of products[i].key. This means I dont have to write multiple search algorithms
            if getattr(products[i], key) < getattr(products[i + 1], key):
                products[i], products[i+1] = products[i+1], products[i]
                swapped = True

        n -= 1

    return products # return the sorted products


