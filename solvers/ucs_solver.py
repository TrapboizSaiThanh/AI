# solvers/ucs_solver.py

from heapq import heappush, heappop
from typing import List, Dict, Optional

letter_freq_cost = {
    'E': 1, 
    
    'A': 2, 'R': 2, 'I': 2, 'O': 2, 'T': 2, 'N': 2, 'S': 2, 'L': 2,

    'C': 3, 'U': 3, 'D': 3, 'P': 3, 'M': 3, 'H': 3,

    'G': 4, 'B': 4, 'F': 4, 'Y': 4, 'W': 4,

    'K': 5, 'V': 5, 'X': 5, 'Z': 5, 'J': 5, 'Q': 5,
}

def step_cost(from_word: str, to_word: str) -> int:
    """Cost = frequency score of the changed letter."""
    for a, b in zip(from_word, to_word):
        if a != b:
            return letter_freq_cost[b]  # cost depends on new letter
    return 1


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
            step_c = step_cost(u, v)
            new_cost = g + step_c  # step cost = 1
            if v not in cost or new_cost < cost[v]:
                cost[v] = new_cost
                parent[v] = u
                heappush(pq, (new_cost, v))

    return None