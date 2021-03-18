import numpy as np
import random
import sys
from datetime import datetime


def deep_neutral_network(weights, values):
    '''Lab_3_1

    '''

    if isinstance(weights[0], list) and isinstance(values[0], list) and all([True for mat in weights for val in values if len(val) == len(mat[0])]):

        for value in values:
            for weight in weights:

                mat = np.array(weight)
                value = value @ mat.T
                value = value * (value > 0)

        return value


def deep_neutral_network_2(weights, values, exp_out, alpha):
    '''Lab_3_2

    '''

    if isinstance(weights[0], list) and isinstance(values[0], list) and \
        all([True for mat in weights for val in values if len(val) == len(mat[0])]) and \
        len(values) == len(exp_out) and \
        len(weights[-1]) == len(exp_out[0]):

        for x in range(len(weights)):
            weights[x] = np.array(weights[x])

        for i in range(100):

            error = [0, 0, 0]
            for x in range(len(values)):

                prev_val = [0, 0, 0]
                predicted = values[x]
                for y in range(len(weights)):
                    
                    predicted = predicted @ weights[y].T
                    predicted *= (predicted > 0)
                    if y == len(weights) - 2:
                        prev_val = predicted

                delta_val2 = predicted - exp_out[x]
                error += delta_val2**2
                delta_val1 = delta_val2 @ weights[-1]
                delta_val1 *= (prev_val > 0)
                delta_val2 = np.outer(delta_val2, prev_val)
                delta_val1 = np.outer(delta_val1, values[x])
                weights[0] = weights[0] - alpha*delta_val1
                weights[-1] = weights[-1] - alpha*delta_val2

            if i == 49:
                print(sum(error))


def neutral_network_RGB_2(fileteach, filetest):
    '''LAB_3_3
        Task LAB_3_3 is almost the same as LAB_2_4 because
        there are no hidden layers. The only one difference
        is that the newer one uses ReLU func.

        Time and error after 10 loops:
        without ReLU - 0:00:00.069436
        sum_error_teach - 613.20
        with ReLU - 0:00:00.088924
        sum_error_teach - 463.27

        with ReLU 20% slower, but 1/3 more accurate
        (slower because func has to calculate ReLU each time)

        Use RGB.txt files from LAB_1_2
    '''

    date = datetime.now()

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

    sum_error = [0] * 4

    for x in range(10):

        error = [0] * 4
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
            predicted *= (predicted > 0)
            delta = predicted - expected
            error += delta ** 2
            delta_weight = np.outer(delta, value[0])
            weight = weight - alpha * delta_weight

        sum_error += error
    print(sum(sum_error))


    with open(filetest, 'r') as f:

        for line in f:

            line = line.split(' ')
            
            value = np.array([float(x) for x in line[:3]])

            try:

                predicted = value @ weight.T
                predicted *= (predicted > 0)
                predicted = list(np.round(predicted, 1))
                x = predicted.index(max(predicted))

                if x != int(line[3][0]) - 1:
                    raise ValueError
                else:
                    print('YES')

            except ValueError:
                print('NO')
                print('||' + str(np.round(predicted, 1)) + '___' + str(expected) + '||')

    print(datetime.now() - date)

    return weight


class Neuron():
    '''LAB_3_4

        Methods in a way that class can be expanded
        to the fully functional deeplearning class.
    '''

    def __init__(self):
        self.weights = []
        self.n_layers = 0
        self.alpha = 0.005
        self.activation_func = {}


    def add_layer(self, n, prev_n=3, activation_func=None, weight_min_value=-1, weight_max_value=1):
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

        if self.n_layers == 0:
            
            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, prev_n)))
        else:

            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, self.get_expected_many())))

        #could be a dict of lists to store activation func and derivative
        self.activation_func[self.n_layers] = activation_func
        self.n_layers += 1


    def get_layers(self):
        '''Return actual amount of layers

        '''

        return self.n_layers

    
    def get_input_many(self):
        '''Return amount of input values in the first layer

        '''

        if self.n_layers > 0:
            return len(self.weights[0][0])
        else:
            return 0


    def get_expected_many(self):
        '''Return amount of output values in the last layer

        '''

        if self.n_layers > 0:
            return len(self.weights[-1])
        else:
            return 0


    def fit(self, input_val, exp_out):
        '''Run a backtracking deep learning. 

        If no. of layers == 0 create a layer with
        proper amount of input and output values
        and default values of other arguments

        input = input values
        exp_out = expected values list
        '''

        if self.get_layers() == 0:
            self.add_layer(len(exp_out), len(input_val))

        try:
            
            if self.get_input_many() != len(input_val):
                raise ValueError

        except ValueError:

            print("Wrong amount of input values. Should be " + str(self.get_input_many()))
            sys.exit(1)

        try:

            if self.get_expected_many() != len(exp_out):
                raise ValueError
        
        except ValueError:

            print("Wrong amount of expected values. Should be " + str(self.get_expected_many()))
            sys.exit(1)

        len_weights = len(self.weights)
        hidden_layers_vals = [np.array(input_val)]
        
        predicted = hidden_layers_vals[0]

        for x in range(len_weights):

            predicted = predicted @ self.weights[x].T

            if self.activation_func[x] is not None:
                predicted = self.activation_func[x](predicted)

            if x + 1 < len_weights:
                hidden_layers_vals.append(predicted)

        delta = predicted - exp_out
        error = sum(delta**2)

        for x in range(len_weights-1, -1, -1):

            delta_prev = delta @ self.weights[x]
            
            #method should take the second activation function
            #(derivative of the main activation function)
            #in this case derivative of reLU for all
            if x > 0 and self.activation_func[x-1] is not None:
                delta_prev = delta_prev * (hidden_layers_vals[x] > 0)
            delta = np.outer(delta, hidden_layers_vals[x])
            self.weights[x] -= self.alpha * delta
            delta = delta_prev


    def create_output(self, index):
        '''Create a list of expected values by given index

        '''

        try:
            if index >= 0  and index < self.get_expected_many():
                return [0.0 if x != index else 1.0 for x in range(self.get_expected_many())]
            else:
                raise IndexError
        except IndexError:
            print("Invalid index passed!")
            sys.exit(1)


    def use(self, values):
        '''Make use of neural network. 

        '''

        try:
            if len(values) != self.get_input_many():
                raise ValueError
        except ValueError:
            print("Wrong amount of input values!")
            sys.exit(1)

        for x in range(len(self.weights)):

            values = values @ self.weights[x].T
            
            if self.activation_func[x] is not None:
                values = self.activation_func[x](values)

        values = list(values)
        return values.index(max(values))


def reLU(array):
    return array * (array > 0)