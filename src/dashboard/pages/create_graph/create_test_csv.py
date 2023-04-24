def test():
    f = open("longcsv.csv", "w")
    x = 0
    y = 1
    # 1*10**8 -> 1.8 gb csv fil
    # 1*10**7 -> 163 mb csv fil

    f.write("x,y\n")
    # set 10**X to determine the size of the created csv file
    for i in range(1 * 10**6):
        f.write(str(x) + "," + str(y) + "\n")
        x += 1
        y += 1
    f.close()


if __name__ == "__main__":
    test()
