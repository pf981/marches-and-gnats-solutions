import logic_mill
import pathlib
import pytest
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


def to_s(num: int) -> str:
    return "|" * num


def test_solution1(r):
    assert r("|||+||||") == "|||||||"
    for lhs in range(1, 10):
        for rhs in range(1, 10):
            input = f"{to_s(lhs)}+{to_s(rhs)}"
            assert r(input) == to_s(lhs + rhs)


def test_solution2(r):
    assert r("|||||||") == "O"
    assert r("||||||") == "E"
    for num in range(1, 10):
        assert r(to_s(num)) == "EO"[num % 2], (
            f"Expect {num} is {['even', 'odd'][num % 2]}"
        )
