# Palletizing with adjacency constrain

The objective is to implement an optimization model for the palletizing problem extended by **constraints**. The constraints should have a form of two lists:

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

The files must be divided into three sections, each section is separated by a blank line **\n**:

- The first section contains the dimensions of each element. The first number is the width and the second is the height.
- The second section contains the index of pairs of elements which have to be adjacent, these shapes start from index 0 (0 element (3,5), 1 element (1,4) and so on).
- The third section contains the index pairs of elements which cannot be adjacent.

Thus, the dimensions of elements will be:
**[(3, 5), (1, 4), (2, 6), (4, 7), (10, 5), (3, 6)]**

the adjacency elements will be:
**[(0, 1), (5, 4), (3, 2)]**

and the non-adjacency elements will be:
**[(1, 2)]**

**Note**: the adjacency and non-adjacency elements are indexed from 0, where 0 is the first element in the list and so on.

## Solution

It is possible to solve this problem in two ways:

1. The basic one, without constraints
2. The extended one, with constraints

To solve this problem with constrains, several constraints were added to the model. Given two shapes with the initial and final coordinates like:

- shape1: [(x1a, y1a), (x1b, y1b)]
- shape2: [(x2a, y2a), (x2b, y2b)]

### Adjacent shapes

![Conditions to be adjacent](img/shapes_points.jpg?raw=true)
</br>
To these shapes be adjacent, one of the following conditions must be met:

- x1b == x2a
  </br>
  ![X1B==X2A](img/x1b__x2a.jpg?raw=true)

- x1a == x2b
  </br>
  ![X1A==X2B](img/x1a__x2b.jpg?raw=true)

- y2b == y1a
  </br>
  ![Y2B==Y1A](img/y2b__y1a.jpg?raw=true)
- y1b == y2a
  </br>
  ![Y1B==Y2A](img/y1b__y2a.jpg?raw=true)

however, this is not enought once the shapes may remain non-adjacent.

![Contraexemplo](img/contra_exemplo.jpg?raw=true)</br>
![Contraexemplo2](img/contra_exemplo2.jpg?raw=true)

In these examples the second condition is met (**x1a==x2b**), but the shapes are non adjacent, in the first image and in the second image, the fourth condition is achieved. Thus, stricter conditions need to be added to the model:

- **x1b == x2a ^ y2b > y1a ^ y2a < y1b**

- **x1a == x2b ^ y2b > y1a ^ y2a < y1b**

- **y2b == y1a ^ x2b > x1a ^ x2a < x1b**

- **y1b == y2a ^ x2b > x1a ^ x2a < x1b**

### Non Adjacent shapes

To these shapes be non adjacent, one of the following conditions must be met:

- **x1b < x2a**

  ![X1B<X2A](img/x1b_l_x1a.jpg?raw=true)

- **x2b < x1a**

  ![X2B<X1A](img/x2b_l_x1a.jpg?raw=true)

- **y1b < y2a**

  ![Y1B<Y2A](img/y1b_l_y2a.jpg?raw=true)

- **y2b < y1a**

  ![Y2B<Y1A](img/y2b_l_y1a.jpg?raw=true)

In this case the conditions are so strict that it is not necessary to add more conditions to the model.

## Results

The solutions are stores in the **_benchmarks/_** directory and inside the folder with the same name as the file used to run the program. Inside this folder, two directories are created, one for the solution without constraints and the other for the solution with constraints. Each directory contains two files:

- The first one contains the position of each element in the arrangement, the area of the arrangement, the max values of **X** and **Y** coordinates, the **area** and the **occupation rate**.
- The second one is an image of the arrangement.
  </br>
  ![Image of the arrangement](benchmarks/file02/solutions_with_constrains/solution_file02_with_constrains.png?raw=true)
  </br>

Inside the directory with the same name as the file used to run the program, there is an image that shows the optimization progress over time for the solution **with** and **without** constraints.
</br>
![Optimization progress](benchmarks/file02/file02_optimization_progress.png?raw=true)

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

**Note**
</br>
More results can be found inside benchmarks directory.

# Author

Work done by [João Farias](https://www.linkedin.com/in/jo%C3%A3o-farias-7a7b48266/)
</br>
[Politechnika Rzeszowska](https://w.prz.edu.pl/), June 2023.
