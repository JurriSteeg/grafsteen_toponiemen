def open_file(file_name):
    """Open txt files to read the content"""
    with open(file_name, "r") as f:
        return f.read()


def read(file):
    """extract the geocodes from the files"""
    file = file.rstrip()
    file = file.split("\n")
    codes = [line.split('"')[1] for line in file]
    
    return codes


def evaluate(test, gold):
    """perform the evaluation"""
    p = 0 # precision
    r = 0 # recall
    missed = 0 # missed tag

    for i in range(len(gold)):
        if test[i] != "":
            if test[i] == gold[i]:
                p += 1
            r += 1
        else:
            missed += 1

    p = p / r
    r = r / (r + missed)

    print("precision:", p)
    print("recall:", r)
    print("f-score:", 2*((p * r)/(p + r)))


def main():
    base1 = read(open_file("baseline1_codes.txt"))
    base2 = read(open_file("baseline2_codes.txt"))
    
    results = read(open_file("results_codes.txt"))

    gold = read(open_file("golden_codes.txt"))
    
    print("baseline 1")
    evaluate(base1, gold)
    print()
    print("baseline 2")
    evaluate(base2, gold)
    print()
    print("results")
    evaluate(results, gold)




    
    



if __name__ == '__main__':
    main()
