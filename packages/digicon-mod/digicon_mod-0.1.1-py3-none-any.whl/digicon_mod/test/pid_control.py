import digicon_mod.plc
import digicon_mod.sim
import digicon_mod.pid
import typing
import numpy
import numpy.testing


def test_one_dim_pid() -> None:
    def system(uc: float) -> typing.Callable[[typing.List[float], float], typing.List[float]]:
        return lambda x, t: [x[0] + uc]

    goal = -1.0
    controller = digicon_mod.pid.PidController(
        goal=goal, k_p=-2.0, k_i=-0.05, k_d=0.0,
        gain=10, step=0.1
    )
    result = digicon_mod.sim.calculate(
        func=system, x0=[1.0], step=0.01,
        time=20, controller=controller
    )
    numpy.testing.assert_almost_equal(result['x1'][-1], goal, decimal=1)
