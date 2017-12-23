"""Main menu of the program.
"""


def prompt(mess: str, default: int = None) -> int:
    """Asks a user for input, with error handling.
    """
    # Asks until a valid input is given.
    while True:
        # Asks for input
        out = input(mess)

        # Returns <default> if it is set and no input was provided
        if default is not None and out == "":
            return default

        # Parses input
        try:
            out = int(out)
            if out < 1:
                raise ValueError
        except ValueError:
            print("Please enter a valid input.")
            continue
        else:
            return out


def main() -> None:
    """Runs the main menu.
    """

    # Displays instructions
    print("Welcome to the Genetic Level Solver!")
    print("[1] Level Creator")
    print("[2] Simulator")
    print("[3] Quit")

    # Asks the user what they want to do.
    message = "Choose one of the above\n> "
    ans = prompt(message)
    while ans not in (1, 2, 3):
        print("Choose either 1, 2, or 3.")
        ans = prompt(message)

    if ans == 1:
        # Imports the level creator which auto-starts
        import level_creator
        level_creator.main()

    elif ans == 2:
        # Imports the simulation
        import simulation

        # Asks the user for parameters
        print("")
        gens = prompt("Number of Generations (default: 250): ", 250)
        num = prompt("Number of Creatures (default: 100): ", 100)
        movs = prompt("Number of Moves per Creature (default: 100): ", 100)
        step = prompt("Evolution Step (default: 10): ", 10)
        interval = prompt("Movement interval in ms (default: 0): ", 0)

        # Starts the simulation with the given parameters
        sim = simulation.Simulation()
        sim.settings(draw_step=step, interval=interval)
        sim.start(gens, num, movs)


if __name__ == '__main__':
    main()