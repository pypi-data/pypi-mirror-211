import sys
sys.path.append('./openirt')
from item_model import ItemModel
from typing import Union
import numpy as np
import matplotlib.pyplot as plt

class PL2(ItemModel):
    def prob(self, ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]) -> np.ndarray:
        """
        Calculate the probability of a correct response given the ability and item parameters.

        Args:
            ability: A list, numpy array, or float representing the ability of the individual.
            params: A list or numpy array containing the item parameters.

        Returns:
            A numpy array representing the probabilities of correct responses.
        """
        items = np.array(params).shape[1]
        num_abilities = 1
        if np.array(ability).shape != ():
            num_abilities = np.array(ability).shape[0]
        ability = np.tile(np.array([ability]).transpose(), (1, items))

        params = np.tile(params, num_abilities).reshape((2, num_abilities, items))
        return 1 / (1 + np.exp(-params[0] - (params[1] * ability)))

    def estimate_parameters(self, ability: Union[list, np.ndarray], result: Union[list, np.ndarray],
                            sigm_orig=-1, lamb_orig=1, end=0.00001, eps=0.1) -> np.ndarray:
        """
        Estimate the parameters of the model given the abilities and item responses.

        Args:
            ability: A list or numpy array containing the abilities of individuals.
            result: A list or numpy array representing the item responses.
            sigm_orig: The initial value for the parameter sigm.
            lamb_orig: The initial value for the parameter lamb.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated parameters.
        """
        ability = np.array(ability)
        result = np.array(result)
        est = [sigm_orig, lamb_orig]
        prev_est = [0, 0]
        while abs(est[0] - prev_est[0]) > end or abs(est[1] - prev_est[1]) > end:
            P = self.prob(ability, [[est[0]], [est[1]]]).transpose()[0]
            W = P * (1 - P)
            L11 = -np.sum(W)
            L12 = -np.sum(ability * W)
            L22 = -np.sum(ability**2 * W)
            L = np.array([[L11, L12], [L12, L22]])
            if abs(np.linalg.det(L)) < eps:
                break
            L_inv = np.linalg.inv(L)

            obs_mat = np.array([np.sum(result - P), np.sum((result - P) * ability)])
            prev_est = est
            est = est - np.matmul(L_inv, obs_mat)
        return est

    def estimate_ability(self, params: Union[list, np.ndarray], results: Union[list, np.ndarray],
                         end=0.00000001, eps=0.01) -> np.ndarray:
        """
        Estimate the ability of an individual given the item parameters and responses.

        Args:
            params: A list or numpy array representing the item parameters.
            results: A list or numpy array representing the item responses.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated ability.
        """
        params = np.array(params)
        results = np.array(results)
        est = 0.5
        prev_est = 0
        while abs(est - prev_est) > end:
            P = self.prob(est, params)[0]
            W = (1 - P) * P
            denom = np.sum(params[1]**2 * W)
            if abs(denom) < eps or np.any(np.abs(W) < eps):
                break
            prev_est = est
            est = est + (np.sum(params[1] * W * ((results - P) / W)) / denom)
        return est
    
    def convert_param_form(self, params):
        """
        Convert item parameters from one form to another.

        Args:
            params: A list or numpy array representing the item parameters.

        Returns:
            A numpy array representing the converted item parameters.
        """
        return np.array([-params[0] / params[1], 1 / params[1]])

    def plot_item_curve(self, p):
        """
        Plot item curves for given item parameters.

        Args:
            p: A numpy array representing the item parameters.
        """
        ability = np.linspace(-4, 4, 100)
        for i in range(p.shape[1]):
            plt.plot(ability, self.prob(ability, p[:,i].reshape(p.shape[0], 1)), label=f'Question{i+1}')
        plt.legend()
        plt.show()
