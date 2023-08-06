__all__ = ["NoncentralChi2"]

import jax.numpy as jnp
import jax.random as random
import jax.scipy as jsp
import tensorflow_probability.substrates.jax as tfp
from jax import lax
from numpyro.distributions import constraints
from numpyro.distributions.distribution import Distribution
from numpyro.distributions.util import (
    is_prng_key,
    promote_shapes,
    validate_sample,
)


def _random_chi2(key, df, shape=(), dtype=jnp.float_):
    return 2.0 * random.gamma(key, 0.5 * df, shape=shape, dtype=dtype)


class NoncentralChi2(Distribution):
    arg_constraints = {
        "df": constraints.positive,
        "nc": constraints.positive,
    }
    support = constraints.positive
    reparametrized_params = ["df", "nc"]

    def __init__(self, df, nc, validate_args=None):
        self.df, self.nc = promote_shapes(df, nc)
        batch_shape = lax.broadcast_shapes(jnp.shape(df), jnp.shape(nc))
        super(NoncentralChi2, self).__init__(
            batch_shape=batch_shape, validate_args=validate_args
        )

    def sample(self, key, sample_shape=()):
        # Ref: https://github.com/numpy/numpy/blob/
        # 89c80ba606f4346f8df2a31cfcc0e967045a68ed/numpy/
        # random/src/distributions/distributions.c#L797-L813
        assert is_prng_key(key)
        shape = sample_shape + self.batch_shape + self.event_shape

        key1, key2, key3 = random.split(key, 3)

        i = random.poisson(key1, 0.5 * self.nc, shape=shape)
        n = random.normal(key2, shape=shape) + jnp.sqrt(self.nc)
        cond = jnp.greater(self.df, 1.0)
        chi2 = _random_chi2(
            key3,
            jnp.where(cond, self.df - 1.0, self.df + 2.0 * i),
            shape=shape,
        )
        return jnp.where(cond, chi2 + n * n, chi2)

    @validate_sample
    def log_prob(self, value):
        # Ref: https://github.com/scipy/scipy/blob/
        # 500878e88eacddc7edba93dda7d9ee5f784e50e6/scipy/
        # stats/_distn_infrastructure.py#L597-L610
        df2 = self.df / 2.0 - 1.0
        xs, ns = jnp.sqrt(value), jnp.sqrt(self.nc)
        res = (
            jsp.special.xlogy(df2 / 2.0, value / self.nc)
            - 0.5 * (xs - ns) ** 2
        )
        corr = tfp.math.bessel_ive(df2, xs * ns) / 2.0
        return jnp.where(
            jnp.greater(corr, 0.0),
            res + jnp.log(corr),
            -jnp.inf,
        )

    @property
    def mean(self):
        return self.df + self.nc

    @property
    def variance(self):
        return 2.0 * (self.df + 2.0 * self.nc)
