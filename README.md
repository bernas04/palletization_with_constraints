# Palletizing with adjacency constrain

The objective is to implement an optimization model for the palletizing problem extended by **constraints**.
Palletization refers to the process of arranging and organizing products or goods on a pallet in an efficient and effective manner,
the main objective of palletization is to maximize space utilization.

The extended version has constraints in the form of two lists:

1. a list of pairs of element which have to be adjacent in the arrangement
2. a list of pairs of element which cannot be adjacent in the arrangement

The **_benchmarks/data_** directory contains the files with the data for the problem. The data files have the following format:

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

The files must be divided into three sections, each section is separated by a blank line **\n**:

- The first section contains the dimensions of each element. The first number is the width and the second is the height.
- The second section contains the index of pairs of elements which have to be adjacent.
- The third section contains the index pairs of elements which cannot be adjacent.

Thus, the dimensions of elements will be:

- **[(3, 5), (1, 4), (2, 6), (4, 7), (10, 5), (3, 6)]**

the adjacency elements will be:

- **[(0, 1), (5, 4), (3, 2)]**

and the non-adjacency elements will be:

- **[(1, 2)]**

**Note**: the adjacency and non-adjacency elements are indexed from 0, where 0 is the first element in the list and so on.

## Solution

It is possible to solve this problem in two ways:

1. The basic one, without constraints
2. The extended one, with constraints

### Solve the problem without constraints

To solve this problem without constraints, it's only necessary to have the possible positions of each shape (horizontal and vertical) and then add that constraint to the model as in the following way:

```python
model.AddNoOverlap2D(horizontal, vertical)
```

### Solve the problem with constraints

To solve this problem with constraints, several constraints were added to the model.

Given two shapes with the initial and final coordinates like:

- shape1: [(x1a, y1a), (x1b, y1b)]
- shape2: [(x2a, y2a), (x2b, y2b)]

