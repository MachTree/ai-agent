from functions.get_file_contents import get_file_contents
from config import MAX_CHARACTER_LIMIT

def test():
    contents = get_file_contents("calculator", "lorem.txt")
    print(f"Result for lorem.txt: {len(contents)} characters")
    concat_string = f"truncated at {MAX_CHARACTER_LIMIT} characters]"
    if contents.find(concat_string, -len(concat_string)) != -1:
        print("File successfully concatenated.")

    contents = get_file_contents("calculator", "main.py")
    print(f"Result for 'main.py':")
    print(contents)

    contents = get_file_contents("calculator", "pkg/calculator.py")
    print(f"Result for 'pkg/calculator.py':")
    print(contents)

    contents = get_file_contents("calculator", "/bin/cat")
    print(f"Result for '/bin/cat':")
    print(contents)

    contents = get_file_contents("calculator", "pkg/does_not_exist.py")
    print(f"Result for 'pkg/does_not_exist.py':")
    print(contents)


if __name__ == "__main__":
    test()