# Grammar

> Grak wider canon seed 1 of 9. The first road of the trivium: how language is built, so every later claim has a parseable shape.

**Why the house keeps it.** Code review, specs, contracts, and error messages are all language under load. A reader who cannot parse a sentence cannot find the load-bearing clause in a requirement. Grammar is the cheapest correctness tool there is: it runs before the compiler and it runs on prose.

## Canon

- **Pāṇini**, *Aṣṭādhyāyī* (c. 4th century BCE): ~4,000 rules, ordered and recursive, describing Sanskrit morphology and phonology. The first generative grammar; rules compose, they do not list.
- **Dionysius Thrax**, *Tékhnē Grammatikē* (c. 100 BCE): the school grammar that fixed the parts of speech for two millennia.
- **Donatus** and **Priscian**, *Institutiones Grammaticae*: the Latin transmission; the vocabulary still used (noun, verb, case, tense).
- **Ferdinand de Saussure**, *Cours de linguistique générale*: sign, signifier, signified; language as a system; synchrony vs diachrony.
- **Leonard Bloomfield**, *Language*: descriptive method; the sentence as the largest free form.
- **Noam Chomsky**, *Syntactic Structures* (1957): constituency, phrase structure, transformation; competence vs performance.
- Reference grammars and **WALS** (World Atlas of Language Structures): typology over anecdote.

## Working toolkit

- **Morphology.** Morpheme; root, stem, affix; inflection (grammatical information: case, number, tense) vs derivation (new lexeme). Agglutinative (Turkish, Finnish: one morpheme per slot) vs fusional (Latin, Russian: one affix, many categories) vs isolating (Mandarin) vs polysynthetic (Inuktitut).
- **Syntax.** Constituency and phrase structure; heads and dependents; agreement (gender, number, person) and government (case assignment); argument structure (subject, object, adjunct).
- **Constituency tests.** Substitution (it/they), movement (fronting, clefting), coordination (and), ellipsis. A claimed constituent must survive at least two independent tests.
- **Alignment and order.** Nominative-accusative (subject of intransitive behaves like transitive subject) vs ergative-absolutive (like transitive object); word-order typology SVO/SOV/VSO and its correlation with adposition order.
- **Tense, aspect, mood, voice.** Tense locates time; aspect shapes it (perfective vs imperfective); mood marks reality (indicative, subjunctive, imperative); voice reorders participants (active, passive, middle).
- **Sandhi and allomorphy.** Sound changes at morpheme boundaries; the reason a clean rule produces an unclean surface.
- **Description before prescription.** Record what speakers do; prescription is a style layer, not a fact layer.

## Method

1. Parse the sentence before arguing about it. Name subject, verb, object, modifiers, and what each pronoun binds to.
2. Run the ambiguity check: if two parses survive, the sentence (or spec) is broken, not the reader. Split it.
3. For morphology, segment to the bone: root first, then each affix and the category it carries.
4. For a new language or notation, find the alignment and order first; assumptions from English are the usual bug.

## Failure modes

- Confusing orthography with grammar. Spaces and spelling are conventions; agreement and case are structure.
- Reading a relative clause onto the wrong noun ("the report on the desk that burned").
- Prescription as description. "Correct" is register, not truth.
- Indo-European bias: forcing case, tense, or word order from English onto languages that encode them elsewhere (topic markers, evidentials, classifiers).
- False cognates and folk etymology as argument.
- Dangling modifiers, unattached pronouns, and scope errors ("every engineer reviewed a design": one design or one per engineer?).

## Exam map

Paper: GR1. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
