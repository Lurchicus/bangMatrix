"""
bangmatrix.py
A "minefield" map creator and analyzer by Dan Rhea (c) 2020
Creates a map of 10 to 24 rows by 40 to 80 colums that is
salted with mines. This map can then be fed to a
ML process to solve. I abandoned the ML idea for now and
just show the minefield we create.
"""
from random import randint
from colorama import Fore, Back


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


# Determine the map dimensions and set the count of mines we will scatter over it to
# 15.21 % of (rows*cols). Since I have the numbers here, caclulate the percentage of 
# mine coverage we will be working with to double check the coverage.
rows: int = randint(6,34)
cols: int = randint(10,62)
cPer: float = 15.21
# mine count should be ~15.21% of rows*cols
mine: int = int(round(((rows*cols) / (100/cPer)), 0))
perc: float = ((mine / (rows*cols)) * 100)

#print(Fore.GREEN + "Rows: "+str(rows)+
#    " cols: "+str(cols)+
#    " mine: "+str(mine)+
#
#     " is "+str(round(perc,2))+
#    "% (target: "+str(round(cPer,2))+"%)."+Fore.WHITE)

bangbox: list[list[int]] = [[0 for col in range(cols)] for row in range(rows)]

# Create a minefield
set_mine: int = 0
while set_mine < mine:
    row_i: int = randint(0, rows-1)
    col_i: int = randint(0, cols-1)
    if bangbox[row_i][col_i] == 0:
        bangbox[row_i][col_i] = -1
        set_mine += 1

# Scan the field for mines and set ajacent counts
look_around(bangbox, rows, cols)

# Output the minefield
print(Fore.GREEN + "Revealed map:" + Fore.WHITE)

# Build and output the column header 
firstDigit: str = "     " + Fore.YELLOW
secondDigit: str = "     " + Fore.YELLOW
for col in range(cols):
    scol: str = str(col)
    if col < 10:
        scol = "0" + scol
    firstDigit += scol[0:1] + " "
    secondDigit += scol[1:2] + " "
print(firstDigit + "  ")
print(secondDigit + "  ")

orow = "   "+ Fore.GREEN + "╔" + "══"*(col+1) + "═╗ "
print(orow)

# And now the rest of the map
realmine = 0
num0 = num1 = num2 = num3 = num4 = num5 = num6 = num7 = num8 = 0
for row in range(rows):
    # column header
    srow = str(row)
    if len(srow) == 1:
        srow = "0" + srow
    orow = Fore.YELLOW + srow + Fore.GREEN + " ║ "
    # then the mines. BangBox: -1 mine, 0 open, 1-8 open next to a mine
    for col in range(cols):
        node = bangbox[row][col]
        match node:
            case -1:
                orow += Fore.WHITE + "* " + Fore.WHITE
                realmine += 1
            case 0:
                orow += "  "
                num0 += 1
            case 1:
                orow += Fore.LIGHTBLUE_EX + str(node) + " " + Fore.WHITE
                num1 += 1
            case 2:
                orow += Fore.LIGHTGREEN_EX + str(node) + " " + Fore.WHITE
                num2 += 1
            case 3:
                orow += Fore.LIGHTRED_EX + str(node) + " " + Fore.WHITE
                num3 += 1
            case 4:
                orow += Fore.LIGHTYELLOW_EX + str(node) + " " + Fore.WHITE
                num4 += 1
            case 5:
                orow += Fore.LIGHTCYAN_EX + str(node) + " " + Fore.WHITE
                num5 += 1
            case 6:
                orow += Fore.LIGHTMAGENTA_EX + str(node) + " " + Fore.WHITE
                num6 += 1
            case 7:
                orow += Fore.GREEN + str(node) + " " + Fore.WHITE
                num7 += 1
            case 8:
                orow += Fore.RED + str(node) + " " + Fore.WHITE
                num8 += 1
    orow += Fore.GREEN + "║ "
    print(orow)
orow = "   "+ Fore.GREEN + "╚" + "══"*(cols) + "═╝ "
print(orow)

# Toss out some statistics because we can
nodes = rows*cols    
print(Fore.GREEN + "Actual mine count is " + str(realmine) + " of " + str(nodes) + " points is " + str(round(perc,2)) + "% coverage." + Fore.WHITE)
print(Fore.WHITE + "*:" + str(realmine) + "(" + str(round((realmine / (nodes) * 100),2)) + ")" +
    " :" + str(num0) + "(" + str(round((num0 / (nodes) * 100),2)) + "%) " + 
    Fore.LIGHTBLUE_EX + "1:" + str(num1) + Fore.WHITE + "(" + str(round((num1 / (nodes) * 100),2)) + "%) " +
    Fore.LIGHTGREEN_EX + "2:" + str(num2) + Fore.WHITE + "(" + str(round((num2 / (nodes) * 100),2)) + "%) " +
    Fore.LIGHTRED_EX + "3:" + str(num3) + Fore.WHITE + "(" + str(round((num3 / (nodes) * 100),2)) + "%) " +
    Fore.LIGHTYELLOW_EX + "4:" + str(num4) + Fore.WHITE + "(" + str(round((num4 / (nodes) * 100),2)) + "%) " +
    Fore.LIGHTCYAN_EX + "5:" + str(num5) + Fore.WHITE + "(" + str(round((num5 / (nodes) * 100),2)) + "%) " +
    Fore.LIGHTMAGENTA_EX + "6:" + str(num6) + Fore.WHITE + "(" + str(round((num6 / (nodes) * 100),2)) + "%) " +
    Fore.GREEN + "7:" + str(num7) + Fore.WHITE + "(" + str(round((num7 / (nodes) * 100),2)) + "%) " +
    Fore.RED + "8:" + str(num8) + Fore.WHITE + "(" + str(round((num8 / (nodes) * 100),2)) + "%)" + Fore.WHITE)
