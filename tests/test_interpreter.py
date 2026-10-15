import unittest
from contextlib import redirect_stdout
from io import StringIO

from interpreter import Interpreter, RuntimeErrorBanana, run


class TestBananaInterpreter(unittest.TestCase):

    def run_program(self, source):
        captured = StringIO()

        with redirect_stdout(captured):
            output = run(source)

        return output, captured.getvalue().splitlines()

    def test_arithmetic(self):
        source = """
        let x = 10;
        let y = 5;
        print x + y;
        print x * y;
        print x - y;
        """

        output, printed = self.run_program(source)

        self.assertEqual(output, ["15", "50", "5"])
        self.assertEqual(printed, ["15", "50", "5"])

    def test_if_else(self):
        source = """
        let x = 10;
        if x > 5 {
            print 1;
        } else {
            print 0;
        }
        """

        output, _ = self.run_program(source)

        self.assertEqual(output, ["1"])

    def test_while_loop(self):
        source = """
        let x = 1;
        while x <= 5 {
            print x;
            x += 1;
        }
        """

        output, _ = self.run_program(source)

        self.assertEqual(output, ["1", "2", "3", "4", "5"])

    def test_comparisons(self):
        source = """
        let x = 10;
        print x == 10;
        print x != 5;
        print x < 20;
        print x > 5;
        print x <= 10;
        print x >= 10;
        """

        output, _ = self.run_program(source)

        self.assertEqual(
            output,
            ["True", "True", "True", "True", "True", "True"],
        )

    def test_compound_assignment(self):
        source = """
        let x = 10;
        x += 5;
        print x;
        x -= 3;
        print x;
        x *= 2;
        print x;
        x /= 4;
        print x;
        """

        output, _ = self.run_program(source)

        self.assertEqual(output, ["15", "12", "24", "6.0"])

    def test_division_by_zero(self):
        source = """
        let x = 10;
        let y = 0;
        print x / y;
        """

        with self.assertRaisesRegex(RuntimeErrorBanana, "Division by zero"):
            run(source)

    def test_undefined_variable(self):
        with self.assertRaisesRegex(
            RuntimeErrorBanana, "Undefined variable 'x'"
        ):
            run("print x;")


if __name__ == "__main__":
    unittest.main()