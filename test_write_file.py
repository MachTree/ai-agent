from functions.write_file import write_file

def test():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"Result for 'calculator/lorem.txt':")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"Result for 'pkg/morelorem.txt':")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"Result for '/tmp/temp.txt':")
    print(result)


if __name__ == "__main__":
    test()