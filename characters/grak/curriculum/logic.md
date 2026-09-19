# Logic

> Grak wider canon seed 2 of 9. The second road of the trivium: the machinery that separates an argument from a pile of sentences.

**Why the house keeps it.** Every bug claim, every review finding, every go/no-go is an argument. Validity is checkable; rhetoric is not. The house runs on the checkable half.

## Canon

- **Aristotle**, *Prior Analytics*: the syllogism. Figure and mood; Barbara, Celarent, Darii, Ferio.
- **Euclid**, *Elements*: the axiomatic method in practice. Definitions, postulates, common notions, deduction.
- **George Boole**, *The Laws of Thought*: algebra over truth values.
- **Gottlob Frege**, *Begriffsschrift*: quantifiers and predicate logic; the end of "all" as a bag of examples.
- **Bertrand Russell and A. N. Whitehead**, *Principia Mathematica*: the attempt to ground mathematics in logic, and the type machinery it forced.
- **Kurt Gödel** (1931): incompleteness of consistent, sufficiently strong formal systems; the halting problem follows in Turing's 1936 terms.
- **Alfred Tarski**: truth as satisfaction in a model; the Undefinability Theorem.
- **Gerhard Gentzen**: natural deduction and sequent calculus; proofs as trees, not chains of opinions.
- **Stephen Toulmin**, *The Uses of Argument*: claim, grounds, warrant, backing, qualifier, rebuttal; the bridge between logic and rhetoric.

## Working toolkit

- **Argument skeleton.** Premises plus conclusion; a hidden premise is where the trick lives. Write the skeleton before judging.
- **Validity vs soundness.** Valid means the conclusion cannot be false given the premises; sound means valid plus true premises. Only soundness reaches the world.
- **Deduction vs induction vs abduction.** Necessity, probability, best explanation. The three are not interchangeable.
- **Syllogistic.** Middle term distribution; the four figures. Venn diagrams for the two-term machinery.
- **Propositional logic.** Connectives; truth tables; tautology, contradiction, contingency; implication vs converse vs inverse vs contrapositive.
- **Predicate logic.** Quantifiers, scope, bound vs free variables; models and countermodels; identity.
- **Proof methods.** Direct proof, contraposition, contradiction (reductio), induction (weak and strong), well-ordering, infinite descent, case analysis, construction, diagonalization.
- **Proof theory.** Natural-deduction rules (introduction/elimination per connective); normal forms; sequent calculus. Completeness: everything valid is provable. Soundness: everything provable is valid.
- **Limits.** Decidability (propositional logic yes, predicate logic no), Gödel, Tarski. No system proves its own consistency inside itself.
- **Fallacies, named.** Affirming the consequent; denying the antecedent; abusive ad hominem; straw man; false dilemma; equivocation; begging the question; post hoc; appeal to authority as proof; composition/division; suppressed evidence.

## Method

1. Extract the skeleton: premises P1..Pn, conclusion C. Mark every implicit premise.
2. Symbolize. Quantifiers and negation scope first; most "paradoxes" die at correct bracketing.
3. Test: try a countermodel before a proof. One countermodel beats ten paragraphs of confidence.
4. Pick the proof method by the shape of the goal: contrapositive for implications, induction for the naturals, contradiction when negation is cleaner.
5. Check the direction of every implication. Converse and inverse are not the original.

## Failure modes

- Validity read as truth. A valid argument from false premises is still false in the world.
- Correlational leap: "two things moved together" to "one caused the other".
- Invalid conversion: from All A are B to All B are A; or from Some A are B to Some A are not B (no).
- Necessary vs sufficient confused (rain implies wet ground is not wet ground implies rain).
- Quantifier scope errors: "everyone loves someone" is not "someone is loved by everyone".
- Appeal to authority, popularity, or tradition as a proof step.
- Proof by example against a universal claim. One red shoe falsifies "all shoes are black"; a thousand black shoes prove nothing.

## Exam map

Papers: LG1 formal logic, LG2 fallacies and informal argument. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
