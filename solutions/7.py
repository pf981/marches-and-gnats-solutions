def generate_code():
    lines = []
    alphabet = "-abcdefghijklmnopqrstuvwxyzäöõü"

    lines.append("INIT _ SEEK_START X L")
    lines.append("SEEK_START X SEEK_START X L")
    lines.append("SEEK_START ] SEEK_START ] L")
    lines.append("SEEK_START [ SEEK_START [ L")
    lines.append("SEEK_START _ DUPE _ R")
    lines.append("DUPE X HALT _ R")

    # w
    lines.append("DUPE_w _ WRITE_W [ R")
    lines.append("WRITE_W _ WRITE_CLOSE w R")
    lines.append("WRITE_CLOSE _ SEEK_START ] L")

    # ch
    lines.append("DUPE c DUPE_C1 _ R")
    lines.append("DUPE_C1 h DUPE_CH _ R")
    lines.append("DUPE_C1 _ SEEK_START C L")
    for c in alphabet + "X[]":
        lines.append(f"DUPE_CH {c} DUPE_CH {c} R")
        if c != "h":
            lines.append(f"DUPE_C1 {c} DUPE_c {c} R")
    lines.append("DUPE_CH _ WRITE_C [ R")
    lines.append("WRITE_C _ WRITE_h c R")
    lines.append("WRITE_h _ WRITE_CLOSE h R")

    for c in alphabet:
        lines.append(f"INIT {c} INIT {c} R")
        lines.append(f"SEEK_START {c} SEEK_START {c} L")

        if c != "c":
            lines.append(f"DUPE {c} DUPE_{c} _ R")

        for c2 in alphabet + "X[]":
            lines.append(f"DUPE_{c} {c2} DUPE_{c} {c2} R")

        if c != "w":
            lines.append(f"DUPE_{c} _ SEEK_START {c} L")

    return "\n".join(lines)


if __name__ == "__main__":
    code = generate_code()
    with open("solutions/7.txt", "w") as f:
        f.write(code)
