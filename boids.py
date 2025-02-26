import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd


class MazeGenerator:
    """
    Generates a perfect maze using Prim's Algorithm.
    
    Attributes:
        size (int): The size of the maze grid.
        maze (ndarray): A numpy array representing the maze, where 1 = wall and 0 = open path.
    """

    def __init__(self, size):
        """Initializes the maze with all walls."""
        self.size = size
        self.maze = np.ones((size, size))  # initialize with walls (1)

    def generate_maze(self):
        """Generates a maze using Prim's Algorithm and converts it to a grid-based structure."""
        size = self.size
        maze = np.ones((size, size))

        # start inside the maze
        start_x, start_y = 1, 1
        maze[start_x, start_y] = 0

        # initialize the frontier cells
        frontier = [(start_x + dx, start_y + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]
                    if 0 < start_x + dx < size-1 and 0 < start_y + dy < size-1]

        while frontier:
            fx, fy = random.choice(frontier)
            frontier.remove((fx, fy))

            # find neighboring visited cells
            neighbors = [(fx + dx, fy + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]
                         if 0 < fx + dx < size-1 and 0 < fy + dy < size-1 and maze[fx + dx, fy + dy] == 0]

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[fx, fy] = 0
                maze[(fx + nx) // 2, (fy + ny) // 2] = 0

                # add new frontier cells
                new_frontiers = [(fx + dx, fy + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]
                                 if 0 < fx + dx < size-1 and 0 < fy + dy < size-1 and maze[fx + dx, fy + dy] == 1]
                frontier.extend(new_frontiers)

        return maze


class BoidAgent:
    """
    Implements a Boids-based multi-agent pathfinding system.
    
    Attributes:
        position (ndarray): Current position of the agent.
        goal (ndarray): Target destination.
        velocity (ndarray): Movement velocity.
        maze (ndarray): Reference to the maze grid.
        max_speed (float): Maximum speed of the agent.
        perception_radius (int): Radius within which the agent considers nearby agents.
    """

    def __init__(self, start, goal, maze):
        """Initializes an agent with random velocity and a given start/goal position."""
        self.position = np.array(start, dtype=float)
        self.goal = np.array(goal, dtype=float)
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.maze = maze
        self.max_speed = 1.0
        self.perception_radius = 3

    def move(self, agents):
        """Applies Boids movement rules, goal-seeking, and an escape mechanism if stuck."""
        prev_position = self.position.copy()

        neighbors = [a for a in agents if np.linalg.norm(a.position - self.position) < self.perception_radius and a != self]

        alignment = self.align(neighbors) if neighbors else np.array([0, 0])
        cohesion = self.cohere(neighbors) if neighbors else np.array([0, 0])
        separation = self.adaptive_separate(neighbors) if neighbors else np.array([0, 0])
        goal_force = self.dynamic_goal_seek()
        wall_avoidance = self.avoid_walls()

        self.velocity += (
            0.6 * alignment +
            0.3 * cohesion +
            0.4 * separation +
            2.0 * goal_force +  # stronger goal-seeking force
            0.1 * wall_avoidance  # reduced wall avoidance
        )
        self.velocity = self.limit_speed(self.velocity)

        new_position = self.position + self.velocity
        if self.is_valid_move(new_position):
            self.position = new_position
        elif np.linalg.norm(self.position - prev_position) < 0.1:
            self.position += np.array([random.uniform(-1, 1), random.uniform(-1, 1)])  # escape mechanism

    def align(self, neighbors):
        """Aligns agent velocity with neighboring agents."""
        avg_velocity = np.mean([agent.velocity for agent in neighbors], axis=0)
        return avg_velocity - self.velocity if len(neighbors) > 0 else np.array([0, 0])

    def cohere(self, neighbors):
        """Moves the agent toward the center of nearby agents."""
        center_of_mass = np.mean([agent.position for agent in neighbors], axis=0)
        return (center_of_mass - self.position) * 0.05

    def adaptive_separate(self, neighbors):
        """Avoids collisions with nearby agents."""
        separation_force = np.sum([self.position - agent.position for agent in neighbors], axis=0)
        intensity = 1.5 if len(neighbors) > 3 else 0.9
        return -separation_force * intensity

    def dynamic_goal_seek(self):
        """Encourages movement toward the goal with variable intensity."""
        direction = self.goal - self.position
        distance = np.linalg.norm(direction)
        intensity = min(2.0, 1.0 + (1.5 / max(distance, 0.1)))
        return (direction / distance) * intensity if distance > 0 else np.array([0, 0])

    def avoid_walls(self):
        """Prevents agents from colliding with walls by applying a small repulsion force."""
        directions = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]
        avoidance_force = np.array([0.0, 0.0])

        for d in directions:
            check_position = self.position + d
            x, y = int(round(check_position[0])), int(round(check_position[1]))
            if 0 <= x < self.maze.shape[0] and 0 <= y < self.maze.shape[1] and self.maze[x, y] == 1:
                avoidance_force -= d * 0.3  # reduced avoidance strength

        return avoidance_force

    def is_valid_move(self, position):
        """Checks if the agent's new position is within bounds and not a wall."""
        x, y = int(round(position[0])), int(round(position[1]))
        return 0 <= x < self.maze.shape[0] and 0 <= y < self.maze.shape[1] and self.maze[x, y] == 0

    def limit_speed(self, velocity):
        """Limits the agent's speed to prevent erratic movement."""
        speed = np.linalg.norm(velocity)
        return (velocity / speed) * self.max_speed if speed > self.max_speed else velocity


maze_generator = MazeGenerator(size=15)
maze = maze_generator.generate_maze()

agents = [
    BoidAgent(start=(1, 1), goal=(13, 13), maze=maze),
    BoidAgent(start=(1, 3), goal=(13, 11), maze=maze),
    BoidAgent(start=(3, 1), goal=(11, 13), maze=maze)
]

# visualization
fig, ax = plt.subplots(figsize=(8, 8))

def update(frame):
    """Updates agent positions and redraws the maze for animation."""
    ax.clear()
    for agent in agents:
        agent.move(agents)
    ax.imshow(maze, cmap='gray', origin='upper')
    for i, agent in enumerate(agents):
        ax.plot(agent.position[1], agent.position[0], marker='o', markersize=8, label=f'Agent {i}')
    ax.legend()
    ax.set_title(f"Frame {frame}: Multi-Agent Navigation")

ani = animation.FuncAnimation(fig, update, frames=40, interval=500, repeat=False)
plt.show()
