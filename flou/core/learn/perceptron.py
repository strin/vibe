# logistic regression through AdaGrad.
import math
import json

sigmoid = lambda z: 1./(1. + math.exp(-z))

def dict_dot(weight, ex):
    res = 0.
    for key in weight:
        if key not in ex:
            continue
        res += weight[key] * ex[key]
    return res


def dict_mul_scalar(ex, scalar):
    res = dict(ex)
    print res
    for key in res:
        res[key] *= scalar
    return res


def dict_sqr(ex):
    return {key: val ** 2 for (key, val) in ex.items()}


class Perceptron(object):
    def __init__(self, lr=1., weight={'__bias__': 0.}, G2={}):
        self.lr = lr
        self.delta = 1e-4
        self.weight = weight
        self.G2 = G2


    def train(self, exs, labels):
        '''
        labels are 0 (dislike), 1 (like).
        '''
        for (ex, label) in zip(exs, labels):
            # add bias.
            if '__bias__' not in ex:
                ex['__bias__'] = 1.
            # compute gradient.
            resp = sigmoid(dict_dot(self.weight, ex))
            grad = dict_mul_scalar(ex, resp - float(label))
            grad2 = dict_sqr(grad)
            for key in grad2:
                if key not in self.G2:
                    self.G2[key] = self.delta
                self.G2[key] += grad2[key]

            # update weights.
            for key in grad:
                if key not in self.weight:
                    self.weight[key] = 0.
                self.weight[key] -= self.lr * grad[key] / math.sqrt(self.G2[key])


    def score(self, ex):
        '''
        return probability of 'like' between 0 and 1
        '''
        resp = sigmoid(dict_dot(self.weight, ex))
        return resp


    def to_dict(self):
        return {
            'weight': self.weight,
            'G2': self.G2,
            'lr': self.lr,
            'delta': self.delta
        }


    def to_json(self):
        return json.dumps(self.to_dict())








