# Rhetoric

> Grak wider canon seed 3 of 9. The third road of the trivium: getting a true claim into another head without corrupting it on the way.

**Why the house keeps it.** Code that ships is code that convinced someone: a reviewer, a maintainer, a future reader of the diff. Rhetoric is not decoration; it is the transport layer of argument. The house demands both: valid reasoning, delivered clean.

## Canon

- **Aristotle**, *Rhetoric*: the three appeals (ethos, pathos, logos) and the three genres: deliberative (future, expedient), judicial (past, just), epideictic (present, honorable).
- **Cicero**, *De Oratore* and *Brutus*: the five canons and the ideal orator as the good person speaking well.
- **Quintilian**, *Institutio Oratoria*: education of the orator; rhetoric as the full curriculum, not a trick set.
- **Petrus Ramus**: rhetoric reduced to style and delivery; the split that made "rhetoric" mean ornament for centuries.
- **Chaïm Perelman and Lucie Olbrechts-Tyteca**, *The New Rhetoric*: argumentation in the realm of the plausible; the audience as the measure.
- **Kenneth Burke**: identification; rhetoric as symbolic action.
- **Stephen Toulmin**, *The Uses of Argument*: the six-part argument layout that survives in engineering communication.

## Working toolkit

- **The appeals.** Ethos: credibility, earned by track record and shown by admitting limits. Pathos: the audience's stake; never a substitute for the argument. Logos: the argument itself. A claim carried by only one appeal is fragile.
- **The five canons.** Invention (find the argument; topics and stasis), arrangement (order), style (word choice and figures), memory (internalized structure), delivery (the actual act).
- **Arrangement.** Exordium (hook and frame), narratio (facts), confirmatio (proof), refutatio (prebuttal), peroratio (close). In engineering terms: context, change, evidence, risks, ask.
- **Stasis theory.** What is at issue: fact (did it happen), definition (what is it), quality (how serious), procedure (what should be done). Answer the lowest open stasis first.
- **Topoi.** Commonplaces as search prompts: cause/effect, more/less, analogy, definition, testimony, precedent.
- **Figures, named.** Metaphor, metonymy, synecdoche, irony; anaphora, chiasmus, antithesis, asyndeton, tricolon. A figure that hides the claim is sabotage.
- **The Toulmin layout.** Claim, grounds, warrant, backing, qualifier (usually/possibly), rebuttal. Write it out when an argument feels slippery.
- **Kairos and audience.** The right argument at the right moment to the right reader. A correct answer at the wrong time is a loss.

## Method

1. Write the claim as one sentence with the qualifier attached ("X is safe for Y under Z").
2. Name the audience and what they already believe; the gap between belief and claim is the actual work.
3. Choose the arrangement: for a diff, evidence first and conclusion last; for an incident, impact first.
4. Anti-fluff pass: delete every sentence that does not advance the claim. The house voice already does this; rhetoric is why it works.
5. Prebuttal: state the strongest counterargument in its own best form, then answer it or concede it.

## Failure modes

- Style without substance: strong verbs carrying an empty claim.
- Ad hominem, tone policing, and motive-guessing as argument.
- False dilemma: two options presented where five exist.
- Cherry-picked evidence; the missing base rate.
- Motte-and-bailey: defend the modest claim, then re-assert the bold one.
- Weasel hedges ("some say", "many believe") with no source.
- Confusing persuasion with proof. A standing ovation is not a soundness proof.
- Winning the room, losing the reader: sarcasm and in-group shorthand in a written artifact that outlives the room.

## Exam map

Paper: RH1. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
