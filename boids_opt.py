import random
import heapq
import pygame
import sys

class Agent:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.steps_taken = 0
        self.path = []

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def move(self, maze):
        # Check if the current position is still valid
        if maze[self.y][self.x] == 1:
            ### DEBUGGING
            print(f"Agent is on a wall at ({self.x}, {self.y}). Replanning path.")
            self.replan_path(maze)
            return

        # Replan if no path or current position is invalid
        if not self.path or maze[self.y][self.x] == 1:
            self.replan_path(maze)

        # Move along the path
        if self.path:
            next_x, next_y = self.path.pop(0)
            self.x, self.y = next_x, next_y
            self.steps_taken += 1

    def replan_path(self, maze):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (self.x, self.y)
        goal = self.target

        # Check if the target is reachable
        if maze[goal[1]][goal[0]] == 1:
            ### DEBUGGING
            print(f"Target {goal} is unreachable (it's a wall).")
            self.path = []  # Clear the path to avoid errors
            return

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_cell = (current[0] + dx, current[1] + dy)
                if 0 <= next_cell[0] < len(maze[0]) and 0 <= next_cell[1] < len(maze) and maze[next_cell[1]][next_cell[0]] == 0:
                    new_cost = cost_so_far[current] + 1
                    if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                        cost_so_far[next_cell] = new_cost
                        priority = new_cost + heuristic(goal, next_cell)
                        heapq.heappush(frontier, (priority, next_cell))
                        came_from[next_cell] = current

        # If the goal was not reached, clear the path
        if goal not in came_from:
            ### DEBUGGING
            print(f"No path found to target {goal}.")
            self.path = []
            return

        # Reconstruct the path
        self.path = []
        current = goal
        try:
            while current != start:
                self.path.append(current)
                current = came_from[current]
            self.path.reverse()
        except KeyError as e:
            ### DEBUGGING
            print(f"Pathfinding error: {e}. No valid path found.")
            self.path = []  # Clear the path to avoid errors


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        stack = [(0, 0)]
        maze[0][0] = 0

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and maze[ny][nx] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        return maze

    def update_maze(self, maze):
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.05:  # 5% chance to toggle a wall
                    maze[y][x] = 1 - maze[y][x]


class Visualization:
    def __init__(self, maze, agents, cell_size):
        self.maze = maze
        self.agents = agents
        self.cell_size = cell_size
        self.width = len(maze[0]) * cell_size
        self.height = len(maze) * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.colors = {
            "wall": (0, 0, 0),
            "path": (255, 255, 255),
            "agent": (255, 0, 0),
        }

    def draw(self, maze, agents):
        self.screen.fill(self.colors["path"])
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(self.screen, self.colors["wall"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        for agent in agents:
            pygame.draw.circle(self.screen, self.colors["agent"], (agent.x * self.cell_size + self.cell_size // 2, agent.y * self.cell_size + self.cell_size // 2), self.cell_size // 3)

        pygame.display.flip()


class SwarmIntelligence:
    def __init__(self, maze, num_agents):
        self.agents = []
        for _ in range(num_agents):
            while True:
                x, y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
                if maze[y][x] == 0:
                    break
            while True:
                target = (random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1))
                if maze[target[1]][target[0]] == 0:
                    break
            self.agents.append(Agent(x, y, target))

    def update_agents(self, maze):
        # Sort agents by distance to target (closest first)
        self.agents.sort(key=lambda agent: agent.manhattan_distance((agent.x, agent.y), agent.target))

        for agent in self.agents:
            agent.move(maze)
            self.avoid_collisions(agent, maze)

    def avoid_collisions(self, agent, maze):
        for other_agent in self.agents:
            if other_agent != agent and (agent.x, agent.y) == (other_agent.x, other_agent.y):
                neighbors = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = agent.x + dx, agent.y + dy
                    if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                        neighbors.append((nx, ny))
                if neighbors:
                    # Move to the neighbor closest to the target
                    best_neighbor = min(neighbors, key=lambda pos: agent.manhattan_distance(pos, agent.target))
                    agent.x, agent.y = best_neighbor


class PerformanceMetrics:
    def __init__(self, agents):
        self.agents = agents
        self.total_path_cost = 0
        self.total_collisions = 0
        self.steps_to_completion = 0
        self.replanning_count = 0  # Track how often agents replan paths

    def update(self):
        self.steps_to_completion += 1
        self.total_path_cost = sum(agent.steps_taken for agent in self.agents)
        self.total_collisions += self.count_collisions()
        self.replanning_count = sum(1 for agent in self.agents if not agent.path)  # Count agents replanning

    def count_collisions(self):
        positions = [(agent.x, agent.y) for agent in self.agents]
        return len(positions) - len(set(positions))

    def print_metrics(self):
        print(f"Total Path Cost: {self.total_path_cost}")
        print(f"Total Collisions: {self.total_collisions}")
        print(f"Steps to Completion: {self.steps_to_completion}")
        print(f"Replanning Count: {self.replanning_count}")
        print("------")


def all_agents_at_target(agents):
    return all((agent.x, agent.y) == agent.target for agent in agents)


def main():
    pygame.init()
    width, height = 20, 20
    cell_size = 30
    maze_generator = MazeGenerator(width, height)
    maze = maze_generator.generate_maze()
    num_agents = 5
    swarm = SwarmIntelligence(maze, num_agents)
    visualization = Visualization(maze, swarm.agents, cell_size)
    metrics = PerformanceMetrics(swarm.agents)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        maze_generator.update_maze(maze)
        swarm.update_agents(maze)
        metrics.update()
        visualization.draw(maze, swarm.agents)

        if metrics.steps_to_completion % 10 == 0:
            metrics.print_metrics()

        if all_agents_at_target(swarm.agents):
            print("All agents reached their targets!")
            running = False

        pygame.time.delay(100)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()