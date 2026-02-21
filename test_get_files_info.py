from functions.get_files_info import get_files_info

def main():
    contents = get_files_info("calculator", ".")
    print(f"Result for current directory:")
    print(contents)

    contents = get_files_info("calculator", "pkg")
    print(f"Result for 'pkg' directory:")
    print(contents)

    contents = get_files_info("calculator", "/bin")
    print(f"Result for '/bin' directory:")
    print(contents)

    contents = get_files_info("calculator", "../")
    print(f"Result for '../' directory:")
    print(contents)

if __name__ == "__main__":
    main()


