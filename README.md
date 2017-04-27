Sorty thing. Two parts:

Part one: tool for filling in a matrix with matchup data. 

Feed it a matrix of the form

```
[], A, B, C
A, [], [], []
B, x1, [], []
C, x2, x3, [] 
```

in CSV (name it input.csv), where A, B, and C are the names of the things you're comparing (you can, of course, have more than three), x* is some value describing the result of the comparison, and [] can be whatever you want because it'll be ignored.

Acceptable x values include: 1 to state that the row beats the column (e.g. if x1 in the above were 1, then B beats A), -1 that the column beats the row, 0 for a tie, and * (or anything you want, really) to indicate incomparability (it'll just be ignored). The program will detect empty entries (not spaces, but rather ""), and will present them to you to be filled in. Upon finishing (or quitting), the updated matrix is written to output.csv. Rename that to input.csv if you want to update it again or use it for Elo calculation.


Part two: Elo determinator

It takes the matrix of the above form from input.csv and uses the matchup data stored within to produce, using the most basic, straightforward application of the Elo formula, an Elo rating for each entry, and then writes this to ranking.csv.

Because there's only one 'game' per matchup, the order in which the matchups are run can greatly affect the end ratings. So the program runs it like 10000 times and averages the results. 

Built for the most stupid purpose, and probably of a code quality that reflects that.