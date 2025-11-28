from heapq import heappush, heappop
from typing import List, Dict, Optional

def heuristic(word: str, goal: str) -> int:
    """Số ký tự khác nhau giữa word và goal (Hamming distance)."""
    return sum(c1 != c2 for c1, c2 in zip(word, goal))


def astar_solve(start: str, goal: str, words: List[str], graph) -> Optional[List[str]]:
    """
    Tìm đường đi ngắn nhất từ start -> goal bằng A* search.
    f = g + h
    Mỗi bước cost = 1.
    """
    start = start.upper()
    goal = goal.upper()

    if start not in words or goal not in words:
        raise ValueError("start và goal phải nằm trong dictionary")

    # priority queue item: (f, g, node)
    pq = []
    h0 = heuristic(start, goal)
    heappush(pq, (h0, 0, start))

    parent: Dict[str, Optional[str]] = {start: None}
    g_cost: Dict[str, float] = {start: 0}

    while pq:
        f, g, u = heappop(pq)

        if u == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]

        for v in graph[u]:
            new_g = g + 1
            if v not in g_cost or new_g < g_cost[v]:
                g_cost[v] = new_g
                parent[v] = u

                f_new = new_g + heuristic(v, goal)
                heappush(pq, (f_new, new_g, v))

    return None
