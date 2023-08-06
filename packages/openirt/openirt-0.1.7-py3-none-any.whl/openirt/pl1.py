from pathlib import Path
import sys
if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from openirt.item_model import ItemModel
from typing import Union
import numpy as np
from pl2 import PL2

class PL1(ItemModel):
    def prob(self, ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]) -> np.ndarray:
        """
        Calculate the probability of a correct response given the ability and item parameters.

        Args:
            ability: A list, numpy array, or float representing the ability of the individual.
            params: A list or numpy array containing the item parameters.

        Returns:
            A numpy array representing the probabilities of correct responses.
        """
        return PL2().prob(ability, [params[0], np.ones(len(params[0]))])

    def estimate_parameters(self, ability: Union[list, np.ndarray], result: Union[list, np.ndarray],
                            sigm_orig=0, end=0.0000001, eps=0.0001) -> np.ndarray:
        """
        Estimate the parameters of the model given the abilities and item responses.

        Args:
            ability: A list or numpy array containing the abilities of individuals.
            result: A list or numpy array representing the item responses.
            sigm_orig: The initial value for the parameter sigm.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated parameters.
        """
        ability = np.array(ability)
        result = np.array(result)
        est = sigm_orig
        prev_est = est + 2 * end
        while abs(est - prev_est) > end:
            P = self.prob(ability, [[est]]).transpose()[0]
            L1 = np.sum(result - P)
            L2 = -np.sum(P * (1 - P))

            if abs(L2) < eps:
                break

            prev_est = est
            est = est - L1 / L2
        return np.array([est])

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
        return PL2().estimate_ability([params[0], np.ones(len(params[0]))], results, end, eps)
