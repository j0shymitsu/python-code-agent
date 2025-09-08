from functions.get_files_info import get_files_info

def main():
    print("Result for the current directory:")
    print(get_files_info("calculator", "."))
    print()

    print("Result for the 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()

    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()

    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()


