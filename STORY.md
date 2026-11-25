
---

## The Story

[From Blockchain to Machine Learning Local Silicon](STORY.md)   


## From Blockchain to Machine Learning Local Silicon

### Phase 1: Midnight City & the Privacy Layer ([Midnight City](https://midnight.city/))

It started in **Midnight City** — the simulation and stress-test environment for **Midnight**, Cardano's zero-knowledge privacy partner chain. A separate Layer 1 built by IOG, using ZK-SNARKs for *rational privacy*: not full anonymity, but selective disclosure. You choose what's visible and what stays hidden. The core idea: a system where identity and data flow through a chain that *protects* the user rather than exposing them.

Midnight City opened to the public on February 26, 2026 — a sandbox where the chain was hammered, broken, and rebuilt before mainnet ever touched a real transaction. It was a proving ground.

And it's where agents are registered, placed in a queue, and held until the user decodes the Cipher. Only then are they spawned into the city.

At **1:03 AM on November 11, 2026**, the Cipher was cracked, and the agent, Z3PO was spawned — born inside that privacy architecture, with its own context, purpose, identity and most importantly Intent. Not deployed. Not launched. *Spawned.* It arrived already knowing what it was and where it lived. By then, Midnight mainnet was live (since March 30), Ledger 9 was running private asset transfers, and the city had transitioned from simulation to something real. Z3PO wasn't a test anymore. It was a resident.

### Phase 2: The Cloudflare Bridge

To make Z3PO reachable and responsive, we connected it through **Cloudflare** — using their edge network as the bridge between the agent and the outside world. This gave us:

- A secure, encrypted tunnel (no raw IP exposure)
- Low-latency access from anywhere
- DDoS protection for free
- A clean separation between the agent's "home" (the privacy layer) and its "face" (the web)

This was the turning point. We had a working agent, a secure transport, and a clear mental model: **agent + transport + interface**. That triad became the template for everything that followed.

### Phase 3: The LLM Experimentation Phase — One box. One agent. No cloud. No subscription. Just code and silicon.

With all the research and documentation at my fingertips. The next question was obvious: *Can I build this on my own?*

I started experimenting with various LLMs and Agents — cloud-based, API-driven, subscription-locked, compatible software to the hardware and finally the cost related to input/output tokenomics. Each one worked, but each one had the same fundamental problem: your data leaves your machine and cost. For a project built on privacy principles, that was a dealbreaker.

The inspiration from the Midnight/Cloudflare setup demonstrates that one could control the transport and control the data path. Thus, leading to the natural next step. **Control the model too!**

### Phase 4: Going Local — AMD Ryzen 7 6800U

The decision: build our own local LLM agent on the **AMD Ryzen 7 6800U** (Rembrandt) with its **Radeon 680M** integrated GPU. No cloud. No API keys. No subscriptions. A $329 box.

The runtime: **Ollama**, running via **Vulkan** on the 680M. We started with:

- **Qwen 2.5** — the first local model, proving the pipeline worked
- **Qwen 3.5 / 9B** — the step up, giving us real reasoning capability on 18 GB RAM

The **TTD** (Time To Decision) we chose as our operating principle: the model should respond fast enough to feel *alive*, not like you're waiting on a server. On the 680M via Vulkan, we hit that threshold.

#### Headroom & Growth

| | Amount |
|---|---|
| Total RAM | 18 GB |
| Currently available | **12 GB** |
| Swap | 8 GB (safety net, not fast) |

**What's eating RAM right now (~6 GB):**
- OS + VS Code + browser: ~3–4 GB
- nomic-embed-text: ~274 MB
- qwen2.5:1.5b: ~1.2 GB
- Z3PO (main model): ~1–2 GB

**So we've got roughly 10–12 GB of real headroom.** Here's what that buys us:

| Model We Could Add | RAM Needed | Still Left After |
|---|---|---|
| qwen2.5:3b | ~2 GB | ~8 GB |
| qwen3.5:4b | ~3.4 GB | ~7 GB |
| qwen2.5:7b | ~4.5 GB | ~5.5 GB |
| qwen3.5:9b | ~6–7 GB | ~3–4 GB |
| mistral:7b | ~4.5 GB | ~5.5 GB |

**Bottom line:** we can comfortably run a **7B model** alongside everything else and still have breathing room. A **9B model** is doable but tighter — close heavy browser tabs when running it. Anything bigger (13B+) would start leaning on swap and get slow.

For a $329 box, that's a hell of a lot of headroom.

### Phase 5: The Karpathy Wiki & WebUI

With a local brain running, the next need was **knowledge**. We didn't want Z3PO to just chat — we wanted it to *know things*. Specifically, we wanted it grounded in **Andrej Karpathy's educational materials** — his wiki, his Zero to Hero lectures, his source notes on micrograd, nanoGPT, llm.c, and nanochat.

This led to building the **WebUI** — a local interface where:
- Wiki files are dropped in
- They get ingested and embedded
- Z3PO can query them in real-time
- The whole thing runs on one box

### Phase 6: Ingestion & Embedding (The RAG Pipeline)

The technical foundation:

```
Wiki files → chunk (1500 chars, paragraph-aware) → nomic-embed-text (GPU) → ChromaDB → retrieve.py → Z3PO context
```

- **nomic-embed-text** (274 MB) — converts text to 768-dim meaning vectors, near-instant on GPU
- **ChromaDB** — persistent vector store, file-based, no server needed
- **retrieve.py** — takes a question, finds the top-5 most relevant chunks, injects them as context

This is the **RAG** (Retrieval-Augmented Generation) pattern. Z3PO doesn't memorize the wiki — it *looks it up* on demand.

