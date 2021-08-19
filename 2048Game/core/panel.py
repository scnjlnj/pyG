import os


class Table(object):
    def __init__(self):
        self.table = [[0]*4 for _ in range(4)]

    def print_in_str(self):
        os.system("cls")
        print("\n" * 3)
        for x in self.table:
            print(f"""\t{x[0]}\t{x[1]}\t{x[2]}\t{x[3]}\t""")

if __name__ == '__main__':
    while input():
        Table().print_in_str()