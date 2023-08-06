import lab as B
import wbml.util
from plum import convert
from wbml.data.predprey import load

from .data import DataGenerator, new_batch
from ..dist import AbstractDistribution
from ..dist.uniform import UniformDiscrete, UniformContinuous

__all__ = ["PredPreyGenerator", "PredPreyRealGenerator"]


def _predprey_step(state, x_y, t, dt, *, alpha, beta, delta, gamma, sigma):
    x = x_y[..., 0]
    y = x_y[..., 1]

    state, randn = B.randn(state, B.dtype(x), 2, *B.shape(x))
    dw = B.sqrt(dt) * randn

    deriv_x = x * (alpha - beta * y)
    deriv_y = y * (-delta + gamma * x)
    # Apply an exponent `1 / 6` to emphasise the noise at lower population levels and
    # prevent the populations from dying out.
    x = x + deriv_x * dt + (x ** (1 / 6)) * sigma * dw[0]
    y = y + deriv_y * dt - (y ** (1 / 6)) * sigma * dw[1]

    # Make sure that the populations never become negative. Mathematically, the
    # populations should remain positive. Note that if we were to `max(x, 0)`, then
    # `x` could become zero. We therefore take the absolute value.
    x = B.abs(x)
    y = B.abs(y)

    t = t + dt

    return state, B.stack(x, y, axis=-1), t


def _predprey_rand_params(state, dtype, batch_size=16):
    state, rand = B.rand(state, dtype, 5, batch_size)

    alpha = 0.2 + 0.6 * rand[0]
    beta = 0.04 + 0.04 * rand[1]
    delta = 0.8 + 0.4 * rand[2]
    gamma = 0.04 + 0.04 * rand[3]

    sigma = 0.5 + 9.5 * rand[4]

    return state, {
        "alpha": alpha,
        "beta": beta,
        "delta": delta,
        "gamma": gamma,
        "sigma": sigma,
    }


def _predprey_simulate(state, dtype, t0, t1, dt, t_target, *, batch_size=16):
    state, params = _predprey_rand_params(state, dtype, batch_size=batch_size)

    # Sort the target times for the validity of the loop below.
    perm = B.argsort(t_target)
    inv_perm = wbml.util.inv_perm(perm)
    t_target = B.take(t_target, perm)

    x_y = 5 + 95 * B.rand(dtype, batch_size, 2)
    t, traj = t0, []

    def collect(t_target, remainder=False):
        while B.shape(t_target, 0) > 0 and (t >= t_target[0] or remainder):
            traj.append((t, x_y))
            t_target = t_target[1:]
        return t_target

    # Run the simulation.
    t_target = collect(t_target)
    while t < t1:
        state, x_y, t = _predprey_step(state, x_y, t, dt, **params)
        t_target = collect(t_target)
    t_target = collect(t_target, remainder=True)

    # Concatenate trajectory into a tensor.
    t, traj = zip(*traj)
    t = B.to_active_device(B.cast(dtype, B.stack(*t)))
    traj = B.stack(*traj, axis=-2)

    # Undo the sorting.
    t = B.take(t, inv_perm)
    traj = B.take(traj, inv_perm, axis=-2)

    return state, t, traj


def _predprey_select_from_traj(t, y, t_target):
    inds = B.sum(B.cast(B.dtype_int(t), t_target[:, None] > t[None, :]), axis=1)
    return B.take(y, inds, axis=0)


