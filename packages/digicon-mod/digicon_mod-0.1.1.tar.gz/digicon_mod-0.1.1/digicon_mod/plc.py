import abc
import numpy
import typing


class PLC(abc.ABC):
    def __init__(self, gain: float, step: float):
        self.last_t = 0.0
        self.last_call_t = 0.0
        self.last_u = 0
        self.step = step
        self.last_e = 0.0
        self.gain = gain
        self.u = []
        self.u_lim = []
        self.t = []

    @staticmethod
    def get_limited_output(value: float) -> float:
        return numpy.tanh(value)

    def add_output_value(self, time: float, value: float) -> None:
        self.t.append(time)
        self.u.append(value)
        self.u_lim.append(self.get_limited_output(value))

    def output(self, x: float, t: float) -> float:
        self.add_output_value(t, self.last_u)
        self.last_u = self.control(x, t)
        self.last_t = t
        self.add_output_value(t, self.last_u)

        return self.gain * self.u_lim[-1]

    @abc.abstractmethod
    def control(self, x: typing.List[float], t: float) -> float:
        raise NoImplementedException('No implementation')

