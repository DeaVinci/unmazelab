from typing import List, Tuple
import time

def find_path_dfs(vertical_walls: List[List[int]], horizontal_walls: List[List[int]], rows: int, cols: int, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
    shortest_path = []
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    current_path = []
    min_steps = [float('inf')]

    def dfs(x: int, y: int, steps: int):
        if x < 0 or y < 0 or x >= rows or y >= cols or visited[x][y]:
            return

        if x == end_x and y == end_y:
            if steps < min_steps[0]:
                min_steps[0] = steps
                shortest_path.clear()
                shortest_path.extend(current_path)
                shortest_path.append((x, y))
            return

        visited[x][y] = True
        current_path.append((x, y))

        #Prawo
        if y < cols - 1 and vertical_walls[x][y] == 0:
            dfs(x, y + 1, steps + 1)
        #Lewo
        if y > 0 and vertical_walls[x][y - 1] == 0:
            dfs(x, y - 1, steps + 1)
        #Dół
        if x < rows - 1 and horizontal_walls[x][y] == 0:
            dfs(x + 1, y, steps + 1)
        #Góra
        if x > 0 and horizontal_walls[x - 1][y] == 0:
            dfs(x - 1, y, steps + 1)

        visited[x][y] = False
        current_path.pop()

    dfs(start_x, start_y, 0)
    return shortest_path

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
        path = find_path_dfs(vertical_walls, horizontal_walls, rows, cols, start_x, start_y, end_x, end_y)
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
