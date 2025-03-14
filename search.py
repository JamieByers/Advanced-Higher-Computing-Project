# import the bubble sort to use in this file 
from sort import ascending_sort

# Advanced Higher Concept - Binary Search Algorithm
def search(products, target: str, key="price"):
    left = 0
    right = len(products)-1

    # sort the products for the binary search to work properly
    products = ascending_sort(products, key)

    # turning target into a string prevents type mismatching
    target = str(target)
    # removing trailing spaces and turning it into lowercase will prevent it impacting the search process as the trailing spaces and lowercase will not affect the comparision
    target = target.strip().lower()

    while left <= right:
        middle = (left + right) // 2

        # get the current product using an inputted key e.g title and it would get the title value e.g Yellow Boots - this would be similar to Product.title, but this works with any key
        current_product = getattr(products[middle], key)
        # current product is then turned into a string so there is no type mismatching 
        current_product = str(current_product)
        # the currecnt product is input validated by removing any trailing spaces and uppercase letters which could affect the searching comparison
        current_product = current_product.strip().lower()

        if current_product == target:
            # print("Product found at index: "+str(middle))
            return middle
        elif current_product < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1 
