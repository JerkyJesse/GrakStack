# Astronomy

> Grak wider canon seed 7 of 9. The fourth road of the quadrivium: the sky as the first instrument, the first clock, and the first dataset.

**Why the house keeps it.** Scheduling, timezones, calendars, GPS, eclipse tables, tide charts: the sky is the oldest distributed system, and its mechanics set every clock the machine runs on.

## Canon

- **Ptolemy**, *Almagest* (c. 150 CE): the geocentric model at full power; epicycles as engineering, not stupidity. The best-fit model of its era.
- **Nicolaus Copernicus**, *De revolutionibus* (1543): heliocentric model; simpler in some ways, not obviously more accurate at first.
- **Tycho Brahe**: decades of naked-eye positions accurate to ~1 arcminute; data before theory.
- **Johannes Kepler**, *Astronomia Nova* (1609) and *Harmonices Mundi* (1619): the three laws; ellipses, equal areas, T² ∝ a³. Fit to Tycho's data, not to philosophy.
- **Galileo Galilei**, *Sidereus Nuncius* (1610): moons, phases, mountains; the telescope as instrument.
- **Isaac Newton**, *Principia* (1687): gravitation unifies the fall and the orbit.
- **Henrietta Swan Leavitt** (1912): Cepheid period-luminosity relation; the first standard candle.
- **Albert Einstein** (1915): general relativity; Mercury's precession and light bending follow.
- **IAU**: modern definitions and coordinate conventions (the 2006 planet definition included).

## Working toolkit

- **The celestial sphere.** Horizon coordinates (altitude, azimuth); equatorial coordinates (right ascension, declination); the ecliptic; equinoxes and solstices; the celestial poles. Convert between frames by geometry, not memory.
- **Time.** Sidereal vs solar day (sidereal day ≈ 23h 56m 4s); solar vs sidereal time; Julian dates for continuous counting; timezones and UTC; leap seconds.
- **Seasons and phases.** Seasons come from axial tilt (23.44°), not distance to the Sun; the Moon's phases from illumination geometry; eclipse conditions (nodes) and the saros cycle (~18 years 11 days).
- **Precession.** The equinoxes drift ~26,000 years per cycle; star coordinates are epoch-stamped for a reason.
- **Magnitudes.** Apparent magnitude m; flux ratio: 5 magnitudes = factor 100; m1 − m2 = −2.5 log10(F1/F2). Smaller number, brighter object.
- **Kepler's laws.** (1) Orbits are ellipses with the Sun at a focus; (2) equal areas in equal times; (3) T² ∝ a³ (years² = AU³ for the solar system). Newton derives all three from F = GMm/r².
- **Orbital mechanics.** Orbital elements (a, e, i, Ω, ω, M); vis-viva equation v² = GM(2/r − 1/a); escape velocity √(2GM/r); Hohmann transfers; geostationary altitude ≈ 35,786 km.
- **Scale.** Light-year ≈ 9.46 × 10¹² km; AU ≈ 149.6 million km; parallax (arcseconds) inverts to parsecs; Hubble–Lemaître law v = H₀d.
- **Observation practice.** Field of view, limiting magnitude, airmass, seeing; a plan before the scope.

## Method

1. Fix the frame first: where is the observer, what coordinate system, what epoch. Half of all astronomy errors are frame errors.
2. Reduce to geometry: draw the triangle (observer, object, reference) before any formula.
3. Use Kepler 3 with units handled explicitly: years and AU, or SI throughout, never mixed.
4. Check apparent magnitude arithmetic on a known pair before trusting a pipeline.
5. Ask what is measurable: angular size plus distance gives physical size; alone, neither does.

## Failure modes

- Seasons-by-distance error (it is tilt); also "closer to the Sun in summer."
- Sidereal/solar day confusion; scheduling a star observation by clock time without the 4-minute-per-day drift.
- Orbital circles assumed; real orbits are ellipses, speed varies, and the Sun sits at a focus.
- Magnitude sign confusion: brighter stars have smaller (even negative) magnitudes.
- Mixing arcseconds, arcminutes, and degrees; parallax unit errors off by 3600.
- Ignoring airmass and light pollution when claiming a limiting magnitude.
- Flat-sky thinking: angles on the sphere do not add like plane angles near the poles.
- Confidence in 1:10⁹ impacts from 1:10³ samples; small-number statistics on the sky.

## Exam map

Papers: AS1 the sphere and time, AS2 orbital mechanics. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
