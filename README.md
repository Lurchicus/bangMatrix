# bangMatrix

By Dan Rhea 2020 Licensed under the MIT license

I was finally able to track this program down on one of my backups.

This program simulates the way a mine sweeper game would populate
its game map. Nothing serious, just a fun exercise while I was 
learning Python. It's designed to run on a command shell in 
Windows or Linux. 

At some point I will go back through it and modernize the code.

## Dependencies

- colorama import Fore, Back
- random import randint

## History

- 06/29/2024 DWR Added the project to GitHub.
- 09/07/2024 DWR Converted a large if block into a match-case block.
- 09/07/2024 DWR Added a docstring to the program.
- 09/07/2024 DWR Removed zombie code.
- 09/07/2024 DWR Changed magenta to light magenta as magenta was not very visible.
- 09/09/2024 DWR Cleaned up the background handling as colorama thinks black is gray.
- 09/10/2024 DWR Removed two more Back references (background color) and tweaked some wording.
- 09/10/2024 DWR Moved the logic for setting the count in cells ajacent to one or more mines into a function.
- 09/10/2024 DWR Clearified the calculation that sets the target percentage for mine coverage.
- 02/26/2025 DWR Adding type notations (foo: int = 0). A work in progress.
- 02/26/2025 DWR Removed the inital output line describing mine coverage as it's redundant.
- 02/26/2025 DWR Switched to using format strings (print(f"foo:{foo}")).
