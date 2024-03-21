# Pacman Project (UoM COMP90054 Contest Project - Team 90)

The AI-related techniques that have been implemented to develop the autonomous agent teams is the ***<u>Search Algorithm (A\* Heuristic Search)***.
The technique is employed to create an agent team of attack agent and defend agent to compete against the staff teams.
The approach is systematically designed by analyzing the problem comprehensively. The advantages and challenges of the design are noted in the respective sections.
Furthermore, possible future improvements for each technique are discussed.
The performance of each technique is analyzed and evaluated by playing against the staff teams. 

 <p align="center">
    <img src="img/capture_the_flag.png" alt="Picture of Pacman board" width="600">
 </p>

# Design Choices

In order to enhance the chances of winning, it is crucial to consume food in enemy territory efficiently while also guarding the food from being eaten on home side. Thus, I have designed a team that consist of an attack agent and a defend agent to compete against the staff teams.
The main challenge lies in accurately defining the behaviors of the two agents given their distinct objectives. Additionally, it is essential to identify the position to be avoided in different situations.

### Offense
For the attack agent, when it is on home side, it would first attempt to move toward the boundary. In addition, it would check whether the opponent has eaten a capsule and triggers the scared timer. If activated, the agent would avoid the observable opponent positions.

If the agent is on enemy side, the position to be avoided would be the opponent positions if the agent has not yet consumed a capsule. If the agent has eaten a capsule, it would move toward the target positions directly without avoiding the opponent ghost. The target of the attack agent would vary based on the situation. In general, the attack agent would **<ins>search for the capsule first</ins>** since it can empower the agent and become unaffected by the opponent. If there are no remaining capsules, it will **<ins>look for the next closest food</ins>**. If the agent has obtained all necessary food or the game is nearly over, it would aim for the nearest boundary position to deposit the food.

### Defense
To safeguard the food, the defend agent would never cross the border into enemy territory and will **<ins>always remain on the home side</ins>**. Therefore, it would be restricted to the boundary, and the positions to be avoided would be the boundary positions.

If an opponent has consumed a capsule and activates the scared timer, the observable opponent position would also be added to the avoid position. In general, the target of the defend agent would be the food positions on home side. Since opponents aim for the food on the home side, the defend agent would move to the food position to protect the food from being eaten.

Initially, the furthest food location is set as the target, allowing the agent to patrol and detect any opponents. If the opponent's position can be observed, it will be added to a list of target positions. Moreover, another list would **<ins>keep track of various versions of foodGrid</ins>**. This list aids in contrasting and identifying if any food gets eaten by the opponent. Although the position of the opponent can be unobservable, we can **<ins>obtain the opponent’s position indirectly</ins>** by this approach. The defend agent would then move towards the closest target position while avoiding specific positions. This strategy enables the defend agent to more precisely guard the food from being consumed.

# Method
The AI technique employed in Method 1 is the A* Heuristic Search Algorithm. The state space of this search problem consists of the (x, y) coordinates on the map, representing the agents’ locations. The initial state of the agents would be the corner coordinates of the map since it is the starting position. As the game progresses, the agent would have various target positions. The goal state can vary depending on the current state of the game, and may include a food position, a location that contains a capsule, or a position that represents a boundary.

The transition function identifies potential next states and assesses their value by calculating the related cost. If the next location is a wall or a position to be avoided, a substantial cost would be assigned. Otherwise, the agent would transition to the next state with the corresponding cost. Lastly, the heuristic function calculates the Manhattan distance between the current state and the goal position. The agent would utilise a combination of the cost and heuristic value in order to determine and discover the subsequent node.

