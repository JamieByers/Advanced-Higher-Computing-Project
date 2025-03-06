# Advanced Higher Concept - Binary Search Algorithm
def search(products, target: str, key="price"):
    left = 0
    right = len(products)-1
    target = target.strip().lower()

    while left <= right:
        middle = (left + right) // 2
        # get the current product using an inputted key e.g title and it would get the title value e.g Yellow Boots - this would be similar to Product.title, but this works with any key
        current_product = getattr(products[middle], key).strip().lower() if isinstance(getattr(products[middle], key), str) else getattr(products[middle], key)
        if current_product == target:
            print("Product found at index: "+middle)
            print("Product information: \n ", products[middle].display())
            return middle
        elif current_product < target:
            left = middle + 1
        else:
            right = middle - 1

    print("Product not found")
    return -1 