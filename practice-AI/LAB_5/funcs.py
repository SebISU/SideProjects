import numpy as np
import random
import sys
from datetime import datetime



def convolutional_1(img, fil_ter, conv_step, padding):
    '''LAB_5_1

    '''

    img  = np.pad(img, (padding, padding))

    img_width = len(img[0])
    img_height = len(img)
    fil_ter_width = len(fil_ter[0])
    fil_ter_height = len(fil_ter)

    batches = []

    for x in range(0, img_height - fil_ter_height + 1, conv_step):

        for y in range(0, img_width - fil_ter_width + 1, conv_step):

            batches.append(img[x:x+fil_ter_height, y:y+fil_ter_width].reshape(1, fil_ter_width*fil_ter_height)[0])

    fil_ter = np.array(fil_ter).reshape(1, fil_ter_width*fil_ter_height)[0]

    return (batches @ fil_ter.T).reshape(img_height - fil_ter_height + 1, img_width - fil_ter_width + 1)


class ConvoNet():
    '''LAB_5_2 5_3

        Methods in a way that class can be expanded
        to the fully functional deeplearning class.
    '''

    def __init__(self):
        self.weights = []
        self.n_layers = 0
        self.alpha = 0.01
        self.activation_func = {}


    def set_alpha(self, val):
        '''Set alpha value.

        '''
        self.alpha = val


    def get_layers(self):
        '''Return actual amount of layers

        '''

        return self.n_layers


    def add_layer(self, n, prev_n=3, activation_func=None, activation_deriv=None, weight_min_value=-1, weight_max_value=1):
        """Add a new layer

            n = amount of neurons in a layer
            prev_n = amount of neurons in a previous layer or amount of input values for the first layer
            acti = reLU or sth
            weights = range of initial weights
        """

        try:
            if n <= 0:
                raise ValueError
        except ValueError:
            print("You can not add a layer with 0 or less nodes!")
            sys.exit(1)

        self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, prev_n)))

        self.activation_func[self.get_layers()] = [activation_func]
        self.activation_func[self.get_layers()].append(activation_deriv)
        self.n_layers += 1


    def add_layer_convo(self, n, size_n, size_m, activation_func=None, activation_deriv=None, weight_min_value=-1, weight_max_value=1):
        """Add a new layer

            n = amount of filters in a layer
            size_n = filter height
            size_m = filter width
            acti = reLU or sth
            weights = range of initial weights
        """

        try:
            if n <= 0:
                raise ValueError
        except ValueError:
            print("You can not add a layer with 0 or less filters!")
            sys.exit(1)
            
        self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, size_n*size_m)))

        self.activation_func[self.get_layers()] = [activation_func]
        self.activation_func[self.get_layers()].append(activation_deriv)
        self.n_layers += 1


    def pooling(self, img, n, m, step):
        '''Reduce an image size. 

            img = pixels as a matrix
            n = pooling height
            m = pooling width
            step = pooling step
            if width or height % size_n/m != 0 ignore remaining
        '''

        info_array = np.zeros((len(img), len(img[0])))
        result = []

        for x in range(0, len(img) - n + 1, step):

            row = []
            for y in range(0, len(img[0]) - m + 1, step):

                value = np.amax(img[x:x+n, y:y+m])
                i, j = np.where(np.isclose(img[x:x+n, y:y+m], value))
                info_array[x+i[0]][y+j[0]] = 1
                row.append(value)

            result.append(row)
        
        return [np.array(result), info_array]


    def pooling_extend(self, img, img_extended):
        '''Extends and pools to the previous size with proper values.
        
        '''

        i = 0

        for x in range(len(img_extended)):

            for y in range(len(img_extended[0])):

                if img_extended[x][y] > 0:
                    img_extended[x][y] = img[i]
                    i += 1

        return img_extended


    def fit(self, img, fil_height, fil_width, conv_step, exp_out, padding=0):
        '''Train a convolutional deep net. 

        img = image as np.array
        fil_height = filter height
        fil_width = filter width
        conv_step = filter step
        exp_out = expected values list
        padding = input array padding
        '''

        img  = np.pad(img, (padding, padding))

        img_width = len(img[0])
        img_height = len(img)

        batches = []

        for x in range(0, img_height - fil_height + 1, conv_step):

            for y in range(0, img_width - fil_width + 1, conv_step):

                batches.append(img[x:x+fil_height, y:y+fil_width].reshape(1, fil_width*fil_height)[0])

        hidden_layer_vals = batches @ self.weights[0].T

        if self.activation_func[0][0] is not None:
            hidden_layer_vals = self.activation_func[0][0](hidden_layer_vals)

        pool_data = self.pooling(hidden_layer_vals, 2, 2, 2)

        if self.get_layers() < 2:
            self.add_layer(len(exp_out), len(pool_data[0]) * len(pool_data[0][0]), weight_min_value=-0.1, weight_max_value=0.1)

        pool_data[0] = pool_data[0].reshape(1, len(pool_data[0]) * len(pool_data[0][0]))[0]

        predicted = pool_data[0] @ self.weights[1].T

        if self.activation_func[1][0] is not None:
            predicted = self.activation_func[1][0](predicted)

        delta_2 = predicted - exp_out

        delta_1 = delta_2 @ self.weights[1]

        delta_1 = self.pooling_extend(delta_1, pool_data[1])

        if self.activation_func[0][1] is not None:
            delta_1 *= self.activation_func[0][1](hidden_layer_vals)

        delta_1 = delta_1.T @ batches

        delta_2 = delta_2[np.newaxis].T @ pool_data[0][np.newaxis]

        self.weights[0] -= self.alpha * delta_1
        self.weights[1] -= self.alpha * delta_2


    def create_output(self, index, many):
        '''Create a list of expected values by given index

        '''

        try:
            if index >= 0:
                return [0.0 if x != index else 1.0 for x in range(many)]
            else:
                raise IndexError
        except IndexError:
            print("Invalid index passed!")
            sys.exit(1)


    def use(self, img, fil_height, fil_width, conv_step, padding=0):
        '''Make use of neural network. 

        '''

        img  = np.pad(img, (padding, padding))

        img_width = len(img[0])
        img_height = len(img)

        batches = []

        for x in range(0, img_height - fil_height + 1, conv_step):

            for y in range(0, img_width - fil_width + 1, conv_step):

                batches.append(img[x:x+fil_height, y:y+fil_width].reshape(1, fil_width*fil_height)[0])

        hidden_layer_vals = batches @ self.weights[0].T
        
        if self.activation_func[0][0] is not None:
            hidden_layer_vals = self.activation_func[0][0](hidden_layer_vals)

        pool_data = self.pooling(hidden_layer_vals, 2, 2, 2)
        pool_data[0] = pool_data[0].reshape(1, len(pool_data[0]) * len(pool_data[0][0]))[0]
        
        predicted = pool_data[0] @ self.weights[1].T
        
        if self.activation_func[1][0] is not None:
            predicted = self.activation_func[1][0](predicted)

        predicted = list(predicted)
        return predicted.index(max(predicted))



def reLU(array):
    return array * (array > 0)

def reLU_deriv(array):
    return (array > 0)

def sigmoid(array):
    return 1 / (1 + np.exp(-array))

def sigmoid_deriv(array):
    return array * (1 - array)

def tanh(array):
    return (np.exp(array) - np.exp(-array)) / (np.exp(array) + np.exp(-array))

def tanh_deriv(array):
    return 1 - array ** 2

def softmax(array):
    '''Special function that standarizes output values so their sum is equal 1
    '''
    return np.exp(array)/sum(np.exp(array))
