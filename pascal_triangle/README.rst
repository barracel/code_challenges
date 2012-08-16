===============
Pascal Triangle
===============

Write a method that outputs the first N+1 lines of Pascal's Triangle.

printPascal(4) should give this output::

   0 1
   1 1 1
   2 1 2 1
   3 1 3 3 1
   4 1 4 6 4 1
   5 1 5 10 10 5 1

E(i, j) = E(i-1, j-1) + E(i-1, j)
