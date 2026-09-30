# FedMed Privacy Guarantees

## Formal Definition

A randomized mechanism M satisfies (ε, δ)-differential privacy if for all
adjacent datasets D, D' (differing in one record) and all output sets S:

    Pr[M(D) ∈ S] ≤ exp(ε) · Pr[M(D') ∈ S] + δ

## Our Guarantee

- **ε = 2.79** after 10 federated training rounds
- **δ = 1e-5** (probability of privacy failure)
- Accountant: Rényi DP (Opacus RDPAccountant)
- Privacy amplification by subsampling (Poisson)

## Interpretation

An adversary observing the final model weights cannot determine whether any
single patient's MRI was included in training with probability greater than
exp(2.79) ≈ 16.3 (bounded advantage).

## References

- Abadi et al. (2016), "Deep Learning with Differential Privacy"
- Mironov (2017), "Rényi Differential Privacy of the Gaussian Mechanism"
- Opacus: https://opacus.ai/
