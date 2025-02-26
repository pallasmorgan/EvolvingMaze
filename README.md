# Dynamic-Multi-Agent-Pathfinding-in-an-Evolving-Maze-with-Swarm-Intelligence
Principles of AI: Midterm Project


### Jack
I used Team Member 1 (Aylene)’s Prim’s Algorithm for maze generation but had to make several adjustments to integrate it with my system. Her original implementation relied on an adjacency matrix, which wasn’t compatible with my grid-based approach, so I converted it into a numpy array, where walls = 1 and open paths = 0. I also ensured that agents had valid pathways between their start and goal positions, fixing indexing issues that initially blocked movement. The core logic of her algorithm remains, but I optimized it for real-time navigation and dynamic updates to work more seamlessly with my implementation.

My algorithm is a multi-agent pathfinding system built on Boids-based swarm intelligence, designed to navigate a dynamically generated maze in real-time. I started with Aylene’s Prim’s Algorithm for maze generation but needed to convert it into a grid-based structure for reasons previously covered. The core of my approach was designing agents that follow simple yet effective movement rules: alignment (staying in sync with nearby agents), cohesion (moving toward the group’s center), separation (avoiding collisions), goal-seeking (prioritizing movement toward the target), and wall avoidance (preventing dead ends).

Early tests showed that agents were too hesitant to move, so I reduced wall avoidance strength, increased goal-seeking force, and added an escape mechanism to prevent them from getting stuck. Performance evaluations confirmed these fixes, with agents reaching their goals 99.33% of the time while maintaining efficient execution speed. The final system is scalable, adaptive, and highly efficient, successfully handling multiple agents in changing environments without pre-planned paths.