![Conditions to be adjacent](https://github.com/bernas04/palletization_with_constraints/blob/main/img/shapes_points.jpg?raw=true)

### Adjacent shapes

</br>
To these shapes be adjacent, one of the following conditions must be met:

- x1b == x2a
  </br>
  ![X1B==X2A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/x1b__x2a.jpg?raw=true)

- x1a == x2b
  </br>
  ![X1A==X2B](https://github.com/bernas04/palletization_with_constraints/blob/main/img/x1a__x2b.jpg?raw=true)

- y2b == y1a
  </br>
  ![Y2B==Y1A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/y2b__y1a.jpg?raw=true)
- y1b == y2a
  </br>
  ![Y1B==Y2A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/y1b__y2a.jpg?raw=true)

Despite the above-mentioned conditions, they are insufficient because circumstances such as those shown below may arise.

![Contraexemplo](https://github.com/bernas04/palletization_with_constraints/blob/main/img/contra_exemplo.jpg?raw=true)</br>
In this example **x2b==x1a** (second condition), however the shapes are not adjacent</br>
![Contraexemplo2](https://github.com/bernas04/palletization_with_constraints/blob/main/img/contra_exemplo2.jpg?raw=true)</br>
Regarding the picture above, **y1b==y2a** (fourth condition) and again the shapes are not adjacent.

Thus, stricter conditions need to be added to the model:

- **x1b == x2a ^ y2b > y1a ^ y2a < y1b**

- **x1a == x2b ^ y2b > y1a ^ y2a < y1b**

- **y2b == y1a ^ x2b > x1a ^ x2a < x1b**

- **y1b == y2a ^ x2b > x1a ^ x2a < x1b**

### Non Adjacent shapes

To these shapes be non adjacent, one of the following conditions must be met:

- **x1b < x2a**

  ![X1B<X2A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/x1b_l_x1a.jpg?raw=true)

- **x2b < x1a**

  ![X2B<X1A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/x2b_l_x1a.jpg?raw=true)

- **y1b < y2a**

  ![Y1B<Y2A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/y1b_l_y2a.jpg?raw=true)

- **y2b < y1a**

  ![Y2B<Y1A](https://github.com/bernas04/palletization_with_constraints/blob/main/img/y2b_l_y1a.jpg?raw=true)

In this case the conditions are so strict that it is not necessary to add more conditions to the model.

## Results

The solutions are stores in the **_benchmarks/_** directory and inside the folder with the same name as the file used to run the program. Inside this folder, two directories are created, one for the solution without constraints and the other for the solution with constraints. Each directory contains two files:

- The first one contains the position of each element in the arrangement, the area of the arrangement, the max values of **X** and **Y** coordinates, the **area** and the **occupation rate**.
- The second one is an image of the arrangement. In this example the [file02.txt](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/data/file02.txt) contains the following data:

```
10  10
5   4
5   8
9   8
2   1
11  9
17  20
14  9
4   9

0   6
5   4

2   3
7   8
1   2
6   7
3   7
1   8
```

So, it means 9 objects are presented in this arranjement. The object **number 0** and the object **number 6** must be adjacent in the solution, as well as the objects **number 5** and **number 4**. At the same time the objects presented in the next list of two pairs must not be adjacent:

**Non-adjacent pairs:**

**(2, 3)** </br>
**(7, 8)** </br>
**(1, 2)** </br>
**(6, 7)** </br>
**(3, 7)** </br>
**(1, 8)**

### Comparing solution with and without constraints

**With constraints solution**
![Image of the arrangement](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file02/solutions_with_constrains/solution_file02_with_constrains.png?raw=True)

As it is possible to see, the adjacent pairs are, indeed adjacents: <br> (0,6) </br>
(5,4)

and all pairs present in the non-adjacency list comply with this same non-adjacency condition.

**Without constraints solution**
![Image of the arrangement](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file02/solutions_without_constrains/solution_file02_without_constrains.png?raw=True)

As it's possible to see, in this solution, the pairs:</br>
(0, 6) </br>
(5,4) </br>

are not adjacent, unlike the previous solution where this condition had to be met.

Regarding the non adjacency contraint, the following pairs are presented in the non adjacency list, however in this solution they are adjacents.

**(1, 2)** </br>
**(6, 7)** </br>
**(3, 7)** </br>

### Optimization progress

Inside the directory with the same name as the file used to run the program, there is an image that shows the optimization progress over time for the solution **with** and **without** constraints.
</br>

**Behaviour of objective function depending of the applied constraints**

Constraints directly influence the objective function by restricting the set of feasible solutions. The objective function represents the goal which in this example represents minimizing the area. When constraints are introduced, the feasible solution space is reduced, and the objective function is evaluated only for the solutions that satisfy all constraints. This can take more time, once more calculations are required.

**In this example**, as you can see the best solution with constraints took more time to be found than the solution without constraints. So in general, **the more constraints** the problem has, **the higher the time** necessary to solve the problem.

![Optimization progress](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file08/file08_optimization_progress.png?raw=true)

However, in the following case the solution without constraints took more time to be found and it's worse in terms of value, than the solution with constraints.

![Optimization progress](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file06/file06_optimization_progress.png?raw=true)

**Graph analyse**

As it is possible to analyse from the images, the value returned from **Objective Function** is maximum in the beggining, but it is also in the beggining that it find more number of solutions and as the time goes by the number of solutions is lower, but the solution value is higher.

This graph has the same behaviour as the positive part of inverse function, shown in the follow image.

![Inverse Function](https://github.com/bernas04/palletization_with_constraints/blob/main/img/inversefunction.png?raw=true)

## How to run the program

It is possible to run the program with a file created by your own, you just have to put the correct path, to the file, like in the command below:

```bash
python3 palletizationWithConstraints.py -f benchmarks/data/file01.txt
```

If you don't want to create your own file, you can use one of the files in the **_benchmarks/data_** directory. The command above will run the program with the file **_file01.txt_**.

## Results with my files

<table >
<tbody>
<tr style=" background-color: #808080;">
<td>&nbsp;</td>
<td style=" text-align: center; vertical-align: middle;" colspan="2"><strong>With Constraints</strong></td>
<td style=" text-align: center; vertical-align: middle;" colspan="2"><strong>Without contraints</strong></td>
</tr>
<tr >
<td><strong>File</strong></td>
<td ><strong>Area</strong></td>
<td ><strong>Occupation (%)</strong></td>
<td ><strong>Area</strong></td>
<td ><strong>Occupation (%)</strong></td>
</tr>
<tr >
<td ><strong>file00.txt</strong></td>
<td>532</td>
<td style=" text-align: center; vertical-align: middle;">97.6</td>
<td >527</td>
<td style=" text-align: center; vertical-align: middle;">98.5</td>
</tr>
<tr >
<td ><strong>file01.txt</strong></td>
<td >130</td>
<td style=" text-align: center; vertical-align: middle;">97.7</td>
<td >130</td>
<td style=" text-align: center; vertical-align: middle;">97.7</td>
</tr>
<tr >
<td ><strong>file02.txt</strong></td>
<td >864</td>
<td style=" text-align: center; vertical-align: middle;">96.6</td>
<td >858</td>
<td style=" text-align: center; vertical-align: middle;">97.3</td>
</tr>
<tr >
<td ><strong>file03.txt</strong></td>
<td >15158</td>
<td style=" text-align: center; vertical-align: middle;">98</td>
<td >15000</td>
<td style=" text-align: center; vertical-align: middle;">99</td>
</tr>
<tr >
<td ><strong>file04.txt</strong></td>
<td >5047</td>
<td style=" text-align: center; vertical-align: middle;">97</td>
<td >4998</td>
<td style=" text-align: center; vertical-align: middle;">98</td>
</tr>
<tr>
<td><strong>file05.txt</strong></td>
<td>1950</td>
<td style=" text-align: center; vertical-align: middle;">99.3</td>
<td >1943</td>
<td style=" text-align: center; vertical-align: middle;">99.7</td>
</tr>
<tr >
<td ><strong>file06.txt</strong></td>
<td >560</td>
<td style=" text-align: center; vertical-align: middle;">97.1</td>
<td >550</td>
<td style=" text-align: center; vertical-align: middle;">98.9</td>
</tr>
<tr >
<td ><strong>file07.txt</strong></td>
<td >4416</td>
<td style=" text-align: center; vertical-align: middle;"><b>97.9</b></td>
<td >4450</td>
<td style=" text-align: center; vertical-align: middle;"><b>97.2</b></td>
</tr>
<tr >
<td ><strong>file08.txt</strong></td>
<td >59118</td>
<td style=" text-align: center; vertical-align: middle;">97.7</td>
<td >58680</td>
<td style=" text-align: center; vertical-align: middle;">98.5</td>
</tr>
<tr >
<td ><strong>file09.txt</strong></td>
<td >110</td>
<td style=" text-align: center; vertical-align: middle;">100</td>
<td >110</td>
<td style=" text-align: center; vertical-align: middle;">100</td>
</tr>
</tbody>
</table>

To test the developed solution, 10 files were created with different data. The results are presented in the table below.

I'd like to notice that for file number 9, the solution with and without constraints found was the perfect one, once the occupation percentage is 100%. The maximum percentage difference between the solution with and without constraints is **1.8%** and it takes place to [file06.txt](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/data/file06.txt), thus it's possible to conclude that the implementation of this algorithm produces good results.

Another interesting thing is regarding the results of [file07.txt](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/data/file07.txt), as you can see in the table the solution with constraints is better than the solution without constraints, what was unexpected once the outcomes of all other files are better in the solution without constraints than in the solution with constraints.
![File07](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file07/file07_optimization_progress.png?raw=True)

As you can see the best solution with constraints was found near **2500 seconds**, approximately **42 minutes**, while the solution without constraints was found near **1000 seconds** (+/- 17 minutes). Once the solver time is limited to **one** hour, it suggests that it most likely did not have enough time to develop a better solution than the constraint solver.

![Solution file 7 with constraints](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file07/solutions_with_constrains/solution_file07_with_constrains.png?raw=True)

![Solution file 7 without constraints](https://github.com/bernas04/palletization_with_constraints/blob/main/benchmarks/file07/solutions_without_constrains/solution_file07_without_constrains.png?raw=True)

Although it seems that the unconstrained solution is better, in reality it is not, since the axis boundaries are not the same in both images.

**Note**
</br>
More results can be found inside benchmarks directory.

# Author

Work done by [João Farias](https://www.linkedin.com/in/jo%C3%A3o-farias-7a7b48266/)
</br>
[Politechnika Rzeszowska](https://w.prz.edu.pl/), June 2023.
