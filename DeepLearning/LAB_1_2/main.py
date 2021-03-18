
import funcs as fu
import numpy as np
import copy


weights_nn = [
[0.1, 0.1, -0.3],
[0.1, 0.2, 0.0],
[0.0, 1.3, 0.1]]


weights_dnn = [
    [
        [0.1, 0.2, -0.1],
        [-0.1, 0.1, 0.9],
        [0.1, 0.4, 0.1]
    ],
    [
        [0.3, 1.1, -0.3],
        [0.1, 0.2, 0.0],
        [0.0, 1.3, 0.1]
    ]
]

values_dnn = [
    [8.5, 0.65, 1.2],
    [9.5, 0.8, 1.3],
    [9.9, 0.8, 0.5],
    [9.0, 0.9, 1.0]
]

exp_out = [
    [0.1, 1, 0.1],
    [0, 1, 0],
    [0, 0, 0.1],
    [0.1, 1, 0.2]
]

def main():

    print(fu.neutral_network_RGB('RGB_teach.txt', 'RGB_test.txt'))



if __name__ == "__main__":

    main()