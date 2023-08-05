from item_model import ItemModel
from typing import Union
import numpy as np
from logistic_2PM import Logistic2PM

class Logistic1PModel(ItemModel):
    
    def prob(self,
             ability: Union[list, np.ndarray, float], 
             params: Union[list, np.ndarray])  -> np.ndarray:
        return Logistic2PM().prob(ability, [params[0], np.ones(len(params[0]))])

    def estimate_parameters(self, 
                            ability: Union[list, np.ndarray], 
                            result: Union[list, np.ndarray], 
                            sigm_orig=0,
                            end=0.0000001,  
                            eps=0.0001) -> np.ndarray:
        ability = np.array(ability)
        result = np.array(result)
        est = sigm_orig
        prev_est = est + 2 * end
        while abs(est - prev_est) > end:
            P = self.prob(
                ability, [[est]]).transpose()[0]
            L1 = np.sum(result - P)
            L2 = -np.sum(P * (1 - P))

            if abs(L2) < eps:
                break
            
            prev_est = est
            est = est - L1 / L2
        return np.array([est])

    def estimate_ability(self,
                         params: Union[list, np.ndarray],
                         results: Union[list, np.ndarray],
                         end=0.00000001,
                         eps=0.01) -> np.ndarray:
        return Logistic2PM().estimate_ability([params[0], np.ones(len(params[0]))], results, end, eps)

