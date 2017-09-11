## Research Review -- AI and Planning 

The official birth of the field of Artificial Intelligence (AI)  is generally considered to be 1956 at a workshop organized by John McCarthy at the Dartmouth Summer Research Project [1]. The goal was to investigate ways and means in which machines could be made to simulate aspects of intelligence. Indeed, McCarthy is credited with coining the term "artificial intelligence" in his proposal co-authored with Marvin Minsky, Nathaniel Rochester and Claude Shannon (himself the father of _Information Theory_)[2]. 

Although the workshop created a unified identity for the field, many ideas of AI have been around for generations. In the 18th century, Thomas Bayes provided a framework for reasoning about probability of events. In the 19th century, George Boole showed that  **logical reasoning**, dating back to Aristotle, could be used for solving equations. In the 20th century, Shannon himself combined binary arithmetic, statistics and Boolean algebra to solve the simplification of telephone switching circuits, and created the field of **Information Theory** and derived a rigorous mathematical theory of communications. His use of binary logic created the field of digital computers, extending the ideas of Alan Turing and John Von Neumann. Digital computers themselves revolutionized research in the field of AI, feeding the virtuous cycles that continue today. 

### Historical Perspective

![Claude Shannon and wife Betty](https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/pete/php65GpYz.png)

Claude Shannon, an avid chess player and an inveterate tinkerer, built himself a chess-playing machine he called _Endgame_ or _Caissac_ (after the fictional “patron goddess of chess,” Caïssa)[3][4]. Shannon's machine could only handle endgames, managing about six pieces at a time. The machine had roughly 150 relay switches, and could decide a move in about 10-15 seconds. The relays were concealed in a box decorated with the pattern of a chess board, and would light up when it was ready to signal a move. Chess, the classic game of strategy, intelligence and planning, was considered a challenge for any automaton, and Shannon's contributions to the field of AI in general and _planning_ in particular are evident. Shannon's chess-playing machine could be considered the "father" of many game-playing machines. Several AI researchers spent their careers inventing new ways for machines to play chess and defeat humans. Finally the breakthrough came with IBM's Deep Blue [5] which defeated reigning champion Garry Kasparov. This victory, though largely symbolic, showed just how far computers had come in becoming artificially intelligent, and in particular crystallized the win of _Search and Planning_ algorithms.

### Search and Planning

Search and planning deal with reasoning about goal-directed behavior. Search plays a key role in determining, for example, which game moves (behavior) will lead to a win (goal).

In 1971, Fikes and Nilsson developed **STRIPS** (Stanford Research Institute Problem Solver), a problem solver for their robot named "Shakey", one of the first general purpose robots. STRIPS was written in LISP, and was designed as a state-space search system to search for goal. It was used as a planning tool for the Shakey robot[6]. Shakey was the first goal-oriented robot  that moved from one room to another, turning light switches on or off, opening and closing doors, climbing up and down rigid surfaces, and pushed movable objects around. STRIPS was used for planning Shakey's actions, even though Shakey itself wasn't capable of performing all actions.  

Shakey's impact in AI and robotics is immense: it resuled in advancing the field of **path planning**, and particularly in the development of A-* search. Also notably, the representation language used for STRIPS resulted in the development of _Problem Domain Description Language (PDDL)_.

### Mobile Robots and Probabilistic Planning

Mobile robots move about in their environment using wheels, legs or similar mechanisms, sense their environments and perform some tasks. As robots, they perform tasks by sensing and manipulating the physical world. Typically, sensors on robots sense the environment and actuators (or effectors) manipulate the physical world. 

Before the robots can perform their tasks, they have to plan their movement. The subfield of planning is key in robotic motion planning. While deterministic motions and plans are good for classical planning, they often do not work for robotic motions as the environment is often probabilistic, with obstacles changing location dynamically (as, for example, pedestrians or cars on a road). Here, instead of classical planning, _probabilistic planning_ becomes important. 

A key development in planning was probabilistic planning using Monte Carlo Localization to estimate a robot's location using random sampling to represent a robot's belief state[7] that allowed for a much faster and computationally efficient estimation. This technique is used in most robots today, including the Roomba vacuum cleaning robot, the DARPA Grand Challenge winner "Stanley", and many others. 

### Stanley

In 2004, Sebastian Thrun and his team at Stanford's AI Lab created "Stanley", a self-driving car that won DARPA's 2005 Grand Challenge, by driving autonomously, the first car to do so. It did so using a combination of LIDARs, cameras and GPS, to build a 3D representation of the real-world and using probabilistic reasoning and machine learning to detect obstacles and path planning [8].

Stanley's challenge was crossing a piece of desert, the exact coordinates of which were kept secret until 2 hours before the challenge. The road coordinates were specified as a set of waypoints, as a result, global path planning was not the key objective per se. The path planner's goal was obstacle avoidance. Stanley performed path planning by probabilistically generating trajectories, and implementing a road-centering heuristic to stay in between lane boundaries and staying on track. It uses a path smoother that smoothens out the path. 

![Stanley](https://upload.wikimedia.org/wikipedia/commons/3/3e/Stanley2.JPG)

The path-planner is implemented as a search algorithm (using **hybrid A-star** approach), that generates trajectories using a linear combination of several cost functions. These cost functions seek to minimize costs of severe jerk while in motion, constraints like maximum lateral acceleration (to prevent fishtailing), maximum steering angle and maximum acceleration/deceleration. The cost functions penalize running over obstacles, leaving the waypoints, etc. Upon generating several possible trajectories, the planner chooses a single best trajectory, and passes it on to the controller to execute the planned motion. This plan is repeated until Stanley reaches its goal.


## Impact 

The impact of search and planning algorithms is hard to overstate. Today in 2017, nearly all robots use some search and planning as basis of their operation. An entire industry of Self-Driving Autonomous Vehicles uses the fruits of the labor of AI scientists, researchers and engineers that developed ever more useful algorithms.

---

References:

[1] "A Short History of AI", https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai  

[2] J. McCarthy, Marvin L. Minsky, Nathaniel Rochester, and Claude E. Shannon, "A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence," August 31, 1955, http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html

[3] C. Shannon, "A Chess Playing Machine", Scientific American, Feb 1950, https://link.springer.com/chapter/10.1007/978-1-4613-8716-9_6

[4] R. Goodman and J. Soni, "The Man Who Built The Chess Machine", https://www.chess.com/article/view/the-man-who-built-the-chess-machine

[5] IBM Deep Blue, https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer) 

[6] Shakey the robot, https://en.wikipedia.org/wiki/Shakey_the_robot 

[7] Monte Carlo Localization, Fox, et. al, http://robots.stanford.edu/papers/fox.aaai99.pdf

[8] Thrun, et. al, "Stanley: The Robot That Won the DARPA Grand Challenge", http://isl.ecst.csuchico.edu/DOCS/darpa2005/DARPA%202005%20Stanley.pdf


