import funcs as fu
import numpy as np
import random
import struct

'''
Task 1 class Neuron():
    For 40-1000-10000:
        started with 5955 matches, after 50 iterations 8570,
        after 100 8581, after 150 8518, after 200 8482,
        after 250 8391, after 300 8471, after 350 8424

    For 40-10000-10000:
        started with 8202 matches, after 10 iterations 8949,
        after 50 9115, after 100 9166, after 150 9161,
        after 200 9161

    For 100-10000-10000:
        started with 8559 matches, after 5 iterations 9045,
        after 10 9185, after 20 9209, after 50 9333,
        after 100 9415, after 150 9397, after 200 9408,
        after 250 9405, after 282 9412

    For 100-60000-10000:
        started with 8350 matches, after 10 iterations 9206,
        after 20 9273, after 50 9316, after 100 9372,
        after 150 9386, after 200 9388, after 250 9388,
        after 300 9378, after 350 9393

Task 2 class Neuron2():
    For 40-1000-10000 0.001:
        started with 2890 matches, after 10 iterations 6117,
        after 20 6836, after 50 7932, after 100 8392,
        after 150 8527, after 200 8527, after 250 8587,
        after 300 8545, after 350 8519

    For 100-10000-10000 0.001:
        started with 7507 matches, after 10 iterations 8826,
        after 20 9049, after 50 9203, after 100 9289,
        after 150 9330, after 200 9365, after 250 9368,
        after 300 9381, after 350 9384

    For 100-60000-10000 0.0001:
        started with 3881 matches, after 10 iterations 7658,
        after 20 8146, after 50 8613, after 100 8871,
        after 150 8984, after 200 9074, after 250 9114,
        after 300 9146, after 350 9163

    For 100-1000-10000 0.001:
        started with 4318 matches, after 10 iterations 7414,
        after 20 7904, after 50 8383, after 100 8586,
        after 150 8668, after 200 8695, after 250 8744,
        after 300 8746, after 350 8743

Task 3 class Neuron2():
    For Alpha: 0.0002, training set size: 1000, test set size: 10000, weights : <-0.01, 0.01><-0.1, 0.1>, hidden units: 300
        Iter 0: 14.08% accuracy, Iter 350: 39.38%

    For Alpha: 0.0005, training set size: 1000, test set size: 10000, weights : <-0.01, 0.01><-0.1, 0.1>, hidden units: 300
        Iter 0: 6.05% accuracy, Iter 350: 50.0%

    For Alpha: 0.0002, training set size: 1000, test set size: 10000, weights : <-0.01, 0.01><-0.1, 0.1>, hidden units: 100
        Iter 0: 13.39% accuracy, Iter 350: 63.56%

    For Alpha: 0.0005, training set size: 1000, test set size: 10000, weights : <-0.01, 0.01><-0.1, 0.1>, hidden units: 100
        Iter 0: 8.8% accuracy, Iter 350: 43.0%

    You can fiddle with coefficients to get better accuracy :)
    
'''

def main():

    net = fu.Neuron2()

    net.add_layer(300, 784, fu.tanh, fu.tanh_deriv, -0.01, 0.01)
    net.add_layer(10, activation_func=fu.softmax, weight_min_value=-0.1, weight_max_value=0.1)
    net.set_alpha(0.0002)

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

            values = [x/255 for x in f_img.read(row_col)]
            imgs_train.append(values)
            exp_on_imgs_train.append(net.create_output(f_lab.read(1)[0]))


    with open('../LAB_3/t10k-images', 'rb') as f_img, open('../LAB_3/t10k-labels', 'rb') as f_lab:

        f_img.read(4)
        f_lab.read(8)

        no_img = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col = int.from_bytes(f_img.read(4), byteorder='big',signed=False)
        row_col *= int.from_bytes(f_img.read(4), byteorder='big',signed=False)

        for x in range(no_img):

            values = [x/255 for x in f_img.read(row_col)]

            imgs_test.append(values)
            exp_on_imgs_test.append(f_lab.read(1)[0])

    with open("Logs3_5tanh_softmax_divided.txt", "w") as f:

        f.write("Alpha: 0.0002, training set size: 1000, test set size: 10000, weights : <-0.01, 0.01><-0.1, 0.1>, hidden units: 300\n")

        for a in range(350):

            for x in range(1000):

                net.fit(imgs_train[x], exp_on_imgs_train[x])

            if a % 10 == 0:

                many = 0
                for x in range(no_img):
                    ret_net = net.use(imgs_test[x])
                    
                    if ret_net == exp_on_imgs_test[x]:
                        many += 1
                f.write("Iter: {}, Test accuracy: {}%\n".format(a, many/100))


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