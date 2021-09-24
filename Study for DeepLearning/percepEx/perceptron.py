import numpy as np

class Perceptron():
    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate

    def fit(self, x, y):
        self.w = np.zeros(1+x.shape[1])  # setting w [0, ]

        error = -1
        epoch = 0
        print("epoch [", epoch, "]: ", self.w)

        while error != 0:
            # epoch
            self.w_ = self.w.copy()
            error = 0
            epoch += 1
            step = 0
            print("[", epoch, ", ", step, "]: ", self.w)
            for xi, y_ in zip(x, y):
                # step
                step += 1
                update = self.learning_rate * (y_ - self.learning(xi, self.w))
                self.w[1:] += update * xi
                self.w[0] += update
                if update < 0: error -= update
                else: error += update
                # print("[", epoch, ", ", step, "]: ", self.w)

            print("epoch [", epoch, "]: ", self.w)

        return self

    def net_input(self, x_, w_):
        return x_.dot(w_[1:].transpose()) + w_[0]

    def learning(self, x_, w_):
        return np.where(self.net_input(x_, w_) >= 0., 1, -1)

x = np.array([[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 0, 0]])
y = np.array([-1, 1, 1, 1, -1, -1, 1, -1])

ppn = Perceptron(learning_rate=0.1)
ppn.fit(x, y)