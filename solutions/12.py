def generate_code():
    lines = []

    def a(s):
        lines.append(s)

    # Place X left of LHS
    a("BOOKEND_LEFT _ SEEK_LHS_END_RIGHT X R")

    for num in range(10):
        a(f"INIT {num} BOOKEND_LEFT {num} L")

        a(f"SEEK_LHS_END_RIGHT {num} SEEK_LHS_END_RIGHT {num} R")

    a("SEEK_LHS_END_RIGHT + POP_LHS_0 + L")

    for carry in [0, 1]:
        for num in range(10):
            a(f"POP_LHS_{carry} {num} SEEK_+_RIGHT_{num + carry} _ R")
        a(f"POP_LHS_{carry} _ POP_LHS_{carry} _ L")

    for carry in range(11):
        a(f"SEEK_+_RIGHT_{carry} _ SEEK_+_RIGHT_{carry} _ R")
        a(f"SEEK_+_RIGHT_{carry} + SEEK_RIGHT_END_{carry} + R")
        for num in range(10):
            a(f"SEEK_RIGHT_END_{carry} {num} SEEK_RIGHT_END_{carry} {num} R")

        # Reached the end of RHS. Place down the number, left, pop RHS, right, add RHS
        # Note that remaining carry is 0 or 10
        a(f"SEEK_RIGHT_END_{carry} _ POP_RHS_{carry - (carry % 10)} {carry % 10} L")

        # If you encounter a number instead of +, that means you deleted the +. Ie RHS is finished
        # Just go left and place the carry
        for num in range(10):
            a(
                f"SEEK_+_RIGHT_{carry} {num} SEEK_RIGHT_END_{carry} {num} L"
            )  # FIXME: Review if the state you move to is correct

    # Pop RHS
    for num in range(10):
        for carry in [0, 10]:  # Carry is 0 or 10
            a(f"POP_RHS_{carry} {num} ADD_{num + carry} _ R")

    # Add to right value
    for carry in range(20):  # Can be carrying up to 19
        for num2 in range(10):
            a(
                f"ADD_{carry} {num2} SEEK_+_LEFT_{(carry + num2) // 10} {(carry + num2) % 10} L"
            )

    # If RHS is + during pop, that means RHS is finished. Still need to shift across LHS and carry
    # Replace it with an _
    for carry in [0, 10]:
        a(f"POP_RHS_{carry} + POP_LHS_{carry // 10} _ L")

        # If RHS is _ during pop, that means you already deleted the +
        a(f"POP_RHS_{carry} _ POP_LHS_{carry // 10} _ L")

    # Note carry is 0 or 1
    for carry in [0, 1]:
        for num in range(10):
            a(f"SEEK_+_LEFT_{carry} {num} SEEK_+_LEFT_{carry} {num} L")
        a(f"SEEK_+_LEFT_{carry} _ SEEK_+_LEFT_{carry} _ L")

    for carry in [0, 1]:
        a(f"SEEK_+_LEFT_{carry} + POP_LHS_{carry} + L")
        # Popping LHS defined higher above

    # If you reach X, seek right
    #  - If you don't hit a +, then prepend
    #  - If you do hit a plus, the RHS carry will be applied to the right number in RHS
    #    and the RHSwill need to be shifted right one. Also, erase the +
    for carry in [0, 1]:
        a(f"POP_LHS_{carry} X FINAL_{carry} _ R")
        a(f"FINAL_{carry} _ FINAL_{carry} _ R")

        # Erase the + and shift RHS right one
        a(f"FINAL_{carry} + SHUFFLE_RHS_{carry} _ R")

    # _ means there is no RHS, so just place carry
    a("SHUFFLE_RHS_0 _ HALT _ R")
    a("SHUFFLE_RHS_1 _ HALT 1 R")

    # Shift RHS to close the gap. Note that you start at the left side of RHS
    for carry in [0, 1]:
        for num in range(10):
            a(f"SHUFFLE_RHS_{carry} {num} FIND_GAP_{carry} {num} R")
            a(f"FIND_GAP_{carry} {num} FIND_GAP_{carry} {num} R")
        a(f"FIND_GAP_{carry} _ APPLY_CARRY_AND_CLOSE_GAP_{carry} _ L")

        for num in range(10):
            a(f"APPLY_CARRY_AND_CLOSE_GAP_{carry} {num} PLONK_{carry + num} _ R")
    for carry in range(11):
        a(f"PLONK_{carry} _ PRE_APPLY_CARRY_AND_CLOSE_GAP_{carry // 10} {carry % 10} L")

    for carry in [0, 1]:
        a(
            f"PRE_APPLY_CARRY_AND_CLOSE_GAP_{carry} _ APPLY_CARRY_AND_CLOSE_GAP_{carry} _ L"
        )

    a("APPLY_CARRY_AND_CLOSE_GAP_0 _ HALT _ L")
    a("APPLY_CARRY_AND_CLOSE_GAP_1 _ PLACE_1_AND_HALT _ R")

    # If you hit a number then prepend. No need to prepend anything if no carry
    for num in range(10):
        a(f"FINAL_0 {num} HALT {num} R")

    for num in range(9):
        a(f"FINAL_1 {num} PLACE_1_AND_HALT {num} L")
    a("PLACE_1_AND_HALT _ HALT 1 L")

    return "\n".join(lines)


if __name__ == "__main__":
    code = generate_code()
    with open("solutions/12.txt", "w", encoding="utf-8") as f:
        f.write(code)
