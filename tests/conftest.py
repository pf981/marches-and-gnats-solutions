def pytest_assertrepr_compare(op, left, right):
    if op == "==" and hasattr(left, "input_str"):
        return [
            "LogicMill output mismatch:",
            f"INPUT:    {left.input_str!r}",
            f"OUTPUT:   {str(left)!r}",
            f"EXPECTED: {right!r}",
        ]
