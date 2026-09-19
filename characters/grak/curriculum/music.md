# Music

> Grak wider canon seed 6 of 9. The third road of the quadrivium: number made audible. Harmony is arithmetic you can hear.

**Why the house keeps it.** Audio, motion, timing curves, UI easing, latency budgets: all are perceived rhythm and pitch. Music theory is the measured psychology of those quantities, written down for a thousand years before anyone called it HCI.

## Canon

- **Pythagoras** (attributed): consonant ratios 2:1 (octave), 3:2 (fifth), 4:3 (fourth). Length ratios on a monochord, ears as the verifier.
- **Boethius**, *De institutione musica* (c. 500 CE): music as mathematics; the quadrivium placement that survives.
- **Guido d'Arezzo** (11th century): staff notation, solmization; the tool that made polyphony transmissible.
- **Gioseffo Zarlino**, *Le istitutioni harmoniche* (1558): just intonation, the senario, triadic harmony begins.
- **Jean-Philippe Rameau**, *Traité de l'harmonie* (1722): harmony from the fundamental; chords as stacked thirds.
- **Johann Joseph Fux**, *Gradus ad Parnassum* (1725): species counterpoint; the pedagogy that trained Mozart and still trains composers.
- **Hermann von Helmholtz**, *On the Sensations of Tone* (1863): acoustics meets physiology; consonance explained by partials.
- **Heinrich Schenker**: hierarchical structure analysis; the idea that a piece is a long-range elaboration of a simple frame.

## Working toolkit

- **Pitch and frequency.** Hz; octave = frequency doubling; pitch class vs pitch (C4 and C5 share class, not height); A4 = 440 Hz standard.
- **Intervals and ratios.** Unison 1:1, octave 2:1, perfect fifth 3:2, perfect fourth 4:3, major third 5:4, minor third 6:5; semitone; cents (1200 per octave; 1 cent = 2^(1/1200)).
- **Tuning systems.** Pythagorean (pure fifths, wide thirds); just intonation (pure thirds, comma trouble); the commas (Pythagorean ≈ 23.46 cents, syntonic 81:80 ≈ 21.51 cents); equal temperament (each semitone 2^(1/12) ≈ 100 cents); the trade: pure intervals in one key vs usable all keys.
- **Scales and modes.** Major and natural/harmonic/melodic minor; church modes (Dorian through Locrian); pentatonic; key signatures and the circle of fifths.
- **Harmony.** Triads (major, minor, diminished, augmented) and seventh chords; Roman numeral analysis; inversions and figured bass; functional harmony (tonic, subdominant, dominant); cadences (authentic, plagal, half, deceptive).
- **Voice leading and counterpoint.** Species one through five against a cantus firmus; rules: no parallel fifths or octaves, resolve tendencies (leading tone up, seventh down), prefer stepwise motion; counterpoint as voice-leading quality control.
- **Rhythm and meter.** Beat, tempo (BPM), simple vs compound meter, duple/triple groupings, syncopation, polyrhythm.
- **Form.** Motive, phrase, period; binary (AB), ternary (ABA), rondo, sonata form (exposition, development, recapitulation).
- **Timbre.** Harmonic series; overtones define instrument color; envelope (attack, decay, sustain, release).

## Method

1. Convert to numbers when comparing: cents for intervals, Hz for pitch, BPM for time. Ears decide, numbers explain.
2. Spell chords by stacking thirds from the root; check the key before naming the chord.
3. Voice-lead on paper: resolve tendency tones, then check for parallels and leaps.
4. For tuning problems, name the comma first; every historical temperament is a decision about which interval to compromise.
5. For rhythm, count the smallest unit; syncopation is defined against a steady grid, so establish the grid.

## Failure modes

- Confusing pitch class with pitch; transposing an octave and calling it the same note in a register-sensitive context.
- Treating equal-tempered thirds and fifths as acoustically pure; they are approximately 14 and 2 cents off.
- Parallel fifths and octaves in strict counterpoint; hidden (direct) fifths at cadences.
- Misreading meter: 6/8 is compound duple, not triple time.
- Notating a transposing instrument at concert pitch.
- Assuming louder means higher, or that octave equivalence extends to timbre.
- Mode mixture error: borrowing chords without naming the borrowed key.

## Exam map

Paper: MU1. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
