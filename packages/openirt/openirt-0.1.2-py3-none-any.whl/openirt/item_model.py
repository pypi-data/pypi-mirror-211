from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import matplotlib.pyplot as plt


class ItemModel():

    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def prob(self, ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]) -> np.ndarray:
        pass
    
    @abstractmethod
    def estimate_parameters(self, 
                            ability: Union[list, np.ndarray], 
                            result: Union[list, np.ndarray]) -> np.ndarray:
        pass
    
    @abstractmethod
    def estimate_ability(self, params: Union[list, np.ndarray], results: Union[list, np.ndarray]) -> np.ndarray:
        pass
    
    def train_em_mle(self, data) -> tuple:
        data = np.array(data)
        subjects, items = data.shape
        
        params = np.array([np.full(items, -1), np.full(items, 1)])
        for j in range(20):
            abilities = np.array([self.estimate_ability(params, data[i]) for i in range(subjects)])
            params = np.array([self.estimate_parameters(abilities, data[:,i]) for i in range(items)]).T
        return abilities, params
    
    def plot_item_curve(self, p):
        ability = np.linspace(-10, 10, 100)
        for i in range(p.shape[1]):
            prob = self.prob(ability, p[:,i].reshape(p.shape[0], 1))
            plt.plot(ability, self.prob(ability, p[:,i].reshape(p.shape[0], 1)), label=f'Question{i+1}')        
        plt.legend()
        plt.show()
    