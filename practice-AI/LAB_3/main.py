import funcs as fu
import numpy as np
import struct


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

    net = fu.Neuron()

    net.add_layer(40, 784, fu.reLU, -0.1, 0.1)
    net.add_layer(10, weight_min_value=-0.1, weight_max_value=0.1)

    with open("train-images", 'rb') as f_img, open("train-labels", 'rb') as f_lab:

        f_img.read(4)
        f_lab.read(8)

        no_img = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col *= int.from_bytes(f_img.read(4), byteorder='big',signed=False)

        for x in range(no_img):

            values = [x/255 for x in f_img.read(row_col)]
            exp_out = net.create_output(f_lab.read(1)[0])
            net.fit(values, exp_out)

    with open('t10k-images', 'rb') as f_img, open('t10k-labels', 'rb') as f_lab:

        f_img.read(4)
        f_lab.read(8)

        no_img = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col *= int.from_bytes(f_img.read(4), byteorder='big',signed=False)

        many = 0
        for x in range(no_img):

            values = [x/255 for x in f_img.read(row_col)]

            ret_net = net.use(values)
            expected = f_lab.read(1)[0]
            
            if ret_net == expected:
                many += 1
        print(many)


if __name__ == "__main__":

    main()


'''
Another way to unpack bytes from a binary file:

print(struct.unpack('i', x)[0])

To create a file with an image by given pixel values use:

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

plt.imsave('filename.png', np.array(values).reshape(28, 28), cmap=cm.gray)
time.sleep(1)

You can display it too but in my case it didn't work.

plt.imshow(np.array(values).reshape(28, 28))

'''