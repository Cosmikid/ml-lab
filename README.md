# ml-lab

> Local-first machine learning experiments. No cloud dependencies.

A sandbox for testing ML pipelines on an AMD Ryzen 7 6800U with Radeon 680M (RDNA 2, 18 GB RAM). Everything runs locally — inference, embeddings, vector search.

## The Story

[From Blockchain to Machine Learning Local Silicon](STORY.md)

---

## Quick Start

### Prerequisites

| Component | Version | Location |
|-----------|---------|----------|
| Python | 3.14 (ml-lab), 3.12 (OpenWebUI) | system |
| Ollama | latest | `~/.ollama` |
| OpenWebUI | v0.13.5 | `~/openwebui/` |
| numpy | latest | `ml-lab/.venv` |

### Launch OpenWebUI (Z3PO + RAG)

```bash
source ~/openwebui/bin/activate
DATA_DIR=/home/daily/.open-webui open-webui serve
```

→ **http://localhost:8080** (admin login)

### Run the Epsilon-Greedy Agent

```bash
cd ~/ml_projects/bandits
pip install numpy  # first time only
python epsilon_greedy.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AMD Ryzen 7 6800U / Radeon 680M (Vulkan) / 18 GB RAM      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Ollama (qwen3.5:9b)                                       │
│       │                                                     │
│       ▼                                                     │
│  OpenWebUI v0.13.5 (port 8080)                             │
│       │                                                     │
│       ├── Knowledge (RAG)                                   │
│       │     ├── embed.py (chunk + nomic-embed-text)         │
│       │     ├── ChromaDB (file-based vector store)          │
│       │     ├── retrieve.py (top-5 chunks)                  │
│       │     └── generate.py (Z3PO context → answer)         │
│       │                                                     │
│       └── Z3PO (agent with Intent)                          │
│                                                             │
│  epsilon_greedy.py (standalone, CPU)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RAG Pipeline

```
data/sample_wiki.md (Karpathy wiki)
    → embed.py (chunk 1500 chars, paragraph-aware + nomic-embed-text 768-dim)
    → ChromaDB (persistent, file-based, no server)
    → retrieve.py (top-5 most relevant chunks)
    → generate.py (injects context → Z3PO via Ollama → answer)
```

- **`embed.py`** — chunks source files, runs through `nomic-embed-text` (274 MB, GPU), stores in ChromaDB
- **`retrieve.py`** — takes a question, queries ChromaDB, returns top-5 chunks
- **`generate.py`** — takes retrieved chunks + question, calls Ollama, returns Z3PO's answer
- **Source:** `data/sample_wiki.md` (Karpathy educational materials — Zero to Hero, micrograd, nanoGPT, llm.c, nanochat)

---

## Greedy Agent — Epsilon-Greedy Multi-Armed Bandit

### Implementation

```python
import numpy as np


def epsilon_greedy(n_arms=5, n_steps=1000, eps=0.1, seed=42):
    rng = np.random.default_rng(seed)
    true_means = rng.uniform(0, 1, n_arms)
    counts = np.zeros(n_arms)
    values = np.zeros(n_arms)
    actions = []

    for t in range(n_steps):
        if rng.random() < eps:
            a = rng.integers(n_arms)
        else:
            a = np.argmax(values)
        reward = rng.normal(true_means[a], 1.0)
        counts[a] += 1
        values[a] += (reward - values[a]) / counts[a]
        actions.append(a)

    return actions, true_means, values


