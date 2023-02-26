import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('A', help = "file A")
argparser.add_argument('B', help = "file B")
argparser.add_argument('-s', '--symmetric', action='store_true', help = "If this is set, only the symmetric difference will be printed with no additional information.")
args = argparser.parse_args()

def read(filename):
    with open(filename, "rt") as f:
        return set((line.strip() for line in f))

def print_iterable(xs):
    for x in xs:
        print(x)

filename_a = args.A
filename_b = args.B

a = read(filename_a)
b = read(filename_b)

if args.symmetric:
    print_iterable(a.symmetric_difference(b))
else:
    print(f'== Result of "{filename_a}" \\ "{filename_b}" ==')
    print_iterable(a.difference(b))
    print(f'\n== Result of "{filename_b}" \\ "{filename_a}" ==')
    print_iterable(b.difference(a))