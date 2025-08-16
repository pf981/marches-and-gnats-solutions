import importlib
import inspect
import pathlib
import pytest
import random
import re
import sys
import typing

import logic_mill


SOLUTIONS_DIR = pathlib.Path("solutions")


def make_runner(code: str) -> typing.Callable[[str], str]:
    try:
        transition_rules = logic_mill.parse_transition_rules(code)
    except Exception as e:
        pytest.fail(f"Failed to parse code: {e}")

    class RunResult(str):
        input_str: str

        def __new__(cls, value: str, input_str: str):
            obj = super().__new__(cls, value)
            obj.input_str = input_str
            return obj

        def __repr__(self):
            return f"<output={super().__repr__()} for input={self.input_str!r}>"

    def run(input: str) -> str:
        try:
            mill = logic_mill.LogicMill(transition_rules)
            result, _ = mill.run(input)
        except Exception as e:
            pytest.fail(f"Failed to run: {e}")
        return RunResult(result.strip("_"), input)

    return run


@pytest.fixture
def r(request: pytest.FixtureRequest) -> typing.Callable[[str], str]:
    """Auto runner fixture - short name for convenience"""
    test_name = request.node.name
    match = re.search(r"test_solution(\d+)", test_name)

    if not match:
        pytest.fail(f"Could not extract solution number from test name: {test_name}")

    solution_number = int(match.group(1))
    solution_file = SOLUTIONS_DIR / f"{solution_number}.txt"

    assert solution_file.exists(), f"Solution file {solution_file} does not exist"

    with open(solution_file, "r") as f:
        code = f.read()

    try:
        run = make_runner(code)
    except Exception as e:
        pytest.fail(f"Failed to build runner from {solution_file}: {e}")

    return run


@pytest.mark.parametrize("solution_file", sorted(SOLUTIONS_DIR.glob("*.py")))
def test_codegen(solution_file):
    """For each solutions/N.py, run its matching test_solutionN(r)."""
    if not solution_file.stem.isdigit():
        pytest.fail(
            f"Solution python module, '{solution_file}', does not have the correct format. Expected '{SOLUTIONS_DIR / '{solution_number}.py'}'"
        )
    solution_number = int(solution_file.stem)

    # Find the corresponding test function in this module
    test_func_name = f"test_solution{solution_number}"
    current_module = sys.modules[__name__]
    test_func = getattr(current_module, test_func_name, None)
    if test_func is None:
        pytest.fail(f"No {test_func_name} defined while processing {solution_file}")

    # Ensure test function takes correct parameters
    sig = inspect.signature(test_func)
    params = list(sig.parameters.keys())
    if params != ["r"]:
        pytest.fail(
            f"Unable to run test for {solution_file} codegen. {test_func_name} test function does have correct parameters. Expected only 'r' parameter by signature was {sig}"
        )

    # Load the solution and build runner
    spec = importlib.util.spec_from_file_location(solution_file.stem, solution_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    code = module.generate_code()
    r = make_runner(code)

    # Run the test
    test_func(r)


def tally(num: int) -> str:
    return "|" * num


def to_bin(num: int) -> str:
    return bin(num)[2:]


def test_solution1(r):
    assert r("|||+||||") == "|||||||"
    for lhs in range(1, 10):
        for rhs in range(1, 10):
            input = f"{tally(lhs)}+{tally(rhs)}"
            assert r(input) == tally(lhs + rhs)


def test_solution2(r):
    assert r("|||||||") == "O"
    assert r("||||||") == "E"
    for num in range(1, 10):
        assert (
            r(tally(num)) == "EO"[num % 2]
        ), f"Expect {num} is {['even', 'odd'][num % 2]}"


def test_solution3(r):
    assert r("1010") == "1011"
    assert r("0") == "1"
    for num in range(1, 10):
        assert r(to_bin(num)) == to_bin(num + 1)


def test_solution4(r):
    assert r("||*|||") == "||||||"
    for lhs in range(1, 10):
        for rhs in range(1, 10):
            assert r(f"{tally(lhs)}*{tally(rhs)}") == tally(lhs * rhs)


def test_solution5(r):
    random.seed(0)
    assert r("||:|||,|||||,||||||||,||||") == "|||||"
    for n in range(1, 10):
        nums = [random.randint(1, 10) for _ in range(n)]
        rhs = ",".join(tally(num) for num in nums)
        for i in range(1, n + 1):
            assert r(f"{tally(i)}:{rhs}") == tally(nums[i - 1])


def test_solution6(r):
    assert r("|||||-||") == "|||"
    assert r("||-||") == ""
    for lhs in range(1, 10):
        for rhs in range(1, lhs):
            assert r(f"{tally(lhs)}-{tally(rhs)}") == tally(lhs - rhs)


def test_solution7(r):
    random.seed(0)
    assert (
        r("wõta-wastu-mu-soow-ja-chillitse-toomemäel")
        == "[w]õta-[w]astu-mu-soo[w]-ja-[ch]illitse-toomemäel"
    )
    for n in range(1, 10):
        lhs = "".join(
            random.choice("-abcdefghijklmnopqrstuvwxyzäöõü") for _ in range(n)
        )
        rhs = "".join({"w": "[w]", "ch": "[ch]"}.get(c, c) for c in lhs)
        assert r(lhs) == rhs


def test_solution8(r):
    random.seed(0)
    assert r("hello-world") == "dlrow-olleh"
    for n in range(1, 10):
        lhs = "".join(
            random.choice("-abcdefghijklmnopqrstuvwxyzäöõü") for _ in range(n)
        )
        rhs = lhs[::-1]
        assert r(lhs) == rhs


def test_solution9(r):
    assert r("|||,||||") == "|||<||||"
    assert r("|||,|||") == "|||=|||"
    for lhs in range(1, 10):
        for rhs in range(1, 10):
            if lhs < rhs:
                op = "<"
            elif lhs > rhs:
                op = ">"
            else:
                op = "="
            assert r(f"{tally(lhs)},{tally(rhs)}") == f"{tally(lhs)}{op}{tally(rhs)}"


def test_solution10(r):
    random.seed(0)
    assert r("hello+world+how-are-you") == "|||"
    for n in range(1, 10):
        words = []

        for _ in range(n):
            word_length = random.randint(1, 10)
            word = "".join(
                random.choice("-abcdefghijklmnopqrstuvwxyzäöõü")
                for _ in range(word_length)
            )
            words.append(word)

        lhs = "+".join(words)
        rhs = tally(n)
        assert r(lhs) == rhs


def test_solution11(r):
    assert r("13") == "14"
    for num in range(1, 1000):
        assert r(str(num)) == str(num + 1)


def test_solution12(r):
    random.seed(0)
    assert r("2+5") == "7"

    for _ in range(1000):
        lhs = random.randint(1, 1000)
        rhs = random.randint(1, 1000)
        assert r(f"{lhs}+{rhs}") == str(lhs + rhs)

        lhs = random.randint(1, 1_000_000_000)
        rhs = random.randint(1, 1_000_000_000)
        assert r(f"{lhs}+{rhs}") == str(lhs + rhs)


def test_solution13(r):
    random.seed(0)
    assert r("||,|,|||||,||||||||") == "|,||,|||||,||||||||"

    for _ in range(100):
        n = random.randint(1, 10)
        nums = random.choices(range(1, 10), k=n)

        input_str = ",".join(tally(num) for num in nums)
        expected_output_str = ",".join(tally(num) for num in sorted(nums))
        assert r(input_str) == expected_output_str
