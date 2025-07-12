import logic_mill
import pathlib
import pytest


def get_logic_mill(solution_number):
    solution_file = pathlib.Path(f"solutions/{solution_number}.txt")

    assert solution_file.exists(), f"Solution file {solution_file} does not exist"

    with open(solution_file, "r") as f:
        code = f.read()

    try:
        transition_rules = logic_mill.parse_transition_rules(code)
        mill = logic_mill.LogicMill(transition_rules)
    except Exception as e:
        pytest.fail(f"Failed to parse {solution_file}: {e}")

    return mill


def test_solution1():
    mill = get_logic_mill(1)
    result, steps = mill.run("|||+||||", verbose=True)
    assert result == "|||||||"
