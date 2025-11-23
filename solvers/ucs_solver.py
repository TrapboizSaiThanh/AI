# solvers/ucs_solver.py

from heapq import heappush, heappop
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

def ucs_solve(start: str, goal: str, words: List[str]) -> Optional[List[str]]:
    """
    Tìm đường đi chi phí thấp nhất từ start -> goal bằng UCS.
    Mặc định mỗi bước cost = 1.
    Trả về list các từ [start, ..., goal] hoặc None nếu không có đường.
    """
    start = start.upper()
    goal = goal.upper()

    if start not in words or goal not in words:
        raise ValueError("start và goal phải nằm trong dictionary")

    graph = build_graph(words)

    # priority queue item: (cost, node)
    pq = []
    heappush(pq, (0, start))

    parent: Dict[str, Optional[str]] = {start: None}
    cost: Dict[str, float] = {start: 0}

    while pq:
        g, u = heappop(pq)
        # reconstruct path
        if u == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        for v in graph[u]:
            new_cost = g + 1  # step cost = 1
            if v not in cost or new_cost < cost[v]:
                cost[v] = new_cost
                parent[v] = u
                heappush(pq, (new_cost, v))

    return None