# solvers/ids_solver.py

from typing import Dict, List, Optional


def ids_solve(start: str, goal: str, words: List[str], graph: Dict[str, List[str]], stop_flag=lambda: False, max_depth: int = 50):
    """
    Iterative Deepening Search (IDS) trên graph Word Ladder.
    Trả về đường đi [start, ..., goal] hoặc None.
    """ 
    start = start.upper()
    goal = goal.upper()
    if start not in words or goal not in words:
        raise ValueError("start và goal phải nằm trong dictionary")

    for depth_limit in range(1, max_depth + 1):
        if stop_flag():    
            return None
    
        print(f"[IDS] thử depth = {depth_limit}")

        visited = set()          # mỗi vòng IDS là visited mới
        path = []

        if dfs_limited(start, goal, graph, depth_limit, visited, path, stop_flag):
            return path

    return None


def dfs_limited(u, goal, graph, depth_left, visited, path, stop_flag):
    """
    DFS với giới hạn độ sâu.
    - u: node hiện tại
    - goal: node đích
    - graph: đồ thị word-ladder
    - depth_left: số bước còn lại
    - visited: tập đã thăm trong lần chạy depth hiện tại
    - path: dùng để xây dựng đường đi
    """
    if stop_flag():
        return False
    
    visited.add(u)
    path.append(u)

    if u == goal:
        return True

    if depth_left <= 0:
        path.pop()
        visited.remove(u)
        return False

    for v in graph[u]:
        if v not in visited:
            if dfs_limited(v, goal, graph, depth_left - 1, visited, path, stop_flag):
                return True

    path.pop()
    visited.remove(u)
    return False
