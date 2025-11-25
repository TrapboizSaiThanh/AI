# solvers/bfs_solver.py

from collections import deque
from typing import List, Dict, Optional


def differ_by_one_letter(a: str, b: str) -> bool:
    """True nếu 2 từ khác đúng 1 ký tự."""
    if len(a) != len(b):
        return False
    diff = 0
    for x, y in zip(a, b):
        if x != y:
            diff += 1
            if diff > 1:
                return False
    return diff == 1


def build_graph(words: List[str]) -> Dict[str, List[str]]:
    """
    Xây đồ thị word-ladder: mỗi từ nối với các từ khác khác đúng 1 ký tự.
    Đồ thị này dùng chung cho BFS/DFS/UCS/A*.
    """
    graph: Dict[str, List[str]] = {w: [] for w in words}
    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            w1, w2 = words[i], words[j]
            if differ_by_one_letter(w1, w2):
                graph[w1].append(w2)
                graph[w2].append(w1)
    return graph


def bfs_solve(start: str, goal: str, words: List[str], graph) -> Optional[List[str]]:
    """
    Tìm đường đi ngắn nhất từ start -> goal bằng BFS (Word Ladder style).
    Trả về list các từ [start, ..., goal] hoặc None nếu không có đường.
    """
    start = start.upper()
    goal = goal.upper()
    if start not in words or goal not in words:
        raise ValueError("start và goal phải nằm trong dictionary")


    queue = deque([start])
    parent: Dict[str, Optional[str]] = {start: None}
    visited = {start}

    while queue:
        u = queue.popleft()
        if u == goal:
            # reconstruct path
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)

    return None
