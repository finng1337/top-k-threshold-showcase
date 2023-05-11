import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
from processor.algorithms import get_k_naive, get_k_treshold, get_aggr_func
from processor.models import Processor
import time
import sys
sys.path.append("..")

def run():

    k = []
    sum = []
    max = []
    min = []
    naive = []
    data = list(Processor.objects.all())

    def test(count: int, fields: list[str]):
        k.append(count)
        start = time.time()
        get_k_treshold(count, data, fields, get_aggr_func('max'))
        max.append(time.time() - start)
        start = time.time()
        get_k_treshold(count, data, fields, get_aggr_func('min'))
        min.append(time.time() - start)
        start = time.time()
        get_k_treshold(count, data, fields, get_aggr_func('sum'))
        sum.append(time.time() - start)

    def plot(x: list[int], y: list[float], label: str):
        x_y_spline = make_interp_spline(x, y)
        x_ = np.linspace(1, 100000, 1000)
        y_ = x_y_spline(x_)

        plt.plot(x_, y_, label=label)
        
    for i in range(1, 100000, 10000):
        print(i)
        test(i, ['cores_desc', 'threads_desc'])

    print(100000)
    test(100000, ['cores_desc', 'threads_desc'])

    plot(k, max, 'treshold - max')
    plot(k, min, 'treshold - min')
    plot(k, sum, 'treshold - sum')
    #plt.plot(k, naive, label='naive')

    plt.xlabel('k')
    plt.ylabel('time [s]')
    plt.legend()

    plt.show()
    plt.savefig('graph22.png')