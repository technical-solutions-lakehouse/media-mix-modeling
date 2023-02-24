import numpy as np
import pymc3 as pm
import theano
import theano.tensor as tt
import warnings

warnings.filterwarnings('ignore', 'iteritems is deprecated')
warnings.filterwarnings('ignore', '`np.complex` is a deprecated')


def geometric_adstock_tt(x,alpha=0,L=12,normalize=True):
    '''
    Geometric Adstock Function

    :param alpha: rate of decay (float)
    :param L: Length of time carryover effects can have an impact (int)
    :normalize: Boolean
    :return transformed spend vector
    '''

    w = tt.as_tensor_variable([tt.power(alpha,i) for i in range(L)])
    xx = tt.stack([tt.concatenate([tt.zeros(i), x[:x.shape[0] - i]]) for i in range(L)])

    if not normalize:
        y = tt.dot(w, xx)
    else:
        y = tt.dot(w / tt.sum(w), xx)
    return y


def logistic_function(x_t, mu=0.1):
    """
    Nonlinear Saturation Function

    :param x_t: marketing spend vector (float)
    :param mu: half-saturation point (float)
    :return transformed spend vector
    """

    return (1 - np.exp(-mu * x_t)) / (1 + np.exp(-mu * x_t))