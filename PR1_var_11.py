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

    for zero_index in range(n-k+1):
        avg = sum(array[zero_index:zero_index+k]) / len(array[zero_index:zero_index+k])
        if avg > max_avg:
            index = zero_index
            max_avg = avg

    print(f"Max arithmetical mean value is {max_avg}. Index of the first element is {index}")


if __name__ == "__main__":
    while True:
        try:
            main_func()
            break
        except ValueError:
            print("Something gone wrong with input values, lets try again")
        except ZeroDivisionError:
            print("Something gone wrong with input values, lets try again")
