# Dice Challenge

This is a solution to the challenge presented
[here](https://www.youtube.com/watch?v=p0J8kIoQF6I).

## Problem statement

Roll two [D8s](https://en.wikipedia.org/wiki/Dice#Common_variations) and add up
the values. There is a:
* 1/64 chance to get 2.
* 2/64 chance to get 3.
* 3/64 chance to get 4.
* 4/64 chance to get 5.
* 5/64 chance to get 6.
* 6/64 chance to get 7.
* 7/64 chance to get 8.
* 8/64 chance to get 9.
* 7/64 chance to get 10.
* 6/64 chance to get 11.
* 5/64 chance to get 12.
* 4/64 chance to get 13.
* 3/64 chance to get 14.
* 2/64 chance to get 15.
* 1/64 chance to get 16.

**Challenge:** Come up with a pair of 8-sided dice that have the same
probability distribution as shown above, where the sides are labeled
differently from standard D8s.

## Formalization as an SMT formula

The plan is to pose the problem as an [SMT
formula](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories), to then
find solutions using the [Z3 SMT solver](https://github.com/Z3Prover/z3).

### Constants

Given two standard $N$-sided dice, the probability that their sum will add up to
$n$ is denoted by $P_n/N^2$, with $n = 1, \dots, 2N$. For example, when $N = 8$,
we have $P_1 = 0$, $P_2 = 1$, $P_3 = 2$, $P_4 = 3$, and so on.

### Free variables

* $x_i \in \mathbb{N}$, represents the value of the label on face number
  $i$ of dice 1, where $i = 1, \dots, N$.
* $y_i \in \mathbb{N}$, represents the value of the label on face number
  $i$ of dice 2, where $i = 1, \dots, N$.

### Constraints

* Range of $x_i$ and $y_i$: 
  
  for $i = 1, \dots, N$,  
  $\quad 1 \leq x_i \leq 2N \text{ and } 1 \leq y_i \leq 2N.$

* Probabilities match standard D8s: 

  for $n = 1, \dots, N$,  
  $\quad |\lbrace x_i + y_j = n  \mid i, j = 1, \dots, 8 \rbrace| = P_n.$

* The faces are sorted in ascending order (to avoid repeats): 

  for $i = 1, \dots, N - 1$,  
  $\quad x_i \leq x_{i + 1} \text{ and } y_i \leq y_{i + 1}.$

### Finding new solutions

Once we find $x^\star_i$ and $y^\star_i$ that satisfy the constraints, we can include the
following additional constraint to disallow getting the same solution when
running the solver again:

$(\bigvee_{i = 1, \dots N} x_i \neq x^\star_i) \text{ and } (\bigvee_{i = 1, \dots N} x_i \neq y^\star_i).$

Notice that the right-hand side of the conjunction is $x_i \neq y^\star_i$ and
**NOT** $y_i \neq y^\star_i$.

## Solutions

### Positive values

When the faces are constrained to values between $1$ and $2N$, with $N = 8$, we
get 4 solutions:
```
================================================================
Solution 1:
Die 1: [1, 2, 2, 3, 3, 4, 4, 5]
Die 2: [1, 3, 5, 5, 7, 7, 9, 11]
================================================================
Solution 2:
Die 1: [1, 3, 3, 5, 5, 7, 7, 9]
Die 2: [1, 2, 2, 3, 5, 6, 6, 7]
================================================================
Solution 3:
Die 1: [1, 2, 3, 3, 4, 4, 5, 6]
Die 2: [1, 2, 5, 5, 6, 6, 9, 10]
================================================================
Solution 4:
Die 1: [1, 2, 3, 4, 5, 6, 7, 8]
Die 2: [1, 2, 3, 4, 5, 6, 7, 8]
```

Solution 4 is a standard D8.

### Allowing empty faces

If we allow faces with 0 dots/pips, we get 11 solutions:

```
================================================================
Solution 1:
Die 1: [0, 1, 1, 2, 2, 3, 3, 4]
Die 2: [2, 4, 6, 6, 8, 8, 10, 12]
================================================================
Solution 2:
Die 1: [1, 2, 5, 5, 6, 6, 9, 10]
Die 2: [1, 2, 3, 3, 4, 4, 5, 6]
================================================================
Solution 3:
Die 1: [0, 1, 4, 4, 5, 5, 8, 9]
Die 2: [2, 3, 4, 4, 5, 5, 6, 7]
================================================================
Solution 4:
Die 1: [2, 3, 6, 6, 7, 7, 10, 11]
Die 2: [0, 1, 2, 2, 3, 3, 4, 5]
================================================================
Solution 5:
Die 1: [0, 1, 1, 2, 4, 5, 5, 6]
Die 2: [2, 4, 4, 6, 6, 8, 8, 10]
================================================================
Solution 6:
Die 1: [2, 3, 3, 4, 6, 7, 7, 8]
Die 2: [0, 2, 2, 4, 4, 6, 6, 8]
================================================================
Solution 7:
Die 1: [1, 2, 2, 3, 5, 6, 6, 7]
Die 2: [1, 3, 3, 5, 5, 7, 7, 9]
================================================================
Solution 8:
Die 1: [2, 3, 3, 4, 4, 5, 5, 6]
Die 2: [0, 2, 4, 4, 6, 6, 8, 10]
================================================================
Solution 9:
Die 1: [1, 2, 2, 3, 3, 4, 4, 5]
Die 2: [1, 3, 5, 5, 7, 7, 9, 11]
================================================================
Solution 10:
Die 1: [2, 3, 4, 5, 6, 7, 8, 9]
Die 2: [0, 1, 2, 3, 4, 5, 6, 7]
================================================================
Solution 11:
Die 1: [1, 2, 3, 4, 5, 6, 7, 8]
Die 2: [1, 2, 3, 4, 5, 6, 7, 8]
```

### Negative values

If we allow negative values, we get infinitely many solutions.

## 6-sided dice

There are 5 6-sided dice with non-negative values:

```
================================================================
Solution 1:
Die 1: [0, 1, 1, 2, 2, 3]
Die 2: [2, 4, 5, 6, 7, 9]
================================================================
Solution 2:
Die 1: [1, 3, 4, 5, 6, 8]
Die 2: [1, 2, 2, 3, 3, 4]
================================================================
Solution 3:
Die 1: [2, 3, 3, 4, 4, 5]
Die 2: [0, 2, 3, 4, 5, 7]
================================================================
Solution 4:
Die 1: [1, 2, 3, 4, 5, 6]
Die 2: [1, 2, 3, 4, 5, 6]
================================================================
Solution 5:
Die 1: [2, 3, 4, 5, 6, 7]
Die 2: [0, 1, 2, 3, 4, 5]
```

## 10-sided dice

There are 5 10-sided dice with non-negative values:

```
================================================================
Solution 1:
Die 1: [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
Die 2: [2, 4, 6, 7, 8, 9, 10, 11, 13, 15]
================================================================
Solution 2:
Die 1: [1, 3, 5, 6, 7, 8, 9, 10, 12, 14]
Die 2: [1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
================================================================
Solution 3:
Die 1: [0, 2, 4, 5, 6, 7, 8, 9, 11, 13]
Die 2: [2, 3, 3, 4, 4, 5, 5, 6, 6, 7]
================================================================
Solution 4:
Die 1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Die 2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
================================================================
Solution 5:
Die 1: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
Die 2: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```
