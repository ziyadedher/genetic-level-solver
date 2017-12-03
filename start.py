"""Main menu of the program.
"""


def prompt(mess, default=None):
    """Asks a user for input, with error handling.
    """
    # Asks until a valid input is given.
    while True:
        out = input(mess)
        # Returns default if it is set and no answer was given
        if default is not None and out == "":
            return default
        try:
            out = int(out)
        except ValueError:
            print("Please enter a valid input.")
            continue
        else:
            return out


def main():
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

    if ans == 2:
        # Imports the simulation
        import simulation

        # Asks the user for parameters
        print("")
        gens = prompt("Number of Generations (default: 250): ", 250)
        num = prompt("Number of Creatures (default: 100): ", 100)
        movs = prompt("Number of Moves per Creature (default: 100): ", 100)
        step = prompt("Evolution Step (default: 10): ", 10)

        # Starts the simulation with the given parameters
        sim = simulation.Simulation()
        sim.start(gens, num, movs, draw_step=step)
    elif ans == 1:
        # Imports the level creator which auto-starts
        import level_creator
        level_creator.main()


if __name__ == '__main__':
    main()
