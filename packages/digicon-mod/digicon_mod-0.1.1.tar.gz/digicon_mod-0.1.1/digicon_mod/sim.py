import numpy
import scipy.integrate
import typing
from . import plc


def calculate(func: typing.Callable, x0: typing.List[float],
              step: float, time: float, controller: plc.PLC
              ) -> typing.Mapping[str, typing.List[float]]:
    result = {'t': [], 'u': []}
    for i in range(0, len(x0)):
        result['x' + str(i + 1)] = []
    plc_step = controller.step
    ode_step = step
    time_v = numpy.linspace(0.0, time, int(time / plc_step + 1))
    for ti in time_v:
        uk = controller.output(x0, ti)
        tk = numpy.linspace(ti, ti + plc_step, int(plc_step / ode_step + 1))
        y = scipy.integrate.odeint(func(uk), x0, tk)
        x0 = y[-1]
        result['t'].extend(tk[:-1])
        for i in range(0, len(x0)):
            result['x' + str(i + 1)].extend(y[:-1, i])
        result['u'].extend([uk for i in tk[:-1]])

    return result
