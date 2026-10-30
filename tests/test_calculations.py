"""Independent numerical checks for corrected or easily confused examples."""
import math
import unittest


class CorrectedCalculationTests(unittest.TestCase):
    def test_rain_relative_velocity_2015(self):
        angle = math.radians(29)
        slope = math.radians(40)
        speed = 12 * math.tan(angle) / (math.cos(slope) + math.tan(angle) * math.sin(slope))
        self.assertAlmostEqual(speed, 5.93, delta=0.01)
        self.assertAlmostEqual(
            math.degrees(math.atan2(speed * math.cos(slope), 12 - speed * math.sin(slope))),
            29.0, places=10,
        )

    def test_conical_pendulum(self):
        mass, gravity, speed, length = 2.0, 10.0, 4.0, 2.50
        radial = mass * speed**2 / length
        tension = (radial + math.sqrt(radial**2 + 4 * (mass * gravity)**2)) / 2
        self.assertAlmostEqual(tension, 27.4, delta=0.05)
        self.assertAlmostEqual(tension - (mass * gravity)**2 / tension, radial, places=10)

    def test_incline_friction(self):
        height, speed, gravity, angle = 2.60, 9.0, 10.0, math.radians(30)
        distance = height / math.sin(angle)
        coefficient = (speed**2 / 2 - gravity * height) / (
            gravity * math.cos(angle) * distance
        )
        self.assertAlmostEqual(coefficient, 0.322, delta=0.001)
        self.assertGreater(coefficient, 0)

    def test_bulb_currents_before_and_after_short(self):
        # Currents in units of V/R: bulb 1 in series with (2 || (3+4)),
        # followed by bulb 1 in series with (2 || 3); bulb 4 is shorted.
        before = (3/5, 2/5, 1/5, 1/5)
        after = (2/3, 1/3, 1/3, 0)
        self.assertGreater(after[0]**2, before[0]**2)
        self.assertLess(after[1]**2, before[1]**2)
        self.assertGreater(after[2]**2, before[2]**2)
        self.assertEqual(after[3], 0)

    def test_projectile_position_angle(self):
        launch, position = map(math.radians, (40, 20))
        time = 2 * 30 * math.cos(launch) / 10 * (math.tan(launch) - math.tan(position))
        self.assertAlmostEqual(time, 2.18, delta=0.01)


if __name__ == "__main__":
    unittest.main()
