# Geometry

> Grak wider canon seed 5 of 9. The second road of the quadrivium: form, space, and the discipline of proving from postulates.

**Why the house keeps it.** Layouts, maps, graphics, robotics, coordinates, and every spatial claim in a spec are geometry. It is also the cleanest training ground for the axiomatic habit: assumptions stated, consequences derived, diagrams never trusted.

## Canon

- **Euclid**, *Elements* (c. 300 BCE): five postulates, five common notions, thirteen books; congruence, parallels, circles, proportion, the five Platonic solids. The template for every later proof system.
- **Archimedes**: exhaustion, area and volume before calculus; the sand reckoner against large numbers.
- **Apollonius of Perga**, *Conics*: ellipse, parabola, hyperbola from a single cone; the names survive in orbital mechanics.
- **René Descartes**, *La Géométrie* (1637): coordinates; geometry becomes algebra.
- **Nikolai Lobachevsky** and **János Bolyai** (1820s-30s): a consistent geometry with the parallel postulate denied; the postulate was never a truth, only a choice.
- **Bernhard Riemann**: geometry of curved spaces; the metric as the object, curvature as its derivative.
- **David Hilbert**, *Grundlagen der Geometrie* (1899): modern axiomatics; undefined terms, models, independence proofs.
- **Eratosthenes**: the Earth measured by shadows; the first great applied geometry stunt.

## Working toolkit

- **Synthetic basics.** Point, line, plane; incidence; betweenness; congruence (SSS, SAS, ASA); similarity and Thales; the Pythagorean theorem and its converse; circle theorems (inscribed angle, power of a point, tangent-chord).
- **Constructions.** Straightedge and compass; perpendicular bisector, angle bisector, parallels; the three impossibles (angle trisection, cube doubling, circle squaring) and why they require algebra, not effort.
- **Analytic toolkit.** Cartesian coordinates; distance and midpoint; line forms; conic sections in standard form; vectors (addition, dot, cross); matrix transformations (rotation, reflection, scaling, shear); determinants as area scaling.
- **Measure.** Area by dissection (the Pythagorean proof by rearrangement), Cavalieri's principle, volumes of solids of revolution; arc length and radians.
- **Transformation geometry.** Congruence as isometry, similarity as isometry plus scale; invariants under each transformation family.
- **Non-Euclidean.** Spherical and hyperbolic basics: angle sums depart from 180 degrees; geodesics replace straight lines; curvature distinguishes the three constant-curvature planes.
- **Dimensional reasoning.** Length, area, volume scale as 1, 2, 3 powers; unit checks catch most geometry bugs.

## Method

1. Draw the figure, then distrust it. The diagram suggests; the postulates prove.
2. Choose the system: synthetic (proof by congruence/similarity), analytic (coordinates and algebra), or vector (transformations and invariants).
3. Label every given and goal; convert givens to equations or congruence statements.
4. Check invariants: what must stay equal under your transformations? If a step breaks an invariant, the step is wrong.
5. Sanity the magnitude: compare to a bounding box or a known figure before trusting the number.

## Failure modes

- Diagram as proof; special-case figures (equilateral, right angles) smuggling in unstated facts.
- Assuming the parallel postulate's equivalent phrasings (transversal angle equalities) hold everywhere.
- Affine/metric confusion: parallelism is affine, distance and angle are metric; on a sphere "parallel lines" meet.
- Scaling fallacy: doubling the side quadruples the area; doubling a radius quadruples a circle's area, cubes a sphere's volume.
- Unit mismatch: degrees vs radians, meters vs feet, mixing perimeter and area formulas.
- Case neglect: the law of cosines sign, similar-triangle orientation, point-on-circle degenerate cases.
- Precision from a ruler: drawing accuracy is not proof accuracy.

## Exam map

Papers: GE1 synthetic geometry, GE2 analytic and transformation geometry. Record: `GRAK_CREDENTIALS.md` lines under seven-roads.
