from filecense.templates import euplTop, euplFull
import os
import sys


def main():
    if len(sys.argv) != 2:
        raise RuntimeError("needs exactly one argument, a path to test")
        raise SystemExit

    path = sys.argv[1]
    print("testing in path: ", path)
    top_lic = euplTop.split("\n")[1:]

    tuples = os.walk(path, topdown=True)
    for root, dirs, files in tuples:
        for fil in files:
            print("checking file: ", fil)
            with open(root+"/"+fil, mode='r') as f:
                full_file = f.read()
            if f.name == "LICENSE":
                if not full_file == euplFull:
                    sys.exit("Error: Does not contain correct full license")
                else:
                    print("\tFile", f.name, ": OK")
                    continue
            for top_lic_line in top_lic:
                if top_lic_line not in full_file:
                    sys.exit("Error: File: '{}' does not contain license"
                             .format(f.name))
            print("\tFile", f.name, ": OK")


if __name__ == '__main__':
    main()
