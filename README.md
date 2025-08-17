# Marches and Gnats Solutions

Solutions to the [Marches and Gnats](https://mng.quest/) puzzles.

- Language: Python 3.13
- Package manager: [uv](https://github.com/astral-sh/uv)
- Test runner: [pytest](https://pytest.org)

## Setup
Install uv from https://github.com/astral-sh/uv

## Run tests

```bash
uv run pytest
```

## Templates

Some transition rules are more easily expressed using a **template language**. This repository includes a `template.py` script that performs the translation.

### Running the translator

Convert all `.template` files to `.txt` with:
```
uv run template.py solutions/*.template
```

By default, this will write to a file with the same name but with the `.txt` extension (e.g. `solutions/7.txt`). If you want to force output to standard output instead of a file, use the `--stdout` flag:

```bash
uv run template.py solutions/7.template --stdout
```

The program will refuse to overwrite the input file if the output path resolves to the input file.

### Template language

The template language extends the transition rules format with **character classes**, **capture groups**, and **left/right shorthand**.

#### Character classes

You can define sets of characters at the top of a template file:

```
digits  = 0123456789
letters = abcdefghijklmnopqrstuvwxyz
```

These can then be referenced using `$name` or `${name}`. This works anywhere - including in state names.

Example:
```
// Replace all digits with X and letters (abc) with Y
digits = 0123456789
letters = abc

INIT $digits INIT X R
INIT $letters INIT Y R
INIT _ HALT _ R
```

Translates to:
```
INIT 0 INIT X R
INIT 1 INIT X R
INIT 2 INIT X R
INIT 3 INIT X R
INIT 4 INIT X R
INIT 5 INIT X R
INIT 6 INIT X R
INIT 7 INIT X R
INIT 8 INIT X R
INIT 9 INIT X R
INIT a INIT Y R
INIT b INIT Y R
INIT c INIT Y R
INIT _ HALT _ R
```

#### Capture groups

When you use multiple character classes in a rule, they expand into a **cross-product**.  
Capture groups let you refer back to the specific character that was matched instead of expanding again.

Example:
```
// Rotate a string left containing a's, b's, and c's.
chars = abc

COPY $chars APPEND_$1 _ R
APPEND_$chars $chars APPEND_$1 $2 R
APPEND_$chars _ HALT $1 R
```

Translates to:
```
COPY a APPEND_a _ R
COPY b APPEND_b _ R
COPY c APPEND_c _ R
APPEND_a a APPEND_a a R
APPEND_a b APPEND_a b R
APPEND_a c APPEND_a c R
APPEND_b a APPEND_b a R
APPEND_b b APPEND_b b R
APPEND_b c APPEND_b c R
APPEND_c a APPEND_c a R
APPEND_c b APPEND_c b R
APPEND_c c APPEND_c c R
APPEND_a _ HALT a R
APPEND_b _ HALT b R
APPEND_c _ HALT c R
```

#### Left/right shorthand

`> STATE CHARACTER` is shorthand for `STATE CHARACTER STATE CHARACTER R`. Similarly for `< STATE CHARACTER`.

```
digits = 0123456789

> SKIP_NUMS $digits
```

Expands to
```
SKIP_NUMS 0 SKIP_NUMS 0 R
SKIP_NUMS 1 SKIP_NUMS 1 R
SKIP_NUMS 2 SKIP_NUMS 2 R
SKIP_NUMS 3 SKIP_NUMS 3 R
SKIP_NUMS 4 SKIP_NUMS 4 R
SKIP_NUMS 5 SKIP_NUMS 5 R
SKIP_NUMS 6 SKIP_NUMS 6 R
SKIP_NUMS 7 SKIP_NUMS 7 R
SKIP_NUMS 8 SKIP_NUMS 8 R
SKIP_NUMS 9 SKIP_NUMS 9 R
```








## Acknowledgements

Includes `logic_mill.py` from [mng.quest](https://mng.quest/logic_mill.py), licensed under the MIT License.

Template language inspired by [IsaacG](https://github.com/IsaacG/Advent-of-Code/blob/main/mng.quest/solve.py).