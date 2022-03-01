def main():
    arr = [2, 5, 6, 2, 9, 4, 3, 9]
    sorted_arr = []
    print(arr)

    while len(arr) > 0:
        min_val = arr[0]
        for current_el in arr:
            if current_el <= min_val:
                min_val = current_el
        sorted_arr.append(min_val)
        arr.remove(min_val)

    print(sorted_arr)

if __name__ == '__main__':
    main()
