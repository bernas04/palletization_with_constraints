# Palletizing with adjacency constrain

The objective is to implement an optimization model for the palletizing problem extended by adjacency constraints. The constraints should have a form of two lists:

1. a list of pairs of element which have to be adjacent in the arrangement
2. a list of pairs of element which cannot be adjacent in the arrangement

The **_benchmarks/data_** directory contains the files with the data for the problem. The data files are in the format:

```
3   5
1   4
2   6
4   7
10  5
3   6

0   1
5   4
3   2

1   2
```

- The first section contains the dimensions of each element. The first number is the width and the second is the height.
- The second section contains the index of pairs of elements which have to be adjacent.
- The third section contains the index pairs of elements which cannot be adjacent.

Thus, the dimensions of elements will be:
[(3, 5), (1, 4), (2, 6), (4, 7), (10, 5), (3, 6)]

the adjacency elements will be:
[(0, 1), (5, 4), (3, 2)]

and the non-adjacency elements will be:
[(1, 2)]

**Note**: the adjacency and non-adjacency elements are indexed from 0, where 0 is the first element in the list and so on.

It is possible to solve this problem in two ways:

1. The basic one, without constraints
2. The extended one, with constraints

The solutions are stores in the **_benchmarks/_** directory, in the form of **three** files:

- The first one contains the position of each element in the arrangement, the area of the arrangement and the max values of **X** and **Y** coordinates.
- The second one is an image of the arrangement.
  </br>
  ![Image of the arrangement](benchmarks/file02/solutions_with_constrains/solution_file02_with_constrains.png)
  </br>
- The third one is the optimization progress over time.
  </br>
  ![Optimization progress](benchmarks/file02/file02_optimization_progress.png)

## How to run the program

```bash
python3 palletizationWithConstraints.py -f benchmarks/data/file01.txt
```
