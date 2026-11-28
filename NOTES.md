**UCB1** (Upper Confidence Bound) — the canonical next step.

The paper: **Auer, Cesa-Bianchi & Fischer (2002)**, *"Finite-time Analysis of the Multiarmed Bandit Problem"*, *Machine Learning*, 47(2-3):235-256. [~4,800 citations](https://link.springer.com/article/10.1023/A:1013689704352).

**Why it's the natural next step:**

| | Epsilon-Greedy | UCB1 |
|---|---|---|
| Exploration strategy | Random (unguided) | Optimistic (directed toward high uncertainty) |
| Hyperparameter | Yes (ε) | No |
| Regret bound | O(εT) — linear | O(log T) — logarithmic (optimal) |
| Key insight | "Sometimes try random" | "Try the arm you're *most unsure* about" |

The core formula for UCB1:

```
a_t = argmax_i  [ x̄_i + sqrt(2 ln t / n_i) ]
```

Pick the arm that maximizes **average reward + confidence bonus**. Arms you haven't pulled much get a big bonus, so exploration is *automatic* and *directed* — no need to tune ε.

**The progression in the literature:**

```
Greedy → Epsilon-Greedy → UCB1 → Thompson Sampling
(simple)  (random explore)  (optimistic)   (Bayesian)
```

```markdown

# Bandits — Notes

## Module 1: Multi-Armed Bandits

### 1.1 Epsilon-Greedy

**Idea:** With probability ε, pick a random arm (explore). With probability 1−ε, pick the arm with the highest estimated reward (exploit).

**Hyperparameter:** ε (exploration rate). Too high → wastes pulls on bad arms. Too low → locks in on a suboptimal arm early.

**Regret bound:** O(εT) — linear in steps. Not optimal.

**Result (50,000 steps, ε=0.1, 5 arms, seed=42):**

```
True means:  [0.774 0.439 0.859 0.697 0.094]
Estimates:   [0.779 0.403 0.85  0.732 0.087]
Best arm:    2, estimated best: 2
```

- Optimal arm: ✓
- MAE (all arms): 0.018
- Uniformly accurate across all arms (keeps pulling everything randomly)

---

### 1.2 UCB1 (Upper Confidence Bound)

**Paper:** Auer, Cesa-Bianchi & Fischer (2002), *"Finite-time Analysis of the Multiarmed Bandit Problem"*, Machine Learning, 47(2-3):235-256.

**Idea:** Pick the arm that maximizes *average reward + confidence bonus*. Arms you haven't pulled much get a big bonus → exploration is automatic and directed. No hyperparameter.

**Formula:**

```
a_t = argmax_i  [ x̄_i + sqrt(2 ln t / n_i) ]
```

- `x̄_i` = running average reward for arm i
- `n_i` = number of times arm i has been pulled
- `t` = current step

**Regret bound:** O(log T) — logarithmic. Optimal (matches the lower bound).

**Result (50,000 steps, 5 arms, seed=42):**

```
True means:  [0.774 0.439 0.859 0.697 0.094]
Estimates:   [0.766 0.317 0.859 0.688 0.048]
Best arm:    2, estimated best: 2
```

- Optimal arm: ✓
- MAE (all arms): 0.037
- **Perfect estimate on best arm (0.000 error)**
- Poor estimates on suboptimal arms (arm 1: 0.122 error)

---

### Side-by-Side

| Metric | ε-greedy | UCB1 |
|--------|----------|------|
| Optimal arm identified | ✓ | ✓ |
| Error on best arm | 0.009 | **0.000** |
| MAE (all arms) | **0.018** | 0.037 |
| Hyperparameter | Yes (ε) | No |
| Regret bound | O(εT) | O(log T) |

**Key insight:** UCB1 optimizes the *decision* (find the best arm), not the *estimates*. Once it identifies the winner, it concentrates pulls there and starves the others. ε-greedy is more "fair" — it keeps pulling everything, so all estimates stay reasonable.

**When to use which:**
- ε-greedy: you want a good estimate of *all* arms (e.g., A/B testing where you need to know all conversion rates)
- UCB1: you just need to *pick the best one* as fast as possible (e.g., ad slot selection)

---

### Next: Thompson Sampling

**Idea:** Maintain a Beta distribution per arm. Each step, sample from each arm's posterior and pick the highest sample. Exploration is "natural" — arms with high uncertainty produce wide distributions, so they get sampled high more often.

**Paper:** Chapelle & Li (2011), *"An Empirical Evaluation of Thompson Sampling"*, NeurIPS.

```
Beta(α_i, β_i) per arm
  → sample θ_i ~ Beta(α_i, β_i)
  → pick argmax θ_i
  → update: if reward=1, α_i++; else β_i++
```

No hyperparameter. O(log T) regret in practice (theoretical bound is tighter than UCB1 in some settings).
```

Paste that into `NOTES.md`, save, and you're set for the next session when you build `thompson_sampling.py`. 🤙



