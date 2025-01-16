def calculate_bcc(data):
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum

if __name__ == "__main__":
    arr = list(map(int, input("Enter numbers separated by spaces: ").split()))
    print("checksum:", calculate_bcc(arr))