import jax
import numpy as np
import pytest
import scipy.stats

from numpyro_ncx2 import NoncentralChi2


@pytest.mark.parametrize("args", [(5, 12.0), (50, 1.1), (1, 80.0)])
def test_sample(args):
    ref = scipy.stats.ncx2(*args)
    samples = NoncentralChi2(*args).sample(jax.random.PRNGKey(4), (10_000,))
    assert scipy.stats.kstest(samples, ref.cdf).statistic < 0.01


@pytest.mark.parametrize("args", [(5, 12.0), (50, 5.1), (1, 80.0)])
def test_logp(args):
    ref = scipy.stats.ncx2(*args)
    dist = NoncentralChi2(*args)
    samples = dist.sample(jax.random.PRNGKey(4), (5000,))
    np.testing.assert_allclose(
        ref.logpdf(samples), dist.log_prob(samples), rtol=2e-6
    )
