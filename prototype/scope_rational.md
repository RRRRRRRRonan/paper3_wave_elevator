# MVS v0.1 Scope Rationale

## Included
- 3 floors
- 5 AMRs
- 1 elevator (capacity=1)
- 20-30 orders per shift
- Deterministic times

## Deliberately Excluded (with reason)
- Multi-elevator → v0.2
- Capacity > 1 → v0.2
- Stochastic times → v0.2
- Dynamic order arrival → Paper 3 scope boundary
- Heterogeneous AMRs → Paper 1 domain
- Charging → Paper 1 domain
- Complex intra-floor routing → abstracted
- Direction switching cost → v0.2 (conservative test at 0 now)
- Rolling horizon → v0.2
- Real data → Month 3 case study
- GUI / animation → never

## Validation Criteria
- [ ] 1000 simulations finish in < 5 minutes
- [ ] I can hand-compute makespan for at least 2 test cases
- [ ] Extreme wave comparison shows >= 2× makespan difference