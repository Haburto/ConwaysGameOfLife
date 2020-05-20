# ConwaysGameOfLife
**EDIT:**
There seems to be a bug with the game logic which I just found as I started my next project. Not sure if I am going to fix it, if I do, I will delete this edit again.

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
The game logic was definitely the hardest part.
A few things I learned in this project were, that method-calls get cluttered very easily if you pass through everything. I were able to solve this problem with an gameInitialization object which I could easily pass through the methods without getting them too long.
With this approach I also had one central place in which I can acces game options like window size and the colours.  

Also having two 'loops' for the game did help with the response time. I am using the ```pygame.time.wait(x)``` method to wait x ms at every start of the loop. (The loop runs as long as the ```game_init.exit_program``` flag is False.)  
When the ```game_init.game_started``` flag is set a counter counts + 1 until it reaches the number y and only after that the game logic is called and then everything begins anew.  
That way I can accept an input every 5 ms wether it is just moving the window or closing the game itself. And all this time my game is not sped up.  
I think that is the right apporach.  

The only thing that is left to do now is to look at all the TODO's and (If I feel like it) do those things as well as cleaing up the code.

# Things I learned while working on clearing my TODO's
First of all I should probably start using mehtod and class descriptions.
```python
class myClass(object):
"""This is my class!"""
  def my_function(self):
  """This is my function..."""
    pass
```
This will help to stay on top of bigger projects.
I also should start to split the content of those projects into several files (but this can wait until my programs have way more code).

## 1. Getters and Setters
The first of my TODO's brings up the questions if getter and setters are used in python.  
Setters and getters are the result of data encapsulation in OOP. Altough data encapsulation can be achieved in python (sort of) it usually is not used that often as in other languages (at least not in the code I read and wrote).  
But there are other benefits to using getters and setters, for example the ability to correct the values that the user of the method want to set to a specific attribute. And there are also two (pythonic) ways of achieving the desired functionality.  

The first way is to use decorators and the second way is to use the property class. Both of them are basically the same. I think the decorator approach is a more pythonic way but I am not certain.  

**decorator**
```python
class MyClass(object):
  def __init__(self):
    self.x = None  # self._x = None
    
  @property
  def x(self):
    """This is the x property."""
    return self.x  # return self._x
    
  @x.setter
  def x(self, new_x):
    self.x = new_x  # self._x = new_x
    
  @x.deleter
  def x(self):
    del self.x  # del self._x
```
**property class**
```python
# You can use _ or __ infront of all getter/setters for data encapsulation, but I will not do that here
class MyClass(objecet):
  def __init__(self):
    self.x = None
    
  def get_x(self):
    return self.x
    
  def set_x(self, new_x):
    self.x = new_x
    
  def del_x(self):
    del self.x
    
  x = property(get_x, set_x, del_x, "This is the x property.")
```
```python
 # You could also do the following, at the end of the methods or under each specific method...
 x = property(get_x, doc="This is the x property.")
 x = x.setter(set_x)
 x = x.deleter(del_x)
```
So just create your class without the getter and setters and if you feel the need to make use of them or even leave out some variables (for example a Money class used to use euroes and cents but now switches to only use cents and calculate the euro value) you can use those two ways to get the functionality without breaking or rewriting the code.

## 2. ```def __init__(self): ...```
I wondered wether or not a __init__ should be always present or not. The answer is no. If it is not needed, then you can leave it out. I should have known that, because of the guidlines number 1 and 3 in the zen of python!
```python
import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
# ...
```
