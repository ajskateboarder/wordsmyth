import multiprocessing as mp


def f(x):
    return x + 1


def main():
    ar = [1, 2, 3, 4, 5]
    pool = mp.Pool(processes=4)
    print(pool.map(f, ar))


if __name__ == "__main__":
    main()
