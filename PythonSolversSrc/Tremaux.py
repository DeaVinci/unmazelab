from typing import List, Tuple
import time

def find_path_tremaux(vertical_walls: List[List[int]], horizontal_walls: List[List[int]], rows: int, cols: int, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
    stack = []
    visited_count = {}
    position = (start_x, start_y)
    
    while position != (end_x, end_y):
        pos_key = hash_position(position)
        visited_count[pos_key] = visited_count.get(pos_key, 0) + 1

        neighbors = find_neighbors(position, vertical_walls, horizontal_walls, rows, cols)

        
        new_neighbors = [neighbor for neighbor in neighbors if visited_count.get(hash_position(neighbor), 0) == 0]

        if new_neighbors:
            stack.append(position)
            position = new_neighbors[0]
        else:
            if stack:
                position = stack.pop()
            else:
                return []

    
    path = stack + [position]
    return path

def find_neighbors(position: Tuple[int, int], vertical_walls: List[List[int]], horizontal_walls: List[List[int]], rows: int, cols: int) -> List[Tuple[int, int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    x, y = position

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            #Prawo
            if dx == 0 and dy == 1 and ny > 0 and vertical_walls[x][y] == 1:
                continue
            #Lewo
            if dx == 0 and dy == -1 and y > 0 and vertical_walls[x][y - 1] == 1:
                continue
            #Dół
            if dx == 1 and dy == 0 and nx > 0 and horizontal_walls[x][y] == 1:
                continue
            #Góra
            if dx == -1 and dy == 0 and x > 0 and horizontal_walls[x - 1][y] == 1:
                continue

            neighbors.append((nx, ny))

    return neighbors

def hash_position(position: Tuple[int, int]) -> str:
    return f"{position[0]},{position[1]}"

if __name__ == "__main__":
    try:
        rows = int(input())
        cols = int(input())
        start_x = int(input())
        start_y = int(input())
        end_x = int(input())
        end_y = int(input())

        vertical_walls = []
        for i in range(rows):
            vertical_walls.append([int(input()) for _ in range(cols - 1)])

        horizontal_walls = []
        for i in range(rows - 1):
            horizontal_walls.append([int(input()) for _ in range(cols)])

        start_time = time.time()
        path = find_path_tremaux(vertical_walls, horizontal_walls, rows, cols, start_x, start_y, end_x, end_y)
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
