import numpy as np
import random
import sys


def simple_deep_net(val, expected, weight, alpha, n):
    '''LAB_1_1 and LAB_2_1

    '''

    weight = np.array(weight)
    val = np.array(val)
    expected = np.array(expected)

    for x in range(n):
        
        predicted = val * weight
        delta = predicted - expected
        error = delta ** 2
        delta = delta * val
        delta = alpha * delta
        weight = weight - delta

    return predicted, error


def simple_deep_net_3(values, expected):
    '''LAB_1_2 and LAB_2_2

    '''

    weight = np.array([0.1, 0.2, -0.1])
    alpha = 0.01
    values = np.array(values)

    for y in range(1000):

        error = 0
        for x in range(len(values)):

            predicted = values[x] @ weight.T
            delta = predicted - expected[x]
            error += delta ** 2
            delta_weight = np.outer(delta, values[x])
            delta_weight = alpha * delta_weight
            weight = weight - delta_weight

        if y == 99:
            print(float(error))


def neutral_network(matrix, values, expected):
    '''LAB_1_3 and LAB_2_3

    '''

    if isinstance(matrix[0], list) and isinstance(values[0], list) and len(matrix[0]) == len(values[0]) and len(matrix) == len(expected):

        alpha = 0.01
        matrix = np.array(matrix)
        values = np.array(values)
        expected = np.array(expected)

        for y in range(100):

            error = [ 0, 0, 0]

            for x in range(len(values)):
                predicted = values[x] @ matrix.T
                delta = predicted - expected[x]
                error += delta ** 2
                delta_weight = np.outer(delta, values[x])
                delta_weight = alpha * delta_weight
                matrix = matrix - delta_weight

            if y == 49:
                print(sum(error))


def neutral_network_RGB(fileteach, filetest):
    '''LAB_2_4

    '''

    alpha = 0.01
    weight = np.random.random((4, 3))
    values = []

    with open(fileteach, 'r') as f:

        for line in f:

            line = line.split(' ')
            
            value = np.array([float(x) for x in line[:3]])

            line = line[3:]
            line[0:0] = [value]
            line[1] = line[1][0]

            values.append(line)


    for x in range(50):

        error = [0, 0, 0, 0]
        for value in values:
            
            if value[1] == '1':
                expected = [1.0, 0.0, 0.0, 0.0]

            elif value[1] == '2':
                expected = [0.0, 1.0, 0.0, 0.0]

            elif value[1] == '3':
                expected = [0.0, 0.0, 1.0, 0.0]

            else:
                expected = [0.0, 0.0, 0.0, 1.0]

            predicted = value[0] @ weight.T
            delta = predicted - expected
            error += delta ** 2
            delta_weight = np.outer(delta, value[0])
            weight = weight - alpha * delta_weight


    with open(filetest, 'r') as f:

        for line in f:

            line = line.split(' ')
            
            value = np.array([float(x) for x in line[:3]])

            try:

                predicted = value @ weight.T
                predicted = list(np.round(predicted, 1))
                x = predicted.index(max(predicted))

                if x != int(line[3][0]) - 1:
                    raise ValueError
                else:
                    print('YES')

            except ValueError:
                print('NO ||' + str(np.round(predicted, 1)) + '___' + str(expected) + '||')

    return weight


def deep_neutral_network(matrixes, values):
    '''Lab_1_4

    '''

    if isinstance(matrixes[0], list) and isinstance(values[0], list) and all([True for mat in matrixes for val in values if len(val) == len(mat[0])]):

        vals = np.array(values[0])

        for x in range(0, 2):
            
            mat = np.array(matrixes[x])

            vals = vals @ mat.T

        return vals


class Neuron():
    '''First added layer takes 3 input values LAB_2_4
    '''

    def __init__(self):
        self.values = []
        self.weights = []
        self.n_layers = 0


    def add_layer(self, n, weight_min_value=-1, weight_max_value=1):
        """Add a new layer

        """

        try:
            if n <= 0:
                raise ValueError
        except ValueError:
            print("You can not add a layer with 0 or less nodes!")
            sys.exit(1)


        if self.n_layers == 0:

            self.add_first_layer(n, 3)

        else:

            rand_layer = []

            for x in range(n):

                lay = []

                for y in range(len(self.weights[-1])):

                    lay.append(round(random.uniform(-1.0, 1.0), 2))

                rand_layer.append(lay)

            self.n_layers += 1
            self.weights.append(rand_layer)


    def add_first_layer(self, n, prev_n, weight_min_value=-1, weight_max_value=1):
        '''Create the first layer

        '''

        try:
            if n <= 0:
                raise ValueError
        except ValueError:
            print("You can not add a layer with 0 or less nodes!")
            sys.exit(1)

        rand_layer = []

        for x in range(n):

            lay = []

            for y in range(prev_n):

                lay.append(round(random.uniform(weight_min_value, weight_max_value), 2))

            rand_layer.append(lay)

        self.n_layers += 1
        self.weights[0:0] = [rand_layer]


    def predict(self, values):
        '''Add required layer if needed and calculate
        '''

        print(self.weights)

        if self.n_layers == 0:
            
            self.add_first_layer(3, len(values))

        elif len(self.weights[0][0]) != len(values):

            self.add_first_layer(len(self.weights[0][0]), len(values))

        self.values = values
        values = np.array(values)

        for x in range(self.n_layers):

            values = values @ np.array(self.weights[x]).T

        return values





