import torch


class StandardScaler:

    def __init__(self, with_mean: bool = True, with_std: bool = True):
        self.with_mean = with_mean
        self.with_std = with_std
        self.n_samples_seen = 0
        self.scale, self.mean, self.var = torch.zeros(0), torch.zeros(0), torch.zeros(0)

    def fit_transform(self, _input: torch.Tensor) -> torch.Tensor:
        self.partial_fit(_input)
        return self.transform(_input)

    def reset(self):
        self.n_samples_seen = 0
        return self

    def partial_fit(self, x: torch.Tensor):
        n_samples = x.shape[0]
        n_features = x.shape[1]
        if n_samples == 0:
            return
        if self.n_samples_seen == 0:
            self.scale = torch.zeros(n_features).to(x.device)
            self.mean = torch.zeros(n_features).to(x.device)
            self.var = torch.zeros(n_features).to(x.device)

        self.mean, self.var, self.n_samples_seen = incremental_mean_and_var(x, self.mean, self.var, self.n_samples_seen)

        self.scale = torch.where(self.var != 0, self.var, torch.ones(self.var.shape).to(x.device))
        self.scale = torch.sqrt(self.scale)

    def transform(self, x: torch.Tensor):
        x_out = x.clone()
        n_features = x.shape[1]
        for i in range(n_features):
            mean, scale = 0., 1.
            if self.with_mean:
                mean = self.mean[i]
            if self.with_std:
                scale = self.scale[i]
            for j in range(self.n_samples_seen):
                x_out[j, i] = (x[j, i] - mean) / scale
        return x_out

    def inverse_transform(self, x: torch.Tensor):
        x_out = x.clone()
        n_features = x.shape[1]
        for i in range(n_features):
            mean, scale = 0., 1.
            if self.with_mean:
                mean = self.mean[i]
            if self.with_std:
                scale = self.scale[i]
            for j in range(self.n_samples_seen):
                x_out[j, i] = mean + x[j, i] * scale
        return x_out


def incremental_mean_and_var(x: torch.Tensor, last_mean: torch.Tensor, last_variance: torch.Tensor,
                             last_sample_count: int):
    new_sample_count = x.shape[0]
    n_features = x.shape[1]
    last_sum = last_mean.clone()
    last_sum = torch.mul(last_sum, float(last_sample_count))
    new_sum = torch.zeros(n_features).to(x.device)
    for i in range(new_sample_count):
        new_sum = torch.add(new_sum, x[i])

    updated_sample_count = last_sample_count + new_sample_count
    updated_mean = torch.add(last_sum, new_sum)
    updated_mean = torch.mul(updated_mean, 1. / float(updated_sample_count))

    new_unnormalized_variance = torch.zeros(n_features).to(x.device)
    new_mean = torch.mul(new_sum, 1. / float(new_sample_count))

    for i in range(new_sample_count):
        tmp = torch.sub(x[i], new_mean)
        tmp = torch.pow(tmp, 2)
        new_unnormalized_variance = torch.add(new_unnormalized_variance, tmp)

    if last_sample_count == 0:
        updated_unnormalized_variance = new_unnormalized_variance.clone()
    else:
        last_over_new_count = float(last_sample_count) / float(new_sample_count)
        last_unnormalized_variance = last_variance.clone()
        last_unnormalized_variance = torch.mul(last_unnormalized_variance, float(last_sample_count))
        tmp = last_sum.clone()
        tmp = torch.mul(tmp, 1. / last_over_new_count)
        tmp = torch.add(tmp, new_sum)
        tmp = torch.pow(tmp, 2)
        tmp = torch.mul(tmp, last_over_new_count / float(updated_sample_count))

        updated_unnormalized_variance = last_unnormalized_variance.clone()
        updated_unnormalized_variance = torch.add(updated_unnormalized_variance, new_unnormalized_variance)
        updated_unnormalized_variance = torch.add(updated_unnormalized_variance, tmp)

    updated_variance = updated_unnormalized_variance.clone()
    updated_variance = torch.mul(updated_variance, 1. / float(updated_sample_count))

    return updated_mean, updated_variance, updated_sample_count
