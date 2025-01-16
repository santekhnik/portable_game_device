def calculate_bcc(data):
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum

if __name__ == "__main__":
    arr = [12, 33, 44, 53, 2, 12]
    print("checksum:", calculate_bcc(arr))

    print("Hello world")