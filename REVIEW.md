# Editorial and accuracy review

Review of the reorganized edition, 2026-10-30. The baseline is Git commit
bd56eec91492894cd103475f2dcb63368ea1c4ee; the original sources and PDFs
remain available in its history.

The review covered the statements, worked solutions, units, assumptions, and
topic placement of all **71 guide examples** and **39 selected problems**.
The selected answers were also compared with the official AAPT answer keys.
The checks are documented below and in the regression tests; they are not a
substitute for an independent subject-matter review.

## Study guide examples

Example numbers restart in each unit. The ranges below cover every example;
the source is in guides/physics/units/.

| Unit | Examples reviewed | Notable edits or checks |
| --- | --- | --- |
| 1. Kinematics | 1–10 | Clarified the force angle, the limiting vertical-circle and river-crossing cases; example 10 now includes the zero and delayed solutions of the differential equation. |
| 2. Newtonian dynamics | 1–8 | Added force definitions and corrected the spring-force sign explanation. |
| 3. Work, energy, power | 1–6 | Fixed the printed conservative-force formula and clarified work and system boundaries. |
| 4. Momentum and collisions | 1–8 | Specified negligible external impulse and corrected the rocket vector sign. |
| 5. Rotational motion | 1–8 | Added the missing no-slip condition, specified the conditions for friction doing no work, and replaced an underdetermined friction example with a specified incline case. |
| 6. Oscillations and waves | 1–5 | Checked period, standing-wave, Doppler and initial-condition examples. |
| 7. Fluids and thermodynamics | 1–7 | Clarified support forces, Bernoulli's assumptions, external pressure in work, and entropy for an isolated system. |
| 8. Electrostatics | 1–4 | Distinguished signed radial field from field magnitude for negative charge. |
| 9. DC circuits | 1–4 | Removed the repeated charging example; stated initial conditions and added a discharge example. |
| 10. Magnetism and induction | 1–5 | Used charge magnitude for radius and period; specified loop geometry and emf magnitude; corrected wave-speed and radiation-source notes. |
| 11. Optics | 1–4 | Checked refraction, critical angle, lens signs and interference. |
| 12. Modern physics | 1–2 | Added the photoelectric threshold condition. |

## Selected problems

data/problem-sources.json records each source paper, original question number,
PDF page, official answer, and official solutions URL. The printed problem set
links directly to the source paper, and the automated integrity test compares
every selected answer to the recorded official key.

Corrections that required more than a formatting change:

- **9:** The short bypasses bulb 4. Bulb 2 dims rather than going out; the
  corrected branch currents still give the official answer, bulbs 1 and 3.
- **12:** The capacitance is 5.0 F as shown in the source figure; its value is
  not needed for the voltage calculation at the specified current.
- **22, 23, 28, 29, 36:** Reconnected the appropriate original figures to the
  questions. The repository's previous image filenames did not match question
  numbers.
- **23:** The three equal force magnitudes imply an incline angle of 60 degrees;
  the original explanation did not state this constraint.
- **26:** Restored the original 2015 scenario: vertical rain, a descending car,
  and a 29-degree apparent angle. Correct relative-velocity calculation gives
  5.93 m/s.
- **27:** Replaced an unrelated incline image with a new conical-pendulum
  diagram and corrected the numerical substitution.
- **28:** Corrected the sign in the work–energy balance.
- **30, 33, 39:** Made the original exam's g = 10 m/s² convention explicit;
  problem 39's substitution now retains the required cosine factor.
- **38–39:** Moved the answers into the same answer-box format used elsewhere.

All remaining selected problems were read against their statements and
solutions; their listed answer letters match the official keys. A source may
have appeared in more than one exam; the reference records one verified
occurrence.

## Outstanding items

- The question statements and several figures originate with AAPT. The
  repository documents their provenance but does not claim ownership or grant
  a license for AAPT material.
- This review does not establish real-world learning outcomes, readership or
  endorsement. Collect feedback and report only results that can be verified.
- Recheck altered examples, source references and page links after future
  edits. PDF links to a companion file require both PDFs to remain together.
