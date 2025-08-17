def generate_code():
    lines = []
    alphabet = "-abcdefghijklmnopqrstuvwxyzäöõü"

    lines.append("PROCESS_RIGHT + SEEK_LEFT _ L")
    lines.append("SEEK_LEFT _ SEEK_LEFT _ L")
    lines.append("SEEK_LEFT | APPEND | R")
    lines.append("APPEND _ SEEK_RIGHT | R")
    lines.append("SEEK_RIGHT _ SEEK_RIGHT _ R")
    lines.append("PROCESS_RIGHT _ HALT _ R")

    for c in alphabet:
        lines.append(f"INIT {c} PROCESS_RIGHT | R")
        lines.append(f"PROCESS_RIGHT {c} PROCESS_RIGHT _ R")
        lines.append(f"SEEK_RIGHT {c} PROCESS_RIGHT _ R")

    return "\n".join(lines)


if __name__ == "__main__":
    code = generate_code()
    with open("solutions/10.txt", "w", encoding="utf-8") as f:
        f.write(code)
