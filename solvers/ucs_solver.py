# solvers/ucs_solver.py

from heapq import heappush, heappop
from typing import List, Dict, Optional


def ucs_solve(start: str, goal: str, words: List[str], graph) -> Optional[List[str]]:
    """
    Tìm đường đi chi phí thấp nhất từ start -> goal bằng UCS.
    Mặc định mỗi bước cost = 1.
    Trả về list các từ [start, ..., goal] hoặc None nếu không có đường.
    """
    start = start.upper()
    goal = goal.upper()

    if start not in words or goal not in words:
        raise ValueError("start và goal phải nằm trong dictionary")


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