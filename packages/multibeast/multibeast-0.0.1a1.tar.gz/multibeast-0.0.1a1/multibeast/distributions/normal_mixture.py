import torch
import torch.distributions as D

from ..builder import __Distribution__


@__Distribution__.register()
class NormalMixture(D.Distribution):
    def __init__(self, mean, log_scale, logit_probs, temperature=1.0):
        batch_shape = log_scale.shape[:-1]
        event_shape = mean.shape[len(batch_shape) + 1 :]
        super().__init__(batch_shape, event_shape, None)

        mix_ = D.Categorical(logits=logit_probs)
        comp = D.Independent(D.Normal(mean, torch.exp(log_scale) * temperature), 1)
        dist = D.MixtureSameFamily(mix_, comp)

        self.dist = dist
        # see https://github.com/ikostrikov/jaxrl/blob/8ac614b0c5202acb7bb62cdb1b082b00f257b08c/jaxrl/networks/policies.py#L47
        # https://pytorch.org/docs/stable/distributions.html#mixturesamefamily

        # TODO: sigmoid or tanh when gaussianpolicy?
        # https://github.com/rail-berkeley/rlkit/blob/354f14c707cc4eb7ed876215dd6235c6b30a2e2b/rlkit/torch/sac/policies/gaussian_policy.py#L132

    def log_prob(self, value):
        log_probs = self.dist.log_prob(value)
        assert log_probs.shape == value.shape
        return log_probs

    def sample(self):
        return self.dist.sample()

    @property
    def mean(self):
        return self.dist.mean
