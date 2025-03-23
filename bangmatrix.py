"""
bangmatrix.py
A "minefield" map creator and analyzer by Dan Rhea (c) 2020
Creates a map of 10 to 24 rows by 40 to 80 colums that is
salted with mines. This map can then be fed to a
ML process to solve. I abandoned the ML idea for now and
just show the minefield we create.
"""
from random import randint
from colorama import Fore


def look_around(bangbox: list[list[int]], rows: int, cols: int) -> None:
    """
    look_around()
    Scan the field for mines and set ajacent counts
    """
    row = col = 0
    for row in range(rows):
        for col in range(cols):
            # If we aren't a mine, look around us to see how many mines are next to us.
            # Just make sure we don't look past the map edges
            if bangbox[row][col] >= 0:
                mines = 0
                # North
                if row - 1 >= 0:
                    if bangbox[row-1][col] == -1:
                        mines += 1
                # Northeast
                if row - 1 >= 0 and col + 1 <= cols-1:
                    if bangbox[row-1][col+1] == -1:
                        mines += 1
                # East
                if col + 1 <= cols-1:
                    if bangbox[row][col+1] == -1:
                        mines += 1
                # SouthEast
                if row + 1 <= rows-1 and col + 1 <= cols-1:
                    if bangbox[row+1][col+1] == -1:
                        mines += 1
                # South
                if row + 1 <= rows-1:
                    if bangbox[row+1][col] == -1:
                        mines += 1
                # Southwest
                if row + 1 <= rows-1 and col - 1 >= 0:
                    if bangbox[row+1][col-1] == -1:
                        mines += 1
                # West
                if col - 1 >= 0:
                    if bangbox[row][col-1] == -1:
                        mines += 1
                # Northwest
                if row - 1 >= 0 and col - 1 >= 0:
                    if bangbox[row-1][col-1] == -1:
                        mines += 1
                bangbox[row][col] = mines


def get_rows(num: list[int], node: int) -> str:
    """
    Build a row of the minefield and collect minefield stats
    """
    orow_: str = ""
    match node:
        case -1:
            orow_ += f"{Fore.WHITE}* {Fore.WHITE}"
        case 0:
            orow_ += "  "
            num[0] += 1
        case 1:
            orow_ += f"{Fore.LIGHTBLUE_EX}{str(node)} {Fore.WHITE}"
            num[1] += 1
        case 2:
            orow_ += f"{Fore.LIGHTGREEN_EX}{str(node)} {Fore.WHITE}"
            num[2] += 1
        case 3:
            orow_ += f"{Fore.LIGHTRED_EX}{str(node)} {Fore.WHITE}"
            num[3] += 1
        case 4:
            orow_ += f"{Fore.LIGHTYELLOW_EX}{str(node)} {Fore.WHITE}"
            num[4] += 1
        case 5:
            orow_ += f"{Fore.LIGHTCYAN_EX}{str(node)} {Fore.WHITE}"
            num[5] += 1
        case 6:
            orow_ += f"{Fore.LIGHTMAGENTA_EX}{str(node)} {Fore.WHITE}"
            num[6] += 1
        case 7:
            orow_ += f"{Fore.GREEN}{str(node)} {Fore.WHITE}"
            num[7] += 1
        case 8:
            orow_ += f"{Fore.RED}{str(node)} {Fore.WHITE}"
            num[8] += 1
    return orow_


def get_mines(node_: int) -> int:
    """
    Collect current mine info
    node: int - The contents of a single cell in the field to check for a mine
    """
    realmine_: int = 0
    if node_ == -1:
        realmine_ += 1
    return realmine_


def scatter_mines(mine: int, rows: int, cols: int, bangbox: list[list[int]]):
    """
    Spread the mines around the field.
    mine: int                - The number of mines to scatter
    rows: int                - The depth of field
    cols: int                - The width of the field
    bangbox: list[list[int]] - the field where we will scatter mines
    """
    set_mine: int = 0
    while set_mine < mine:
        row_i: int = randint(0, rows-1)
        col_i: int = randint(0, cols-1)
        if bangbox[row_i][col_i] == 0:
            bangbox[row_i][col_i] = -1
            set_mine += 1
    return set_mine


