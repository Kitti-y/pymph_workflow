import multiprocessing as mp

def worker(x):
    return x*x

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:   # use 4 parallel processes
        results = pool.map(worker, [1, 2, 3, 4, 5, 6])
    print(results)