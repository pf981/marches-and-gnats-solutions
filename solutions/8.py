def generate_code():
    lines = []
    alphabet = "-abcdefghijklmnopqrstuvwxyzäöõü"

    # hello-world
    # Yhello-world
    # Yhello-worldY
    # Yhello-worlYd
    # Yhello-wor_Ydl
    # ...
    # Y__________Ydlrow-olleh
    # ___________Ydlrow-olleh
    # ____________dlrow-olleh
    lines.append("BOOKEND_LEFT _ BOOKEND_RIGHT Y R")
    lines.append("BOOKEND_RIGHT _ POP Y L")
    lines.append("SEEK_Y Y POP Y L")
    lines.append("POP _ POP _ L")
    lines.append("POP Y REMOVE_LAST_Y _ R")
    lines.append("REMOVE_LAST_Y _ REMOVE_LAST_Y _ R")
    lines.append("REMOVE_LAST_Y Y HALT _ R")

    for c in alphabet:
        lines.append(f"INIT {c} BOOKEND_LEFT {c} L")
        lines.append(f"BOOKEND_RIGHT {c} BOOKEND_RIGHT {c} R")

        lines.append(f"POP {c} APPEND_{c}1 _ R")
        lines.append(f"APPEND_{c}1 _ APPEND_{c}1 _ R")
        lines.append(f"APPEND_{c}1 Y APPEND_{c}2 Y R")
        for c2 in alphabet:
            lines.append(f"APPEND_{c}1 {c2} APPEND_{c}1 {c2} R")
            lines.append(f"APPEND_{c}2 {c2} APPEND_{c}2 {c2} R")
        lines.append(f"APPEND_{c}2 _ SEEK_Y {c} L")

        lines.append(f"SEEK_Y {c} SEEK_Y {c} L")

    return "\n".join(lines)


if __name__ == "__main__":
    code = generate_code()
    with open("solutions/8.txt", "w") as f:
        f.write(code)
