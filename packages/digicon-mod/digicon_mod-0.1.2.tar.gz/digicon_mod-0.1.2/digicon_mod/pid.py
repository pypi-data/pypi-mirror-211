import typing
from . import plc


class PidController(plc.PLC):

    def __init__(self, goal: float, k_p: float, k_i: float, k_d: float,
                 gain: float, step: float) -> None:
        super().__init__(gain=gain, step=step)
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.ei = 0
        self.prev_e = 0
        self.goal = goal

    def control(self, x: typing.List[float], t: float) -> float:
        e = x[0] - self.goal
        self.ei = self.ei + e
        ed = e - self.prev_e
        return self.k_p * e + self.k_i * self.ei + self.k_d * ed
