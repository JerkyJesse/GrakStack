# Arithmetic

> Grak wider canon seed 4 of 9. The first road of the quadrivium: number, the raw material every later measure is built from.

**Why the house keeps it.** Sizing, rates, budgets, offsets, retries, capacity: all arithmetic under pressure. A wrong unit or a wrong base rate kills more systems than a wrong data structure.

## Canon

- **Euclid**, *Elements* Books VII-IX: divisibility, the Euclidean algorithm, primes, the fundamental theorem of arithmetic, perfect numbers.
- **Diophantus**, *Arithmetica*: first systematic treatment of equations in the unknown.
- **Brahmagupta** (628 CE): zero as a number with rules; negative numbers in trade and debt.
- **al-Khwārizmī**: the Hindu-Arabic positional system and algebra; algorithm carries his name.
- **Leonardo of Pisa (Fibonacci)**, *Liber Abaci* (1202): the positional system into Europe.
- **Carl Friedrich Gauss**, *Disquisitiones Arithmeticae* (1801): congruences, quadratic reciprocity, the modular lens.
- **Richard Dedekind** and **Giuseppe Peano**: the construction of the number systems; axioms for the naturals.
- **Georg Cantor**: cardinality; countably infinite vs uncountable; the continuum.

## Working toolkit

- **Number systems by construction.** ℕ (naturals) → ℤ (integers, additive inverses) → ℚ (rationals, field) → ℝ (reals, completeness) → ℂ (algebraic closure). Know which one your problem actually lives in.
- **Positional notation.** Base conversion both ways; binary, octal, hex; fixed vs floating point.
- **Divisibility.** GCD/LCM; Euclidean algorithm; extended Euclidean algorithm (Bézout coefficients); divisibility rules.
- **Primes.** Fundamental theorem of arithmetic (unique factorization); Euclid's infinitude proof; sieve of Eratosthenes; primality testing vs factorization (different difficulty classes).
- **Modular arithmetic.** Congruences; addition/multiplication tables mod n; inverses exist iff gcd = 1; Fermat's little theorem; Euler's theorem; Chinese remainder theorem (CRT); modular exponentiation by squaring.
- **Proof engines.** Induction (base case plus step), strong induction, well-ordering, infinite descent. Most number claims bow to one of these.
- **Relations and rates.** Ratio, proportion, percentage; percentage points vs percent change; compound vs simple growth; the rule of 72; base-rate reasoning.
- **Counting.** Permutations, combinations, binomial theorem; pigeonhole principle; inclusion-exclusion.
- **Magnitude and error.** Orders of magnitude; scientific notation; absolute vs relative error; floating-point representation error; catastrophic cancellation.

## Method

1. Name the domain: integers, reals, or modular. The wrong domain is the most common bug.
2. Check units and bases before computing; convert once, at the end, not at every step.
3. Prefer exact where exact exists (rationals, integers, CRT), float only when measurement demands it.
4. Estimate first: order-of-magnitude bound before the precise call. A result outside the bound is a bug, not a discovery.
5. Prove before trusting: induction or descent for claims about all naturals.

## Failure modes

- Division by zero, and its cousins: dividing by a variable that can be zero.
- Treating floating-point as real arithmetic; 0.1 + 0.2 ≠ 0.3; equality tests on floats.
- Percentage errors: "up 200%" read as "doubled" (it tripled); percent vs percentage points.
- Base-rate neglect: a 99% accurate test on a rare condition mostly returns false positives.
- Assuming patterns from small samples (primes, random sequences); the law of small numbers.
- Off-by-one at boundaries; fencepost counting.
- Assuming all infinities are the same size, or that infinite sets behave like finite ones (Hilbert's hotel).
- Precision theater: reporting ten digits from two-digit inputs.

## Exam map

Paper: NU1. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
