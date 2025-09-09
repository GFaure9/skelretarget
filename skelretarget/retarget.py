from abc import ABC, abstractmethod
import numpy as np


class SkelRetarget(ABC):
    def __init__(self, skel_def):
        self.skel_def = skel_def

    @abstractmethod
    def run(self, skels: np.ndarray) -> np.ndarray:
        pass