"""Numerically check selected printed answers using data parsed from their questions."""
import math
import re
import unittest

from test_integrity import problem_blocks


class CorrectedCalculationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problems = problem_blocks()

    def value(self, number, pattern):
        statement = self.problems[number].split(r'\begin{enumerate}', 1)[0]
        match = re.search(pattern, statement)
        self.assertIsNotNone(match, f'Problem {number}: missing input for {pattern}')
        return float(match.group(1))

    def check_numeric_answer(self, number, calculated, tolerance):
        block = self.problems[number]
        answer = re.search(r'\\finalanswer\{\(([A-E])\)\s*\$?([0-9.]+)', block)
        self.assertIsNotNone(answer, f'Problem {number}: numeric answer missing')
        options = re.findall(r'\\item\s+([0-9.]+)', block.split(r'\end{enumerate}', 1)[0])
        self.assertEqual(len(options), 5, f'Problem {number}: expected five numeric options')
        printed = float(answer.group(2))
        self.assertEqual(printed, float(options[ord(answer.group(1)) - ord('A')]))
        self.assertAlmostEqual(calculated, printed, delta=tolerance)

    def test_rain_relative_velocity_2015(self):
        rain = self.value(26, r'vertically at ([0-9.]+) m/s')
        slope = math.radians(self.value(26, r'slope at \$([0-9.]+)\^\\circ\$'))
        angle = math.radians(self.value(26, r'moving at \$([0-9.]+)\^\\circ\$'))
        speed = rain * math.tan(angle) / (math.cos(slope) + math.tan(angle) * math.sin(slope))
        self.check_numeric_answer(26, speed, 0.01)
        self.assertAlmostEqual(math.atan2(speed * math.cos(slope), rain - speed * math.sin(slope)), angle)

    def test_conical_pendulum(self):
        mass = self.value(27, r'A ([0-9.]+) kg mass')
        speed = self.value(27, r'speed of ([0-9.]+) m/s')
        length = self.value(27, r'length of ([0-9.]+) m')
        gravity = self.value(27, r'g=([0-9.]+)')
        radial = mass * speed**2 / length
        tension = (radial + math.sqrt(radial**2 + 4 * (mass * gravity)**2)) / 2
        self.check_numeric_answer(27, tension, 0.05)
        self.assertAlmostEqual(tension - (mass * gravity)**2 / tension, radial)

    def test_incline_friction(self):
        speed = self.value(28, r'initial speed of ([0-9.]+) m/s')
        height = self.value(28, r'vertically ([0-9.]+) m')
        gravity = self.value(28, r'g=([0-9.]+)')
        angle = math.radians(self.value(28, r'incline is \$([0-9.]+)\^\\circ\$'))
        distance = height / math.sin(angle)
        coefficient = (speed**2 / 2 - gravity * height) / (gravity * math.cos(angle) * distance)
        self.check_numeric_answer(28, coefficient, 0.001)
        self.assertGreater(coefficient, 0)

    def test_bulb_currents_before_and_after_short(self):
        block = self.problems[9]
        self.assertIn('all four bulbs are identical', block)
        self.assertIn('shorting wire (no resistance)', block)
        before = (3/5, 2/5, 1/5, 1/5)
        after = (2/3, 1/3, 1/3, 0)
        brighter = [i + 1 for i, (old, new) in enumerate(zip(before, after)) if new**2 > old**2]
        self.assertEqual(brighter, [1, 3])
        self.assertIn(r'\finalanswer{(D) Bulbs 1 and 3 only}', block)
        self.assertLess(after[1]**2, before[1]**2)
        self.assertEqual(after[3], 0)

    def test_projectile_position_angle(self):
        launch = math.radians(self.value(39, r'launched at an angle of \$([0-9.]+)\^\\circ\$'))
        position = math.radians(self.value(39, r'position of the projectile makes an angle of \$([0-9.]+)\^\\circ\$'))
        speed = self.value(39, r'speed of ([0-9.]+) m/s')
        gravity = self.value(39, r'g=([0-9.]+)')
        time = 2 * speed * math.cos(launch) / gravity * (math.tan(launch) - math.tan(position))
        self.check_numeric_answer(39, time, 0.01)


if __name__ == '__main__':
    unittest.main()
