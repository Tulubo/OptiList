# grocery-pricer
This is a simple python module that searches for the optimal amount of groceries or similar items that can be bought within a given budget by using linear programming.  
This is a very simple use of the library pyscipopt that is much more powerful than what it's used for here but it demonstrates a real life application of this problem.  


temporary list of used dependencies (will be rewritten and completed)
-
* pandas
* pyscipopt

### TODO List
- [ ] Add installation instructions (and conda env .yml file)
- [x] Have something working
- [ ] Add nicer looking visuals (output .md table, GUI(unlikely) or csv-like file)
### How to format the csv file
Here are the required columns:
- *name*: a string representing youR item'S name.
- *price*: a floating point value representing the item's monetary value.
- *min*(can be empty): the minimum quantity of items that should be bought.
- *max*(can be empty): the maximum quantity of items that should be bought.

Notes: 
- The file can contain more columns than required if it was used for other purposes, the program will simply ignore them.
- The use of floating point for the price assumes your currency has decimal parts similar to euro or dollars. If not, you will simply have to use it like an integer or convert it to a currency using this format. I would recommend conversion as a general fix but if your currency doesn't reach high values, the first solution can work.


