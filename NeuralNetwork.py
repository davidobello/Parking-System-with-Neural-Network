import numpy as np
import os

from tensorflow.python.keras.utils.version_utils import training


class ReLU:
    def forward(self, z):
        return np.maximum(z,0)

    def backward(self,z):
        return (z > 0).astype(float)


class Softmax:
    def forward(self,z):
        exp = np.exp(z - np.max(z,axis=1, keepdims=True))
        return exp/np.sum(exp, axis=1, keepdims=True)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, saved_data_path=None):
        if saved_data_path and os.path.exists(saved_data_path):
            loaded_data = np.load(saved_data_path)

            self.w1 = loaded_data['w1']
            self.w2 = loaded_data['w2']

            self.b1 = loaded_data['b1']
            self.b2 = loaded_data['b2']
        else:
            self.w1 = np.random.randn(input_size, hidden_size) * 0.01
            self.b1 = np.zeros((1, hidden_size))

            self.w2 = np.random.randn(hidden_size, output_size) * 0.01
            self.b2 = np.zeros((1, output_size))

        self.activation1 = ReLU()
        self.activation2 = Softmax()

    def forward(self, X):
        """Input layer to Hidden layer"""
        self.z1 = X @ self.w1 + self.b1
        self.a1 = self.activation1.forward(self.z1)

        """Hidden layer to Output layer"""
        self.z2 = self.a1 @ self.w2 + self.b2
        self.a2 = self.activation2.forward(self.z2)

        return self.a2

    def mutate(self, mutation_rate=0.01, mutation_strength=0.05):
        """Mutate weights and biases of w1, b1, w2, b2"""
        mutation_mask_w1 = np.random.rand(*self.w1.shape) < mutation_rate
        self.w1 += mutation_mask_w1 * np.random.randn(*self.w1.shape) * mutation_rate

        mutation_mask_b1 = np.random.rand(*self.b1.shape) < mutation_rate
        self.b1 += mutation_mask_b1 * np.random.randn(*self.b1.shape) * mutation_rate

        mutation_mask_w2 = np.random.rand(*self.w2.shape) < mutation_rate
        self.w2 += mutation_mask_w2 * np.random.randn(*self.w2.shape) * mutation_rate

        mutation_mask_b2 = np.random.rand(*self.b2.shape) < mutation_rate
        self.b2 += mutation_mask_b2 * np.random.randn(*self.b2.shape) * mutation_rate


    def crossover(self, other_network):
        """Simulates generic cross over like combining DNA"""
        """self.w1.shape[0] = input size, w1 = weight matrix between input and hidden layer"""
        """.shape[0] means the number of rows, which is the number of input neurons"""
        """Hence, self.w1.shape[0] = size of input layer. The same applies hidden_size and output_size"""
        child = NeuralNetwork(self.w1.shape[0], self.w1.shape[0], self.w2.shape[1])


        """Crossover for weights; first part from self, rest from other_network/parents"""

        crossover_point_w1 = np.random.randint(1, self.w1.shape[0])
        child.w1[:crossover_point_w1] = self.w1[:crossover_point_w1]
        child[crossover_point_w1:] = other_network.w1[crossover_point_w1:]
        # Crossover for weights (half from self, half from other_network)
        crossover_point_w1 = np.random.randint(1, self.w1.shape[0])  # Random split for w1
        child.w1[:crossover_point_w1] = self.w1[:crossover_point_w1]
        child.w1[crossover_point_w1:] = other_network.w1[crossover_point_w1:]

        crossover_point_w2 = np.random.randint(1, self.w2.shape[0])  # Random split for w2
        child.w2[:crossover_point_w2] = self.w2[:crossover_point_w2]
        child.w2[crossover_point_w2:] = other_network.w2[crossover_point_w2:]

        # Crossover for biases (half from self, half from other_network)
        crossover_point_b1 = np.random.randint(1, self.b1.shape[1])
        child.b1[:crossover_point_b1] = self.b1[:crossover_point_b1]
        child.b1[crossover_point_b1:] = other_network.b1[crossover_point_b1:]

        crossover_point_b2 = np.random.randint(1, self.b2.shape[1])
        child.b2[:crossover_point_b2] = self.b2[:crossover_point_b2]
        child.b2[crossover_point_b2:] = other_network.b2[crossover_point_b2:]

        return child

    def save_data(self):
        """To save our widths and biases after training"""
        np.savez('saved_data', w1=self.w1, w2=self.w2, b1=self.b1, b2=self.b2)
