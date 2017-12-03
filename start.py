print("Welcome to the Genetic Level Solver!")
print("Made in 8 hours at the UofT S.G. Local Hack Day 2017")
print("[1] Level Creator")
print("[2] Simulator")
print("[3] Quit")

prompt = "Choose one of the above: "
ans = int(input(prompt))
while ans not in (1, 2, 3):
    print("Choose either 1, 2, or 3.")
    ans = int(input(prompt))

if ans == 2:
    import simulation

    gens = int(input("Number of Generations (integer): "))
    num = int(input("Number of Creatures (integer): "))
    movs = int(input("Number of Moves per Creature (integer): "))
    step = int(input("Show Progress Every How Many Evolutions (integer)? "))

    sim = simulation.Simulation()
    sim.start(gens, num, movs, draw_step=step)
elif ans == 1:
    import level_creator
