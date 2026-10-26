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


    def test_function_parameters_and_return_value(self):
        source = """
        function multiply(a, b) {
            return a * b;
        }
        print(multiply(6, 7));
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["42"])

    def test_function_without_parameters(self):
        source = """
        function getTen() {
            return 10;
        }
        print(getTen());
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["10"])

    def test_local_and_global_scope(self):
        source = """
        let count = 100;
        function show() {
            let count = 5;
            print(count);
        }
        show();
        print(count);
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["5", "100"])

    def test_nested_function_calls(self):
        source = """
        function add(a, b) {
            return a + b;
        }
        function double(n) {
            return n * 2;
        }
        print(double(add(2, 3)));
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["10"])

    def test_for_loop_sum(self):
        source = """
        let total = 0;
        for (let i = 1; i <= 4; i += 1) {
            total += i;
        }
        print(total);
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["10"])

    def test_undefined_function(self):
        with self.assertRaisesRegex(
            RuntimeErrorBanana, "Undefined function 'missing'"
        ):
            run("print missing(1);")

    def test_function_wrong_argument_count(self):
        source = """
        function add(a, b) {
            return a + b;
        }
        print(add(1));
        """
        with self.assertRaisesRegex(
            RuntimeErrorBanana, "expects 2 argument"
        ):
            run(source)

    def test_return_outside_function(self):
        with self.assertRaisesRegex(
            RuntimeErrorBanana, "outside a function"
        ):
            run("return 5;")

    def test_recursive_function(self):
        source = """
        function factorial(n) {
            if n <= 1 {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }
        print(factorial(5));
        """
        output, _ = self.run_program(source)
        self.assertEqual(output, ["120"])


    def test_functions_cannot_access_caller_locals(self):
        source = """
        function inner() {
            print(secret);
        }

        function outer() {
            let secret = 99;
            inner();
        }

        outer();
        """
        with self.assertRaisesRegex(
            RuntimeErrorBanana, "Undefined variable 'secret'"
        ):
            run(source)


if __name__ == "__main__":
    unittest.main()