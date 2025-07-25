import logic_mill
import pathlib
import pytest
import random
import re
import typing


def get_transition_rules(solution_number: int) -> list[logic_mill.TransitionType]:
    solution_file = pathlib.Path(f"solutions/{solution_number}.txt")

    assert solution_file.exists(), f"Solution file {solution_file} does not exist"

    with open(solution_file, "r") as f:
        code = f.read()

    try:
        transition_rules = logic_mill.parse_transition_rules(code)
    except Exception as e:
        pytest.fail(f"Failed to parse {solution_file}: {e}")

    return transition_rules


@pytest.fixture
def r(request: pytest.FixtureRequest) -> typing.Callable[[str], str]:
    """Auto runner fixture - short name for convenience"""
    test_name = request.node.name
    match = re.search(r"test_solution(\d+)", test_name)

    if not match:
        pytest.fail(f"Could not extract solution number from test name: {test_name}")

    solution_number = int(match.group(1))
    transition_rules = get_transition_rules(solution_number)

    def run(input: str) -> str:
        try:
            mill = logic_mill.LogicMill(transition_rules)
            result, _ = mill.run(input)
        except Exception as e:
            pytest.fail(f"Failed to run: {e}")
        return result.strip("_")

    return run


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
