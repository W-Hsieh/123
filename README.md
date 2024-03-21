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

## Offense
For the attack agent, when it is on home side, it would first attempt to move toward the boundary. In addition, it would check whether the opponent has eaten a capsule and triggers the scared timer. If activated, the agent would avoid the observable opponent positions.

If the agent is on enemy side, the position to be avoided would be the opponent positions if the agent has not yet consumed a capsule. If the agent has eaten a capsule, it would move toward the target positions directly without avoiding the opponent ghost. The target of the attack agent would vary based on the situation. In general, the attack agent would **<ins>search for the capsule first</ins>** since it can empower the agent and become unaffected by the opponent. If there are no remaining capsules, it will **<ins>look for the next closest food</ins>**. If the agent has obtained all necessary food or the game is nearly over, it would aim for the nearest boundary position to deposit the food.

## Defense
To safeguard the food, the defend agent would never cross the border into enemy territory and will **<ins>always remain on the home side</ins>**. Therefore, it would be restricted to the boundary, and the positions to be avoided would be the boundary positions.

If an opponent has consumed a capsule and activates the scared timer, the observable opponent position would also be added to the avoid position. In general, the target of the defend agent would be the food positions on home side. Since opponents aim for the food on the home side, the defend agent would move to the food position to protect the food from being eaten.

Initially, the furthest food location is set as the target, allowing the agent to patrol and detect any opponents. If the opponent's position can be observed, it will be added to a list of target positions. Moreover, another list would **<ins>keep track of various versions of foodGrid</ins>**. This list aids in contrasting and identifying if any food gets eaten by the opponent. Although the position of the opponent can be unobservable, we can **<ins>obtain the opponent’s position indirectly</ins>** by this approach. The defend agent would then move towards the closest target position while avoiding specific positions. This strategy enables the defend agent to more precisely guard the food from being consumed.
