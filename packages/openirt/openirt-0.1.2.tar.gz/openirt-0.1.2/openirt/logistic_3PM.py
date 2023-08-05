from item_model import ItemModel
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize    


class Logistic3PM(ItemModel):
    
    def prob(self, 
             ability: Union[list, np.ndarray, float], 
             params: Union[list, np.ndarray])  -> np.ndarray:
        items = np.array(params).shape[1]
        num_abilities = 1
        if np.array(ability).shape != ():
            num_abilities = np.array(ability).shape[0]
        ability = np.tile(np.array([ability]).transpose(), (1, items))

        params = np.tile(params, num_abilities).reshape(
            (3, num_abilities, items))
        return params[2] + (1 - params[2]) / (1 + np.exp(-params[0] * (ability - params[1])))
    
    def prob2PM(self,
                ability: Union[list, np.ndarray, float],
                params: Union[list, np.ndarray]) -> np.ndarray:
        items = np.array(params).shape[1]
        num_abilities = 1
        if np.array(ability).shape != ():
            num_abilities = np.array(ability).shape[0]
        ability = np.tile(np.array([ability]).transpose(), (1, items))

        params = np.tile(params, num_abilities).reshape(
            (3, num_abilities, items))
        return 1 / (1 + np.exp(-params[0] * (ability - params[1])))
    
    def estimate_parameters(self, 
                            ability: Union[list, np.ndarray], 
                            result: Union[list, np.ndarray],
                            a_orig=1,
                            b_orig=0.1, 
                            c_orig=0.1,
                            end=0.0000001,  
                            eps=0.1) -> np.ndarray:
        # use orig_params?
        ability = np.array(ability)
        result = np.array(result)
        est = np.array([a_orig, b_orig, c_orig])
        prev_est = est + 2 * end
        while np.all(np.abs(prev_est - est) > end):
            # self.plot_item_curve(est.reshape((3,1)))
            P = self.prob(ability, est.reshape((3,1))).T[0]
            Q = 1 - P
            P_2pm = self.prob2PM(ability, est.reshape((3,1))).T[0]
            
            L11 = -np.sum((ability-est[1])**2 * P * Q * (P_2pm/P)**2)
            L12 = np.sum(est[0] * (ability - est[1]) * P * Q * (P_2pm/P))
            L13 = -np.sum((ability - est[1]) * (Q / (1 - est[2])) * (P_2pm/P))
            
            L22 = -est[0]**2 * np.sum(P * Q * (P_2pm/P))
            L23 = np.sum(est[0] * (Q / (1 - est[2])) * (P_2pm/P))
            
            L33 = -np.sum((Q / (1 - est[2])) / (P - est[2]) * (P_2pm/P))

            L = np.array([[L11, L12, L13], [L12, L22, L23], [L13, L23, L33]])
            
            if abs(np.linalg.det(L)) < eps:
                print('break')
                break
            L_inv = np.linalg.inv(L)
            
            L1 = np.sum((result - P) * (ability - est[1]) * (P_2pm/P))
            L2 = -est[0] * np.sum((result - P) * (P_2pm/P))
            L3 = np.sum((result - P) / (P - est[2]) * (P_2pm/P))
            obs_mat = np.array([L1, L2, L3])
            prev_est = est
            est = est - np.matmul(L_inv, obs_mat)
        return est
    
    def estimate_ability(self,
                         params: Union[list, np.ndarray],
                         results: Union[list, np.ndarray],
                         end=0.00000001,
                         eps=0.01) -> np.ndarray:
        params = np.array(params)
        results = np.array(results)
        est = 0.5
        prev_est = 0
        while abs(est - prev_est) > end:
            P = self.prob(est, params)[0]
            Q = 1 - P
            P_2pm = self.prob2PM(est, params)[0]
            W = P_2pm * (1 - P_2pm)
            
            denom = - np.sum(params[0]**2 * W * (P_2pm/P)**2)
            
            print(denom)
            if abs(denom) < eps:
                break
            num = np.sum(params[0] * W * ((results - P) / (P * Q)) * (P_2pm/P))
            prev_est = est
            est = est + (num / denom)
        return est
    
    def plot_item_curve(self, p):
        ability = np.linspace(-5, 5, 100)
        for i in range(p.shape[1]):
            plt.plot(ability, self.prob(ability, p[:,i].reshape(p.shape[0], 1)), label=f'Question{i+1}')        
        plt.legend()
        plt.show()
