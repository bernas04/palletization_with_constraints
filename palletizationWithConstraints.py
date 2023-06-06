import sys, getopt, os, math
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, model):
        self.model = model
        self.solutions = []
        cp_model.CpSolverSolutionCallback.__init__(self)

    def on_solution_callback(self):
        current_objective = self.ObjectiveValue()
        current_time = self.WallTime()
        self.solutions.append((current_time, current_objective))

    def getSolution(self):
        return self.solutions


def main(argv, mode, listData=None):
    inputfile = ""
    palletizationWithConstaints = mode

    opts, args = getopt.getopt(argv, "hf:", ["file="])
    if len(opts) == 0:
        print("python3 palletizationWithConstraints.py -f <inputfile>")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("python3 palletizationWithConstraints.py -f <inputfile>")
            sys.exit()
        elif opt in "-n":
            palletizationWithConstaints = "without"
        elif opt in ("-f", "--file"):
            inputfile = arg
        else:
            print("python3 palletizationWithConstraints.py -f <inputfile>")
            sys.exit()

    print(f">> Running palletization {palletizationWithConstaints} constraints")

    size_factor = 1.5
    # this data shows the dimensions of the elements (width, height)
    data = []
    adjacent_pairs = []
    non_adjacent_pairs = []

    # read the benchmarks files
    # f = open("benchmarks/data/file01.txt", "r")
    f = open(inputfile, "r")
    fileName = f.name.split("/")[2].replace(".txt", "")
    allLines = f.readlines()
    f.close()

    # parse the data from the file
    # data is a list of tuples (width, height)
    # adjacent_pairs is a list of tuples (element1, element2)
    # non_adjacent_pairs is a list of tuples (element1, element2)
    # elements start from 0

    if listData == None:
        tmp = []
        newLineNumber = 0
        for line in allLines:
            if line != "\n":
                a, b = line.split()
                tmp.append((int(a), int(b)))
            elif line == "\n":
                if newLineNumber == 0:
                    data = tmp.copy()
                elif newLineNumber == 1:
                    adjacent_pairs = tmp.copy()
                newLineNumber += 1
                tmp.clear()
        if newLineNumber == 2 or newLineNumber == 3:
            non_adjacent_pairs = tmp.copy()

        # sort adjacent pairs list based on first element of tuple
        adjacent_pairs = sorted(adjacent_pairs, key=lambda x: x[0])
        adjacent_pairs = [(min(x), max(x)) for x in adjacent_pairs]

        # sort non adjacent pairs list based on first element of tuple
        non_adjacent_pairs = sorted(non_adjacent_pairs, key=lambda x: x[0])
        non_adjacent_pairs = [(min(x), max(x)) for x in non_adjacent_pairs]
    else:
        data = listData

    lb = sum(d[0] * d[1] for d in data)
    max_size = math.ceil(size_factor * math.sqrt(lb))

    model = cp_model.CpModel()

    xmax = model.NewIntVar(0, max_size, "x_max")
    ymax = model.NewIntVar(0, max_size, "y_max")

    horizontal = []
    vertical = []

    # basic condition to not overlap
    counter = 0
    for element in data:
        a, b = element

        x1 = model.NewIntVar(0, max_size, f"x1_{counter}")
        y1 = model.NewIntVar(0, max_size, f"y1_{counter}")
        x2 = model.NewIntVar(0, max_size, f"x2_{counter}")
        y2 = model.NewIntVar(0, max_size, f"y2_{counter}")
        o = model.NewBoolVar(f"o_{counter}")
        model.Add(x2 <= xmax)
        model.Add(y2 <= ymax)

        horizontal.append(
            model.NewIntervalVar(x1, a + o * (b - a), x2, f"hor_{counter}")
        )
        vertical.append(model.NewIntervalVar(y1, b + o * (a - b), y2, f"ver_{counter}"))
        counter += 1

    model.AddNoOverlap2D(horizontal, vertical)

    if palletizationWithConstaints == "with":
        # Constraint: adjacent pairs must be adjacent
        for pair in adjacent_pairs:
            # a -> first element
            # b -> second element

            a, b = pair

            x1a = horizontal[a].StartExpr()
            x1b = horizontal[a].EndExpr()
            y1a = vertical[a].StartExpr()
            y1b = vertical[a].EndExpr()
            x2a = horizontal[b].StartExpr()
            x2b = horizontal[b].EndExpr()
            y2a = vertical[b].StartExpr()
            y2b = vertical[b].EndExpr()

            v1 = [model.NewBoolVar(f"v_{i}_{a}_{b}") for i in range(4)]

            model.Add(x1b == x2a).OnlyEnforceIf(v1[0])
            model.Add(y2b > y1a).OnlyEnforceIf(v1[0])
            model.Add(y2a < y1b).OnlyEnforceIf(v1[0])

            model.Add(x1a == x2b).OnlyEnforceIf(v1[1])
            model.Add(y2b > y1a).OnlyEnforceIf(v1[1])
            model.Add(y2a < y1b).OnlyEnforceIf(v1[1])

            model.Add(y1b == y2a).OnlyEnforceIf(v1[2])
            model.Add(x2b > x1a).OnlyEnforceIf(v1[2])
            model.Add(x2a < x1b).OnlyEnforceIf(v1[2])

            model.Add(y1a == y2b).OnlyEnforceIf(v1[3])
            model.Add(x2b > x1a).OnlyEnforceIf(v1[3])
            model.Add(x2a < x1b).OnlyEnforceIf(v1[3])

            model.Add(sum(v1) >= 1)

        # Constraint: non adjacent pairs must not be adjacent
        for pair in non_adjacent_pairs:
            # a -> first element
            # b -> second element

            a, b = pair

            x1a = horizontal[a].StartExpr()
            x1b = horizontal[a].EndExpr()
            y1a = vertical[a].StartExpr()
            y1b = vertical[a].EndExpr()
            x2a = horizontal[b].StartExpr()
            x2b = horizontal[b].EndExpr()
            y2a = vertical[b].StartExpr()
            y2b = vertical[b].EndExpr()

            v2 = [model.NewBoolVar(f"v_{i}_{a}_{b}") for i in range(4)]

            model.Add(x1b < x2a).OnlyEnforceIf(v2[0])
            model.Add(x2b < x1a).OnlyEnforceIf(v2[1])
            model.Add(y1b < y2a).OnlyEnforceIf(v2[2])
            model.Add(y2b < y1a).OnlyEnforceIf(v2[3])
            model.Add(sum(v2) >= 1)

    area = model.NewIntVar(0, max_size * max_size, "area")
    model.Add(area >= lb)
    model.AddMultiplicationEquality(area, [xmax, ymax])
    model.Minimize(area)

    solver = cp_model.CpSolver()

    solution_printer = SolutionPrinter(model)  #

    # 60 minutes maximum time
    solver.parameters.max_time_in_seconds = 3600

    status = solver.Solve(model, solution_callback=solution_printer)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        os.chdir("benchmarks")
        if not os.path.isdir(f"{fileName}"):
            os.mkdir(f"{fileName}")
        os.chdir(f"{fileName}")

        if not os.path.isdir(f"solutions_{palletizationWithConstaints}_constrains"):
            os.mkdir(f"solutions_{palletizationWithConstaints}_constrains")
        os.chdir(f"solutions_{palletizationWithConstaints}_constrains")

        f = open(
            f"solution_{fileName}_{palletizationWithConstaints}_constrains.txt", "w"
        )
        f.write(
            f"Optimal: xmax = {solver.Value(xmax)}, ymax = {solver.Value(ymax)}, area = {solver.ObjectiveValue()}, occupation percentage = {round((lb/solver.ObjectiveValue()*100),1)}\n"
        )

        solution = []
        coloringData = []
        print(
            f"\tOptimal: xmax = {solver.Value(xmax)}, ymax = {solver.Value(ymax)}, area = {solver.ObjectiveValue()}, occupation percentage = {round((lb/solver.ObjectiveValue())*100,1)}"
        )
        xLimit = solver.Value(xmax)
        yLimit = solver.Value(ymax)

        for i in range(counter):
            pos = (
                solver.Value(horizontal[i].StartExpr()),
                solver.Value(horizontal[i].EndExpr()),
                solver.Value(vertical[i].StartExpr()),
                solver.Value(vertical[i].EndExpr()),
            )
            solution.append(pos)
            print("\tnum=%i, x1=%i, x2=%i, y1=%i, y2=%i" % ((i,) + pos))
            coloringData.append(
                {"num": i, "x1": pos[0], "x2": pos[1], "y1": pos[2], "y2": pos[3]}
            )
            f.write("num=%i, x1=%i, x2=%i, y1=%i, y2=%i\n" % ((i,) + pos))
        f.close()

        palette = sns.color_palette(n_colors=len(data))

        # Create a figure and axis
        fig, ax = plt.subplots()
        # Plot rectangles with different face colors and shape index labels
        for i, shape in enumerate(coloringData):
            x = shape["x1"]
            y = shape["y1"]
            width = shape["x2"] - shape["x1"]
            height = shape["y2"] - shape["y1"]
            rect = patches.Rectangle(
                (x, y),
                width,
                height,
                linewidth=1,
                edgecolor="black",
                facecolor=palette[i],
            )
            ax.add_patch(rect)

            # Add shape index label
            label_x = x + width / 2
            label_y = y + height / 2
            ax.text(
                label_x,
                label_y,
                str(shape["num"]),
                color="black",
                ha="center",
                va="center",
            )

            # Set axis limits
        ax.set_xlim(0, xLimit)
        ax.set_ylim(0, yLimit)

        # Set labels and title
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title(
            f"{fileName}: Palletization solution {palletizationWithConstaints} constraints"
        )

        # Show the plot
        plt.savefig(f"solution_{fileName}_{palletizationWithConstaints}_constrains.png")
        plt.clf()

        os.chdir("../../..")
        return data, solution_printer.getSolution(), fileName

    else:
        print("No solution")
        sys.exit(0)


if __name__ == "__main__":
    data, timeAndObjectiveValues1, fileName = main(sys.argv[1:], "with")
    data, timeAndObjectiveValues2, fileName = main(sys.argv[1:], "without", data)

    os.chdir(f"benchmarks/{fileName}")

    x_axis_1 = [x[0] for x in timeAndObjectiveValues1]
    y_axis_1 = [x[1] for x in timeAndObjectiveValues1]

    x_axis_2 = [x[0] for x in timeAndObjectiveValues2]
    y_axis_2 = [x[1] for x in timeAndObjectiveValues2]

    plt.plot(x_axis_1, y_axis_1, label="Palletization with constraints")
    plt.plot(x_axis_2, y_axis_2, label="Palatalization without constraints")
    plt.legend()

    plt.xlabel("Time in seconds")
    plt.ylabel("Objective value")
    plt.title(f"{fileName}: objective value over time")
    plt.savefig(f"{fileName}_optimization_progress.png")
