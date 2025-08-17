import pathlib
import re
from typing import Literal

import typer


def parse_line(line: str, replacements: dict[str, str]) -> list[str]:
    regex = re.compile(r"(\$\{[^}]+\}|\$\S+)")
    parts = regex.split(line)

    def get_rules(i, used):
        if i == len(parts):
            return [""]

        part = parts[i]

        # Literal
        if not part.startswith("$") or part.startswith("$$"):
            return [part + rest for rest in get_rules(i + 1, used)]

        # Template
        template_name = part[2:-1] if part[1] == "{" else part[1:]

        # Template reference number. E.g. $1
        if template_name.isdigit():
            num = int(template_name)
            if len(used) < num:
                raise ValueError(
                    f"Expected at least {num} template names due to template "
                    f"reference number, {part!r}, but only encountered {len(used)}."
                )
            return [used[num - 1] + rest for rest in get_rules(i + 1, used)]

        # Template name. E.g. ${chars}
        if template_name not in replacements:
            raise ValueError(
                f"Template, {template_name!r}, was reference but not defined."
            )

        result = []
        for replacement in replacements[template_name]:
            for rest in get_rules(i + 1, used + (replacement,)):
                result.append(replacement + rest)
        return result

    return get_rules(0, tuple())


def parse(text: str) -> str:
    result = []
    replacements: dict[str, str] = {}

    def add(
        state_in: str,
        ch_in: str | int,
        state_out: str,
        ch_out: str | int,
        direction: str,
    ):
        line = f"{state_in} {ch_in} {state_out} {ch_out} {direction}"
        result.extend(parse_line(line, replacements))

    def move(state: str, ch: str, direction: Literal["R"] | Literal["L"]):
        line = f"{state} {ch}"
        for parsed in parse_line(line, replacements):
            result.append(f"{parsed} {parsed} {direction}")

    for i, line in enumerate(text.splitlines(), 1):
        words = line.split("//", 1)[0].split()

        match words:
            case []:
                pass
            case [lhs, "=", rhs]:
                if lhs in replacements:
                    raise ValueError("{lhs} redefined on line {i}: {line!r}")
                replacements[lhs] = rhs
            case [">", state, ch]:
                move(state, ch, "R")
            case ["<", state, ch]:
                move(state, ch, "L")
            case [state_in, ch_in, state_out, ch_out, direction]:
                add(state_in, ch_in, state_out, ch_out, direction)
            case _:
                raise ValueError("Unable to parse line {i}: {line!r}")

    return "\n".join(result)


def main(input_file: str, output_file: str = "AUTO") -> None:
    input_path = pathlib.Path(input_file)
    text = input_path.read_text(encoding="utf-8")

    code = parse(text)

    if output_file != "AUTO" or input_path.suffix.lower() == ".txt":
        print(code)
        return

    if output_file == "AUTO":
        output_path = input_path.with_suffix(".txt")
    else:
        output_path = pathlib.Path(output_file)

    print("Writing output to {output_path}.")
    output_path.write_text(code, encoding="utf-8")


if __name__ == "__main__":
    typer.run(main)