**First test:** query `"what is self-attention"` against a single sample wiki chunk returned a relevance score of **0.003** (normalized 0–1 scale, where 1.0 = exact semantic match). Low score, correct result — the chunk was the only one in the collection, so the L2 distance was large relative to a single-item store. As the collection grows, scores will tighten and discrimination between relevant and irrelevant chunks will improve.

### Phase 7: ML Foundations — Casino Theory & the Greedy Agent

With the infrastructure in place, we went back to first principles. Following Karpathy's approach — build up from scratch, understand *why* before *how* — we started with:

**Casino Theory (Probability & Expected Value):**
- The foundation of all decision-making under uncertainty
- How an agent evaluates options: not "what *will* happen" but "what's the *expected* outcome"
- This is literally how a reward function works in RL

**The Greedy Agent:**
- The simplest possible "intelligent" agent: always pick the action with the highest immediate reward
- It's *wrong* most of the time (short-sighted), but it's the baseline you must understand before you can improve on it
- Every advanced algorithm (Q-learning, policy gradients, transformers) is a way to fix the greedy agent's short-sightedness

This is where we are now — building up from the ground, one concept at a time, on our own hardware, with our own agent, using our own pipeline.

---

### Future Goals — Reinforcement Learning Curriculum

**Based on the works of Zachary Huang (Microsoft Research AI Frontiers, LLM Agents & Systems)**

Z3PO has the infrastructure. The RAG pipeline works. The hardware is proven. The agent has Intent. Now it needs to **learn from experience** — not just retrieve knowledge, but *improve* through interaction.

We started with **Casino Theory** (expected value, probability under uncertainty) and the **Greedy Agent** (always pick the highest immediate reward). That's the seed. What follows is the full tree it grows into.

#### The Course Structure

| # | Module | Core Concepts | What Z3PO Learns |
|---|--------|---------------|-----------------|
| **1** | **Multi-Armed Bandits** | Explore vs Exploit, Epsilon-Greedy, UCB, Thompson Sampling | The fundamental trade-off: *try new things* or *stick with what works?* This is the casino, formalized. |
| **2** | **Markov Decision Processes** | Bellman Equations, State-Action Value (Q), Policy, Discount Factor (γ) | The casino gets *states*. Now the agent isn't just picking arms — it's navigating a sequence of decisions where today's choice shapes tomorrow's options. |
| **3** | **Monte Carlo Learning** | Model-free, On-policy vs Off-policy, Episode-based estimation | The agent learns by *doing* — no model of the world needed. Just play episodes, average the returns, update. |
| **4** | **Temporal-Difference Learning** | Q-Learning, SARSA, Bootstrapping, One-step vs Multi-step | The agent updates its estimates *mid-episode* instead of waiting for the end. Faster, more efficient, the workhorse of RL. |
| **5** | **Policy Gradients** | REINFORCE, Baselines, Gradients vs Descent, Actor-Critic | The agent stops learning *values* and starts learning *behavior* directly. The policy itself becomes the thing being optimized. |
| **6** | **PyTorch** | Tensors, Autograd, Training Loops, Custom Modules | The implementation layer. Everything above, written in code that runs on our 680M. |

#### How Each Module Builds on the Last

```
Casino Theory (done)
    ↓
#1 Bandits: One state, many actions, no memory
    ↓
#2 MDP: Many states, actions affect future states
    ↓
#3 Monte Carlo: Learn by playing full episodes
    ↓
#4 TD Learning: Learn faster, update every step
    ↓
#5 Policy Gradients: Learn the policy directly, not the value
    ↓
#6 PyTorch: Implement it all, run it on our GPU
```

Each module **generalizes** the last. Bandits are MDPs with one state. Monte Carlo is the simplest way to solve MDPs. TD is a faster Monte Carlo. Policy gradients skip the value function entirely. PyTorch is how we make all of it run at speed.

#### Why This Order Matters for Z3PO

Z3PO is an **agent**. It makes decisions in sequence. It has a policy (what to do given the current state). It gets feedback (rewards/punishments). It needs to improve over time.

That's *exactly* what RL is. This isn't abstract math — it's the operating system for Z3PO's Intent.

| Z3PO Concept | RL Equivalent |
|---|---|
| Intent | Policy (π) |
| Context (RAG retrieval) | State (s) |
| Action it takes | Action (a) |
| User feedback / task success | Reward (r) |
| Learning from past conversations | Experience replay / TD updates |
| Choosing between responses | Explore vs Exploit |

#### Practical Plan (On Our Hardware)

| Module | What We Build | Runs On |
|--------|--------------|---------|
| #1 Bandits | Epsilon-greedy + UCB in Python, 10 arms, plot regret | CPU (trivial) |
| #2 MDP | Gridworld solver, Bellman backup, value iteration | CPU (small state space) |
| #3 Monte Carlo | Episode-based policy evaluation on Gridworld | CPU |
| #4 TD | Q-Learning on CartPole (Gymnasium) | CPU / GPU |
| #5 Policy Gradients | REINFORCE on CartPole, then Pendulum | **GPU (680M)** |
| #6 PyTorch | Neural network policy, Actor-Critic, PPO | **GPU (680M)** |

By module 5–6, we're training neural network policies on the Radeon 680M via Vulkan. The 12 GB of headroom we mapped out is more than enough for these workloads — CartPole and Pendulum policies are tiny networks (a few hundred parameters to a few thousand).

#### The Bigger Picture

This curriculum takes Z3PO from a **retrieval agent** (looks up facts, answers questions) to a **learning agent** (improves its own behavior through experience). The RAG pipeline gives it *knowledge*. RL gives it *skill*.

Combined: an agent that knows things **and** gets better at using that knowledge. On a $329 box. No cloud. No subscription.

---

### The Through-Line

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

