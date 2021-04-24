import numpy as np
import random
import sys
from datetime import datetime




class Neuron():
    '''LAB_4_1

        Methods in a way that class can be expanded
        to the fully functional deeplearning class.
    '''

    def __init__(self):
        self.weights = []
        self.n_layers = 0
        self.alpha = 0.005
        self.activation_func = {}

    
    def set_alpha(self, val):
        '''Set alpha value.

        '''
        self.alpha = val


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

        if self.n_layers == 0:
            
            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, prev_n)))
        else:

            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, self.get_expected_many())))

        self.activation_func[self.get_layers()] = [activation_func]
        self.activation_func[self.get_layers()].append(activation_deriv)
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

        dropout = [[random.randint(0, 1) for y in range(len(self.weights[x]))] for x in range(len_weights-1)]

        predicted = hidden_layers_vals[0]

        for x in range(len_weights):

            predicted = predicted @ self.weights[x].T

            if self.activation_func[x][0] is not None:
                predicted = self.activation_func[x][0](predicted)

            if x + 1 < len_weights:
                predicted = predicted * dropout[x] * 2
                hidden_layers_vals.append(predicted)


        delta = predicted - exp_out
        #error = sum(delta**2)

        for x in range(len_weights-1, -1, -1):

            delta_prev = delta @ self.weights[x]
            
            if x > 0 and self.activation_func[x-1][1] is not None:
                delta_prev = delta_prev * self.activation_func[x-1][1](hidden_layers_vals[x])
                delta_prev  *= dropout[x-1]

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
            
            if self.activation_func[x][0] is not None:
                values = self.activation_func[x][0](values)

        values = list(values)
        return values.index(max(values))



class Neuron2():
    '''LAB_4_2 LAB_4_3

        Methods in a way that class can be expanded
        to the fully functional deeplearning class.
    '''

    def __init__(self):
        self.weights = []
        self.n_layers = 0
        self.alpha = 0.005
        self.activation_func = {}
        self.batch_grad_many = 0
        self.batch_grad = []
        self.batch_grad_out = []

    
    def set_alpha(self, val):
        '''Set alpha value.

        '''
        self.alpha = val


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

        if self.n_layers == 0:
            
            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, prev_n)))
        else:

            self.weights.append(np.random.uniform(weight_min_value, weight_max_value, (n, self.get_expected_many())))

        self.activation_func[self.get_layers()] = [activation_func]
        self.activation_func[self.get_layers()].append(activation_deriv)
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

        self.batch_grad.append(input_val)
        self.batch_grad_out.append(exp_out)
        self.batch_grad_many += 1

        if self.batch_grad_many == 100:

            self.batch_grad = np.array(self.batch_grad)
            self.batch_grad_out = np.array(self.batch_grad_out)

            len_weights = len(self.weights)
            hidden_layers_vals = [self.batch_grad]

            dropout = [np.array([[random.randint(0, 1) for y in range(len(self.weights[x]))] for a in range(self.batch_grad_many)]) for x in range(len_weights-1)]
            predicted = hidden_layers_vals[0]

            for x in range(len_weights):

                predicted = predicted @ self.weights[x].T


                if self.activation_func[x][0] is not None:
                    predicted = self.activation_func[x][0](predicted)

                if x + 1 < len_weights:
                    predicted = predicted * dropout[x] * 2
                    hidden_layers_vals.append(predicted)

            delta = (predicted - self.batch_grad_out)/self.batch_grad_many

            for x in range(len_weights-1, -1, -1):

                delta_prev = delta @ self.weights[x]

                if x > 0 and self.activation_func[x-1][1] is not None:
                    delta_prev = delta_prev * self.activation_func[x-1][1](hidden_layers_vals[x])
                    delta_prev  *= dropout[x-1]

                delta = delta.T @ hidden_layers_vals[x]
                self.weights[x] -= self.alpha * delta
                delta = delta_prev

            self.batch_grad = []
            self.batch_grad_out = []
            self.batch_grad_many = 0


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
            
            if self.activation_func[x][0] is not None:  # required?
                values = self.activation_func[x][0](values)

        values = list(values)
        return values.index(max(values))



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