class PredPreyGenerator(DataGenerator):
    """Predator–prey generator.

    Args:
        dtype (dtype): Data type to generate.
        noise (float, optional): Observation noise. Defaults to 0.
        seed (int, optional): Seed. Defaults to 0.
        num_tasks (int, optional): Number of tasks to generate per epoch. Must be an
            integer multiple of `batch_size`. Defaults to 2^14.
        batch_size (int, optional): Batch size. Defaults to 16.
        big_batch_size (int, optional): Size of the big batch. Defaults to 2048.
        dist_x (:class:`neuralprocesses.dist.dist.AbstractDistribution`, optional):
            Distribution of the inputs. Defaults to a uniform distribution over
            $[0, 100]$.
        dist_x_context (:class:`neuralprocesses.dist.dist.AbstractDistribution`,
            optional): Distribution of the context inputs. Defaults to `dist_x`.
        dist_x_target (:class:`neuralprocesses.dist.dist.AbstractDistribution`,
            optional): Distribution of the target inputs. Defaults to `dist_x`.
        num_context (:class:`neuralprocesses.dist.dist.AbstractDistribution`, optional):
            Distribution of the number of context inputs. Defaults to a uniform
            distribution over $[25, 100]$.
        num_target (:class:`neuralprocesses.dist.dist.AbstractDistribution`, optional):
            Distribution of the number of target inputs. Defaults to the fixed number
            100.
        device (str, optional): Device on which to generate data. Defaults to `"cpu"`.

    Attributes:
        dtype (dtype): Data type.
        float64 (dtype): Floating point version of `dtype` with 64 bits.
        int64 (dtype): Integer version of `dtype` with 64 bits.
        noise (float): Observation noise.
        num_tasks (int): Number of tasks to generate per epoch. Is an integer multiple
            of `batch_size`.
        batch_size (int): Batch size.
        big_batch_size (int): Sizes of the big batch.
        dist_x_context (:class:`neuralprocesses.dist.dist.AbstractDistribution`):
            Distribution of the context inputs.
        dist_x_target (:class:`neuralprocesses.dist.dist.AbstractDistribution`):
            Distribution of the target inputs.
        num_batches (int): Number batches in an epoch.
        num_context (:class:`neuralprocesses.dist.dist.AbstractDistribution`):
            Distribution of the number of context inputs.
        num_target (:class:`neuralprocesses.dist.dist.AbstractDistribution`):
            Distribution of the number of target inputs.
        state (random state): Random state.
        device (str): Device.
    """

    def __init__(
        self,
        dtype,
        seed=0,
        noise=0,
        num_tasks=2**14,
        batch_size=16,
        big_batch_size=2048,
        dist_x=UniformContinuous(0, 100),
        dist_x_context=None,
        dist_x_target=None,
        num_context=UniformDiscrete(25, 100),
        num_target=UniformDiscrete(100, 100),
        device="cpu",
    ):
        super().__init__(dtype, seed, num_tasks, batch_size, device)

        with B.on_device(self.device):
            self.noise = B.to_active_device(B.cast(self.float64, noise))

        self.dist_x_context = convert(dist_x_context or dist_x, AbstractDistribution)
        self.dist_x_target = convert(dist_x_target or dist_x, AbstractDistribution)

        self.num_context = convert(num_context, AbstractDistribution)
        self.num_target = convert(num_target, AbstractDistribution)

        self.big_batch_size = big_batch_size
        self._big_batch_t = None
        self._big_batch_y = None
        self._big_batch_num_left = 0

    def generate_batch(self):
        with B.on_device(self.device):
            if self._big_batch_num_left > 0:
                # There is still some available from the big batch. Take that.
                t, y = self._big_batch_t, self._big_batch_y[: self.batch_size]
                self._big_batch_y = self._big_batch_y[self.batch_size :]
                self._big_batch_num_left -= 1
            else:
                # For computational efficiency, we will not generate one batch, but
                # `multiplier` many batches.
                multiplier = max(self.big_batch_size // self.batch_size, 1)

                # Simulate the equations.
                self.state, t, y = _predprey_simulate(
                    self.state,
                    self.float64,
                    0,
                    100,
                    # Use a budget of 5000 steps.
                    100 / 5000,
                    # Generate observations at an $x$-resolution of `100 / 2000 = 0.05`.
                    B.linspace(self.float64, 0, 100, 2000),
                    batch_size=multiplier * self.batch_size,
                )

                # Save the big batch and rerun generation.
                self._big_batch_t = t
                self._big_batch_y = y
                self._big_batch_num_left = multiplier
                return self.generate_batch()

            set_batch, xcs, xc, nc, xts, xt, nt = new_batch(self, 2)
            x = B.concat(xc, xt, axis=-2)

            # Select the right elements from the simulation output.
            y = B.stack(
                *(
                    _predprey_select_from_traj(t, y[i, :, :], x[i, :, 0])
                    for i in range(self.batch_size)
                ),
                axis=0
            )

            # Add observation noise.
            self.state, randn = B.randn(self.state, y)
            y = y + B.abs(B.sqrt(self.noise) * randn)

            # Generate the batch.
            batch = {}
            set_batch(batch, y[:, :nc, :], y[:, nc:, :])
            return batch


class PredPreyRealGenerator(DataGenerator):
    def __init__(self, dtype):
        df = load()
