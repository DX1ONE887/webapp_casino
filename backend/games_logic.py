import random
import math
from typing import Any, Dict, List, Tuple

# 1. Дартс
def play_darts(force: float, angle_deg: float) -> Dict[str, Any]:
    r = max(0.0, min(1.0, force))
    theta = math.radians(angle_deg % 360)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    dist = math.hypot(x, y)
    if dist <= 0.2: score = 10
    elif dist <= 0.4: score = 9
    elif dist <= 0.6: score = 7
    elif dist <= 0.8: score = 5
    else: score = 1
    return {"x": x, "y": y, "score": score}

# 2. Мины
def init_mines(size: int, num_mines: int) -> Tuple[List[List[bool]], List[List[int]]]:
    mines = [[False]*size for _ in range(size)]
    coords = random.sample([(i, j) for i in range(size) for j in range(size)], num_mines)
    for i, j in coords: mines[i][j] = True
    counts = [[0]*size for _ in range(size)]
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for i in range(size):
        for j in range(size):
            if mines[i][j]: counts[i][j] = -1
            else:
                counts[i][j] = sum(
                    mines[i+di][j+dj] for di, dj in dirs
                    if 0 <= i+di < size and 0 <= j+dj < size
                )
    return mines, counts

def reveal_cell(mines, counts, revealed, i, j):
    if mines[i][j]: return [], False
    to_reveal, stack, visited = [], [(i, j)], set()
    while stack:
        ci, cj = stack.pop()
        if (ci, cj) in visited: continue
        visited.add((ci, cj))
        revealed[ci][cj] = True
        to_reveal.append((ci, cj, counts[ci][cj]))
        if counts[ci][cj] == 0:
            for di in (-1,0,1):
                for dj in (-1,0,1):
                    ni, nj = ci+di, cj+dj
                    if 0 <= ni < len(mines) and 0 <= nj < len(mines) and (ni, nj) not in visited:
                        stack.append((ni, nj))
    return to_reveal, True

# 3. Бросок кубика
def roll_dice(sides: int = 6) -> int:
    return random.randint(1, sides)

# 4. Колесо фортуны
def spin_wheel(segments: List[Any], spins: int = 5) -> Dict[str, Any]:
    N = len(segments)
    final_offset = random.random() * 360
    index = int(final_offset // (360 / N)) % N
    return {"result": segments[index], "angle": spins * 360 + final_offset}
