def main_func():
    array = []
    n = int(input("Enter size of array(natural number): "))

    for _ in range(n):
        num = input(f"Enter element {_} of array(natural number): ")
        array.append(int(num))

    k = int(input("Enter k number(natural number, <n): "))

    if k >= n:
        raise ValueError("K MUST BE LESS THEN N")

    max_avg = 0
    index = -1

    for zero_index in range(n-k):
        avg = sum(array[zero_index:zero_index+k]) / len(array[zero_index:zero_index+k])
        if avg > max_avg:
            index = zero_index
            max_avg = avg

    print(f"Max arithmetical mean value is {max_avg}. Index of the first element is {index}")


if __name__ == "__main__":
    try:
        main_func()
    except ValueError:
        print("Something gone wrong with input values")
    except ZeroDivisionError:
        print("Something gone wrong with input values")
