# Pathfingding_Visualisation

Project to vizualize different pathfinding algorithms:
- bfs
- dfs


Using pygame to vizualise

### Demos ###

##### Recursive creation of maze: #####

![](https://github.com/EinPy/Pathfingding_Visualisation/blob/main/recursiveGrid.gif)


##### BFS exploring maze: #####

![](https://github.com/EinPy/Pathfingding_Visualisation/blob/main/bfsGrid.gif)

Nota that this maze has an unreachable area that is not possible for the bfs to reach,
no matter how it explroes the maze. 


### Algorithms ###

The first challenge is to create a maze for this program to explore. The wordy explanation
of this is to first divide the maze in two with one hole, and then repeat this for all new squares.

As seen hear breadth first search explores in all directions at the same time, while depth first search
explores in "one direction". 
