import funcs as fu
import numpy as np
import random
import struct


input_img = [
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0]
]

fil_ter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

out_img = [
    [4, 3, 4],
    [2, 4, 3],
    [2, 3, 4]
]

'''Results:

Task 2:
    For 1000-10000-0.01:
    Iter 0: 70.04%, Iter 10: 82,98%, Iter 20: 84,95%,
    Iter 30: 85,58%, Iter 40: 85,73%

    For  10000-10000-0.01:
    Iter 0: 87.34%, Iter 10: 91.14%, Iter 20: 92.08%,
    Iter 30 93.4%, Iter 40: 92.77%

    For  60000-10000-0.01:
        Takes to long :)

Task 3:
    I created a memory monster

    For 1000-10000-0.01:
    Iter 0: 64.8%. I took so much time that I decided
    stop it. Pooling takes so much time...
    Maybe another/faster way to pool images?

'''


def main():

    #print(fu.convolutional_1(input_img, fil_ter, 1, 0))

    net = fu.ConvoNet()

    net.add_layer_convo(16, 3, 3, fu.reLU, fu.reLU_deriv, -0.01, 0.01)
    net.set_alpha(0.01)

    imgs_train = []
    exp_on_imgs_train = []
    imgs_test = []
    exp_on_imgs_test = []

    with open("../LAB_3/train-images", 'rb') as f_img, open("../LAB_3/train-labels", 'rb') as f_lab:

        f_img.read(4)
        f_lab.read(8)

        no_img = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col *= int.from_bytes(f_img.read(4), byteorder='big',signed=False)

        for x in range(no_img):

            values = np.array([x/255 for x in f_img.read(row_col)]).reshape(28, 28)
            imgs_train.append(values)
            exp_on_imgs_train.append(net.create_output(f_lab.read(1)[0], 10))


    with open('../LAB_3/t10k-images', 'rb') as f_img, open('../LAB_3/t10k-labels', 'rb') as f_lab:

        f_img.read(4)
        f_lab.read(8)

        no_img = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col *= int.from_bytes(f_img.read(4), byteorder='big',signed=False)

        for x in range(no_img):

            values = np.array([x/255 for x in f_img.read(row_col)]).reshape(28, 28)

            imgs_test.append(values)
            exp_on_imgs_test.append(f_lab.read(1)[0])


    for a in range(50):

        for x in range(1000):

            net.fit(imgs_train[x], 3, 3, 1, exp_on_imgs_train[x])

        if a % 10 == 0:

            many = 0
            for x in range(no_img):
                ret_net = net.use(imgs_test[x], 3, 3, 1)
                
                if ret_net == exp_on_imgs_test[x]:
                    many += 1
            print("Iter: {}, Test accuracy: {}%\n".format(a, many/100))


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