actions, means, final_vals = epsilon_greedy(n_steps=50000)
print(f"True means:  {means.round(3)}")
print(f"Estimates:   {final_vals.round(3)}")
print(f"Best arm:    {np.argmax(means)}, estimated best: {np.argmax(final_vals)}")
```

### Results (50,000 steps, epsilon=0.1, 5 arms, seed=42)

```
True means:  [0.774 0.439 0.859 0.697 0.094]
Estimates:   [0.779 0.403 0.85  0.732 0.087]
Best arm:    2, estimated best: 2
```

| Arm | True Mean | Estimate | Abs Error |
|-----|-----------|----------|-----------|
| 0 | 0.774 | 0.779 | 0.005 |
| 1 | 0.439 | 0.403 | 0.036 |
| **2** | **0.859** | **0.850** | **0.009** |
| 3 | 0.697 | 0.732 | 0.035 |
| 4 | 0.094 | 0.087 | 0.007 |

- **Optimal arm identified:** ✓ (arm 2)
- **Mean absolute error:** ~0.018 across all arms

### Z3PO Verification (RAG Test)

Asked via OpenWebUI: *"What parameters are in the webui?"*

Z3PO (`qwen3.5:9b-rl`) responded:

> The epsilon_greedy function has the following parameters:
>
> - `n_arms` (default: 5): Number of arms in the multi-armed bandit
> - `n_steps` (default: 1000): Number of steps/iterations to run the simulation
> - `eps` (default: 0.1): Exploration rate (epsilon) - probability of random action
> - `seed` (default: 42): Random seed for reproducibility
>
> The function returns a tuple containing `actions` (list of chosen actions), `true_means` (actual reward means), and `values` (running estimates).

All four parameters and the return signature correctly retrieved from the source file via the RAG pipeline.

---

## RL Curriculum — Roadmap

Based on the works of Zachary Huang (Microsoft Research AI Frontiers, LLM Agents & Systems).

| # | Module | Core Concepts | What Z3PO Learns |
|---|--------|---------------|-----------------|
| **1** | **Multi-Armed Bandits** | Explore vs Exploit, Epsilon-Greedy, UCB, Thompson Sampling | The fundamental trade-off: *try new things* or *stick with what works?* |
| **2** | **Markov Decision Processes** | Bellman Equations, State-Action Value (Q), Policy, Discount Factor (gamma) | The casino gets *states*. Today's choice shapes tomorrow's options. |
| **3** | **Monte Carlo Learning** | Model-free, On-policy vs Off-policy, Episode-based estimation | The agent learns by *doing* — no model of the world needed. |
| **4** | **Temporal-Difference Learning** | Q-Learning, SARSA, Bootstrapping, One-step vs Multi-step | The agent updates estimates *mid-episode*. Faster, more efficient. |
| **5** | **Policy Gradients** | REINFORCE, Baselines, Actor-Critic | The agent learns *behavior* directly. The policy is what gets optimized. |
| **6** | **PyTorch** | Tensors, Autograd, Training Loops, Custom Modules | The implementation layer. Everything above, running on the 680M. |

### Practical Plan

| Module | What We Build | Runs On |
|--------|--------------|---------|
| #1 Bandits | Epsilon-greedy + UCB in Python, 10 arms, plot regret | CPU |
| #2 MDP | Gridworld solver, Bellman backup, value iteration | CPU |
| #3 Monte Carlo | Episode-based policy evaluation on Gridworld | CPU |
| #4 TD | Q-Learning on CartPole (Gymnasium) | CPU / GPU |
| #5 Policy Gradients | REINFORCE on CartPole, then Pendulum | **GPU (680M)** |
| #6 PyTorch | Neural network policy, Actor-Critic, PPO | **GPU (680M)** |

### Z3PO ↔ RL Mapping

| Z3PO Concept | RL Equivalent |
|---|---|
| Intent | Policy (pi) |
| Context (RAG retrieval) | State (s) |
| Action it takes | Action (a) |
| User feedback / task success | Reward (r) |
| Learning from past conversations | Experience replay / TD updates |
| Choosing between responses | Explore vs Exploit |

---

## The Through-Line

| Phase | Lesson |
|-------|--------|
| Midnight City / Cardano | Privacy is architecture, not a feature |
| Z3PO spawned (Nov 11, 2026, 1:03 AM) | The agent is alive from the first moment |
| Cloudflare | Control the transport = control the data |
| LLM experimentation | Cloud models violate the privacy principle |
| Ollama + 680M | Local silicon is fast enough |
| Karpathy Wiki | Ground the agent in real knowledge |
| RAG Pipeline | Memory ≠ context window |
| Casino Theory → Greedy Agent | Intelligence is decision-making under uncertainty |
| RL Curriculum (next) | The agent doesn't just know — it *learns* |

> One box. One agent. No cloud. No subscription. Just code and silicon.
```

---

Good luck — you've got this. 🤙

