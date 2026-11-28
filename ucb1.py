import numpy as np


def ucb1(n_arms=5, n_steps=1000, seed=42):
    rng = np.random.default_rng(seed)
    true_means = rng.uniform(0, 1, n_arms)
    counts = np.zeros(n_arms)
    values = np.zeros(n_arms)
    actions = []

    for t in range(1, n_steps + 1):
        if t <= n_arms:
            a = t - 1
        else:
            ucb = values + np.sqrt(2 * np.log(t) / counts)
            a = np.argmax(ucb)
        reward = rng.normal(true_means[a], 1.0)
        counts[a] += 1
        values[a] += (reward - values[a]) / counts[a]
        actions.append(a)

    return actions, true_means, values


actions, means, final_vals = ucb1(n_steps=50000)
print(f"True means:  {means.round(3)}")
print(f"Estimates:   {final_vals.round(3)}")
print(f"Best arm:    {np.argmax(means)}, estimated best: {np.argmax(final_vals)}")
