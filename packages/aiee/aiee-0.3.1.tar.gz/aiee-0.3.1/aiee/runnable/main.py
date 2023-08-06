import sys

from aiee.numbers import postfix_to_int


def main():
    print(postfix_to_int(sys.argv[1]))


if __name__ == '__main__':
    main()