### Table of Contents
- [Governing Strategy Tree](#governing-strategy-tree)
  * [Motivation](#motivation)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Future improvements](#future-improvements)

### Governing Strategy Tree  

<img src="https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/31e6546a-8dee-487d-bf86-e60091a34376" width="800">

<br /><br />

<img src="https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/43fe51d0-9477-4b10-9f81-9d239a9a84f9" width="800">



### Motivation  
The motivation of this approach is to precisely calculate the cost and heuristic value in order to determine the next move for the agent. 
The main challenge lies in accurately defining the behaviors of the two agents given their distinct objectives, as well as identifying the position to be avoided in different situations. For instance, when an attack agent (without consuming a capsule) is close to an opponent on enemy territory, the algorithm should assign corresponding values to the positions near the opponent. This can be achieved by assigning larger costs to the risky locations that are closer to the opponent and lower costs as the distance increases. Consequently, the agents are able to avoid moving to the risky positions and clashing with the opponent.

In addition, the distance maintained between agents and the opponent can vary according to the game conditions. For example, when an opponent has consumed a capsule, the defender should leave space between themselves and the opponent. However, when the scared timer is about to end, the agent can move closer to the opponent and attempt to capture once the scared timer expires. Hence, the defend agent could prevent the opponent from scoring more effectively.


### Application  
To apply the motivation stated above, when the position of the opponent is observable, we can iterate over the positions that are around the opponent. As shown in the figure below, we can calculate the maze distance of each position to the location of the opponent and record three layers of positions.

We would then allocate higher value to the layer that is closer to the opponent.
- The **<ins>red layer</ins>** (distance = 1) are the closest locations to the opponent, which will be assigned with the highest cost value that is identical to the wall (i.e. 999999).
- The **<ins>yellow layer</ins>** (distance = 2) would be given a cost value of 1000, and the **<ins>green layer</ins>** (distance = 3) will be allocated with a value of 100. As a result, the agent can determine the next position based on the calculated value and maintain distance with the opponent.

For the defend agent, it would also record three layers of positions around the opponent when the opponent consume the capsule. However, when the scared timer is lower than a certain threshold, it would only avoid the positions in the red layer and move closer to the opponent. Thus, once the scared timer expires, the defending agent is better positioned to capture the opponent or interfere with the opponent's attempt to reach the boundary and score. 

<img src="https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/1b6375e1-559e-446e-8a89-51c6eeed5c09" width="600">


### Trade-offs  
#### *Advantages*  
The search algorithm is relatively straightforward to implement.
From the above applications, the designer can easily adjust the values and observe the changes that the agents made.
By thoroughly considering diverse game states, the designer can construct a robust strategy tree and hand-coded the plans for the agent to execute.
As a result, the two agents can execute their respective roles under various circumstances and achieve a decent performance against the staff team.  

#### *Disadvantages*
On the contrary, it requires the designer to comprehensively evaluate all of the potential outcomes.
Moreover, since this strategy lacks the ability to predict the movement of the opponent, certain strategy can be challenging to implement.
Hence, although this method can use hand-coded decision trees to express game-specific behaviour, it is not the ideal approach to implement as the main goal is to apply general techniques for autonomy. 

### Future improvements  
In this approach, the chooseAction function has been modified to make calculated decisions instead of picking actions at random. The agents can attain a high winning percentage against the staff team by thoroughly examined several scenarios.

However, this approach mandates the designer to set target positions manually, and it is possible that certain conditions might be overlooked.
Furthermore, this implementation lacks of predicting the moves of the opponent, making it challenging to avoid the opponent under specific circumstances.

Given these constraints, it would be advisable to employ techniques where agents can autonomously determine their actions based on learning through trial and error. The agents can deal with the trade-off between exploration and exploitation to discover better strategies over time. This way, the agent can continuously evolve with minimal manual programming.

# Evolution of the approach

### Initial Strategy

In the preliminary design, when the attack agent is on home side, the target is to simply reach the boundary.
However, after testing on the server, it can be observed that certain staff team is designed to wait on the border and capture our attack agent.
Thus, when the attack agent is moving toward the boundary, it should look for the locations of the observable opponents.

![c1a7f4c9-678a-49ca-9150-baad2474d1a9](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/1c79c11d-02e3-41f2-9c2b-e7975991b944)

In addition, the position to be avoided was set to be the exact location of the opponent in the initial implementation. Nevertheless, since the opponent is moving dynamically, it is likely that our agent will still run into the opponent even with this strategy in place. Hence, the agent should also record the surrounding locations and prevent clashing with the opponent.

![e3549297-3247-4632-a4c6-be8f3e4e6b34](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/e66fcb4f-6ff3-487e-a8a5-d41a9cd4069e)


#### Competition results: Games - 18-1-21 | Percentile - 45%

![18](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/1f5215b8-0f8c-4c88-ae5d-db4b380bff33)



### Revised Strategy

When an attack agent is moving toward the boundary, it would iterate over the opponent indices to see if there is an observable opponent in enemy territory. If so, it would change the entering position to avoid directly clashing with the opponent.

![5b37fc96-107f-4775-83e5-aca565ab4a46](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/16518df5-0c70-4c06-9ef1-142f66aa740f)

Due to the opponent's dynamic movement, it would be ideal to record proximity locations of the opponent instead of just the exact position of the opponent.
When the position of the opponent is observable, the agent will record three layers of locations and allocate the respective cost values in these locations as stated in the [previous section](AI-Method-1#Application).

For the defend agent, it would mark three layers of surrounding positions and maintain distance with opponent when the opponent has consumed a capsule.
However, it would only steer clear of the positions in the red layer when the scared timer is about to expire. As a result, the defend agent can more efficiently deter the opponent from scoring by implementing this strategy.

![f9496f1e-0b8c-4fb5-b51a-df6cf35f8456](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/1108dfb8-2870-4adb-8126-5863a069f533)

#### Competition results: Games - 27-1-21 | Percentile - 67.5%

![27](https://github.com/COMP90054-2023s2/a3-team90/assets/142127312/af7840c1-c1a4-46b6-818d-a15eb3b4cefd)


#### Strategy summary

- Check opponent position when crossing boundary.

- Record the surrounding locations of the opponent (i.e. three layers of positions) and allocate corresponding cost values.

- For defend agent, adjust the distance maintained with the opponent to capture the opponent more effectively.


# Conclusions and Reflections

### Challenges  

- **Limitation**: Given that this method cannot anticipate the opponent's movements, executing certain strategies can be challenging. For example, entering a dead end can be risky, especially when the agent is chased by the opponent. Because this approach doesn't predict or identify patterns in the opponent's movements, the agent might inadvertently end up in a dead end and get caught by the opponent.

- **Requires Thorough Consideration**: The method requires the designer consider thoroughly and manually set target positions. There is a chance that certain conditions might be neglected. Much of the progress in this approach came from analyzing the replays and seeking for solutions. However, this approach may not be effective due to the fact that many perspectives may still be overlooked.

### Conclusions and Learnings
Implementing the A* Heuristic Search method is relatively straightforward. The designer is able to readily modify the values and observe the adjustments made by the agents. By thoroughly analyzing various scenarios, the designer can construct a robust strategy tree, and the agents may achieve a decent winning percentage against the staff team. However, it requires the designer to hand-code the plans for the agents to execute. It is likely that certain conditions may be neglected, and the plans could be suboptimal. As a result, it would be ideal to employ techniques where agents can autonomously determine their actions based on learnings, and apply general techniques for autonomy.
