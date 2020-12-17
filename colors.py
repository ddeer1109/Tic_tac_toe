def print_board(board):
    """Prints a 3-by-3 board on the screen with borders."""
    color_elem = []
    for row in board:
        for element in row:
            if element == "X":
                color_elem.append(Fore.GREEN + element)
            elif element == "0":
                color_elem.append(Fore.RED + element)
            elif element == ".":
                color_elem.append(Fore.WHITE + element)
    x = [Fore.WHITE + "   1   2   3",
    Fore.WHITE + "A "  + " " + color_elem[0] + Fore.WHITE + " | " + color_elem[1] + Fore.WHITE + " | " + color_elem[2],
    Fore.WHITE + "  ---+---+---",
    Fore.WHITE + "B "  + " " + color_elem[3] + Fore.WHITE + " | " + color_elem[4] + Fore.WHITE + " | " + color_elem[5],
    Fore.WHITE + "  ---+---+---",
    Fore.WHITE + "C "  + " " + color_elem[6] + Fore.WHITE + " | " + color_elem[7] + Fore.WHITE + " | " + color_elem[8]
    ]
    print(x[0])
    print(x[1])
    print(x[2])
    print(x[3])
    print(x[4])
    print(x[5])
    Fore.WHITE
