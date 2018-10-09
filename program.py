import fileinput

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line)
        print(line)

if __name__== "__main__":
    main()
