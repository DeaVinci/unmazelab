from heapq import heappop, heappush
from typing import List, Tuple, Dict, Optional
import time

class Node:
    def __init__(self, x: int, y: int, priority: int):
        self.x = x
        self.y = y
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def find_path_a_star(vertical_walls: List[List[int]], horizontal_walls: List[List[int]], rows: int, cols: int, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
    open_set = []
    heappush(open_set, Node(start_x, start_y, 0))

    costs: Dict[str, int] = {hash_position(start_x, start_y): 0}
    predecessors: Dict[str, Optional[Tuple[int, int]]] = {hash_position(start_x, start_y): None}

    while open_set:
        current = heappop(open_set)

        if current.x == end_x and current.y == end_y:
            path = []
            position = (current.x, current.y)

            while position is not None:
                path.append(position)
                position = predecessors[hash_position(*position)]
            path.reverse()
            return path

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor_x = current.x + dx
            neighbor_y = current.y + dy

            if neighbor_x < 0 or neighbor_y < 0 or neighbor_x >= rows or neighbor_y >= cols:
                continue

            #Prawo
            if dx == 0 and dy == 1 and neighbor_y > 0 and vertical_walls[current.x][current.y] == 1:
                continue
            #Lewo 
            if dx == 0 and dy == -1 and current.y > 0 and vertical_walls[current.x][current.y - 1] == 1:
                continue
            #Dół
            if dx == 1 and dy == 0 and neighbor_x > 0 and horizontal_walls[current.x][current.y] == 1:
                continue
            #Góra
            if dx == -1 and dy == 0 and current.x > 0 and horizontal_walls[current.x - 1][current.y] == 1:
                continue

            new_cost = costs[hash_position(current.x, current.y)] + 1

            if hash_position(neighbor_x, neighbor_y) not in costs or new_cost < costs[hash_position(neighbor_x, neighbor_y)]:
                costs[hash_position(neighbor_x, neighbor_y)] = new_cost
                heuristic = abs(neighbor_x - end_x) + abs(neighbor_y - end_y)
                priority = new_cost + heuristic
                heappush(open_set, Node(neighbor_x, neighbor_y, priority))
                predecessors[hash_position(neighbor_x, neighbor_y)] = (current.x, current.y)

    return []

def hash_position(x: int, y: int) -> str:
    return f"{x},{y}"

if __name__ == "__main__":
    try:
        rows = int(input())
        cols = int(input())
        start_x = int(input())
        start_y = int(input())
        end_x = int(input())
        end_y = int(input())

        vertical_walls = []
        for _ in range(rows):
            vertical_walls.append([int(input()) for _ in range(cols - 1)])

        horizontal_walls = []
        for _ in range(rows - 1):
            horizontal_walls.append([int(input()) for _ in range(cols)])

        start_time = time.time()
        path = find_path_a_star(vertical_walls, horizontal_walls, rows, cols, start_x, start_y, end_x, end_y)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_final = int(execution_time * 1_000_000)

        if path:
            print(execution_time_final)
            for cell in path:
                print(cell[0])
                print(cell[1])
    except Exception as e:
        raise RuntimeError(e)