def prompt():
    """ 
    Display prompt and return string entered
    """
    s_got: str = ""
    s_got = input(f"{Fore.YELLOW}Enter 'q' to quit or enter to repeat: {Fore.WHITE}")
    return s_got


def field() -> None:
    """
    Determine the map dimensions and set the count of mines we will scatter over it to
    15.21 % of (rows*cols). Since I have the numbers here, caclulate the percentage of
    mine coverage we will be working with to double check the coverage.
    """

    rows: int = randint(6,34)
    cols: int = randint(10,62)
    cper: float = 15.21
    # mine count should be ~15.21% of rows*cols (or very close to it)
    mine: int = int(round(((rows*cols) / (100/cper)), 0))
    perc: float = ((mine / (rows*cols)) * 100)

    # Create the empty field
    bangbox: list[list[int]] = [[0 for col in range(cols)] for row in range(rows)]

    # Scatter mines in the field
    scatter_mines(mine, rows, cols, bangbox)

    # Scan the field for mines and set ajacent mine counts
    look_around(bangbox, rows, cols)

    # Output the minefield to the screen
    print(f"{Fore.GREEN}Revealed map:{Fore.WHITE}")

    # Build and output the column header
    first_digit: str = f"     {Fore.YELLOW}"
    second_digit: str = f"     {Fore.YELLOW}"
    for col in range(cols):
        scol: str = str(col)
        if col < 10:
            scol = f"0{scol}"
        first_digit += f"{scol[0:1]} "
        second_digit += f"{scol[1:2]} "
    print(f"{first_digit}  ")
    print(f"{second_digit}  ")

    # build the top border
    orow: str = f"   {Fore.GREEN}╔{"══"*(col+1)}═╗ "
    print(orow)

    # And now build the rows (and get stats)
    realmine: int = 0
    num: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for row in range(rows):
        # column header
        srow: str = str(row)
        if len(srow) == 1:
            srow = f"0{srow}"
        orow = f"{Fore.YELLOW}{srow}{Fore.GREEN} ║ "
        # then the mines. BangBox: -1 mine, 0 open, 1-8 open next to a mine
        for col in range(cols):
            node: int = bangbox[row][col]
            orow += get_rows(num, node)
            realmine += get_mines(node)
        orow += f"{Fore.GREEN}║ "
        print(orow)

    # Build the bottom border
    orow = f"   {Fore.GREEN}╚{"══"*(cols)}═╝ "
    print(orow)

    # Toss out some statistics, because we can
    nodes: int = rows*cols
    orow = f"{Fore.GREEN}Actual mine count is {str(realmine)} of {str(nodes)} points is {str(round(perc,2))}% coverage.{Fore.WHITE}"
    print(orow)

    # Show stats for the entire field
    orow = f"{Fore.WHITE}*:{str(realmine)}({str(round((realmine / (nodes) * 100),2))}%) "
    orow += f"\' \':{str(num[0])}({str(round((num[0] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTBLUE_EX}1:{str(num[1])}{Fore.WHITE}({str(round((num[1] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTGREEN_EX}2:{str(num[2])}{Fore.WHITE}({str(round((num[2] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTRED_EX}3:{str(num[3])}{Fore.WHITE}({str(round((num[3] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTYELLOW_EX}4:{str(num[4])}{Fore.WHITE}({str(round((num[4] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTCYAN_EX}5:{str(num[5])}{Fore.WHITE}({str(round((num[5] / (nodes) * 100),2))}%) "
    orow += f"{Fore.LIGHTMAGENTA_EX}6:{str(num[6])}{Fore.WHITE}({str(round((num[6] / (nodes) * 100),2))}%) "
    orow += f"{Fore.GREEN}7:{str(num[7])}{Fore.WHITE}({str(round((num[7] / (nodes) * 100),2))}%) "
    orow += f"{Fore.RED}8:{str(num[8])}{Fore.WHITE}({str(round((num[8] / (nodes) * 100),2))}%)"
    print(orow)


def main() -> None:
    """
    Runs the field() process and prompts to see if we run again or quit.
    """
    field()
    sinp = prompt()
    while sinp != 'q' and sinp != 'x':
        field()
        sinp = prompt()


if __name__ == '__main__':
    main()
