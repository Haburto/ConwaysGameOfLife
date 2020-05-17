# ConwaysGameOfLife
A little project to try and code Conways Game of Life.

I will be using pygame!

# After the game logic was implemented
It took me longer than expected!
Between the first and last commit on day one lies a time span of about 11 hours from which about 8 hours were used on the project itself if I had to guess.

Here are some things that are noteworthy:
* Even when the rules are simple and you fully understand them, comming up with a structure and a way to handle those rules is quite hard and time consuming. (At least if you never did it before.)

* When running pygame you **NEED** to regularly check the pygame.event's with one of the 4 methods e.g. pygame.event.get()!
Otherwise your OS thinks pygame has crashed.

* I did set up a grid system with two-dimensional arrays. I achieved that in python thanks to list comprehension.

```python
# Example list comprehension:
class Cells(position):
  pass

rows = 10
columns = 15
grid = [[Cell((x, y)) for x in range(columns] for y ind range(rows)]
```
This sets up a list in a list, which can be called like this grid[y][x].  
So do not confuse the x with the y position!

Also remember when you want to change the value of the array you have to do the following:  
```python
array[0] + 1
```
instead of me begin silly and doing the following
```python 
array[0 + 1]
```
This seems obvious but when your array calls look like this it is easy to overlook that small error with a huge effect.
```python
neighbours.update([
    self.grid[position[1]-1][position[0]-1],  # top - left
    self.grid[position[1]-1][position[0]],  # top - center
    self.grid[position[1]-1][position[0]+1],  # top - right

    self.grid[position[1]][position[0]-1],  # middle - left
    self.grid[position[1]][position[0]+1],  # middle - right

    self.grid[position[1]+1][position[0]-1],  # bottom - left
    self.grid[position[1]+1][position[0]],  # bottom - center
    self.grid[position[1]+1][position[0]+1],  # bottom - right
])
```
# AFTER the project was finished
...
