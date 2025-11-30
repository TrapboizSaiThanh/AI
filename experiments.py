import time
import random
import csv
from collections import deque
from typing import Dict, List, Optional

from game.logic import load_words
from solvers.bfs_solver import build_graph
from solvers.ucs_solver import step_cost


# ======================= HELPER =======================

def filter_five_letter_words(words: List[str]) -> List[str]:
    """Chỉ lấy các từ 5 chữ cái cho graph cho đúng Word Ladder."""
    return [w.upper() for w in words if len(w) == 5]


# ======================= BFS =======================

def bfs_experiment(start: str, goal: str, graph: Dict[str, List[str]]):
    start, goal = start.upper(), goal.upper()

    queue = deque([start])
    parent = {start: None}
    visited = {start}

    expanded = 0
    peak_mem = len(queue) + len(visited)

    while queue:
        u = queue.popleft()
        expanded += 1

        if u == goal:
            path: List[str] = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path)), expanded, peak_mem

        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)

        peak_mem = max(peak_mem, len(queue) + len(visited))

    return None, expanded, peak_mem


# ======================= IDS (có limit) =======================

MAX_IDS_EXPANDED = 2000  # giới hạn số node 


def dfs_limited(u, goal, graph, depth_left, visited, path, stats):
    if stats["expanded"] >= MAX_IDS_EXPANDED:
        return False

    visited.add(u)
    path.append(u)
    stats["expanded"] += 1
    stats["peak"] = max(stats["peak"], len(visited))

    if u == goal:
        return True
    if depth_left == 0:
        path.pop()
        visited.remove(u)
        return False

    for v in graph[u]:
        if v not in visited:
            if dfs_limited(v, goal, graph, depth_left - 1, visited, path, stats):
                return True
            if stats["expanded"] >= MAX_IDS_EXPANDED:
                break

    path.pop()
    visited.remove(u)
    return False


def ids_experiment(start: str, goal: str, graph: Dict[str, List[str]], max_depth: int = 10):
    start, goal = start.upper(), goal.upper()

    total_expanded = 0
    peak_global = 0

    for depth_limit in range(1, max_depth + 1):
        visited = set()
        path: List[str] = []
        stats = {"expanded": 0, "peak": 0}

        found = dfs_limited(start, goal, graph, depth_limit, visited, path, stats)

        total_expanded += stats["expanded"]
        peak_global = max(peak_global, stats["peak"])

        if found:
            return path, total_expanded, peak_global

        if stats["expanded"] >= MAX_IDS_EXPANDED:
            break

    return None, total_expanded, peak_global


# ======================= UCS =======================

def ucs_experiment(start: str, goal: str, graph: Dict[str, List[str]]):
    import heapq

    start, goal = start.upper(), goal.upper()

    pq = [(0, start)]
    cost = {start: 0}
    parent = {start: None}

    expanded = 0
    peak_mem = len(pq) + len(cost)

    while pq:
        g, u = heapq.heappop(pq)
        expanded += 1

        if u == goal:
            path: List[str] = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path)), expanded, peak_mem

        for v in graph[u]:
            step_c = step_cost(u, v)
            new_cost = g + step_c
            if v not in cost or new_cost < cost[v]:
                cost[v] = new_cost
                parent[v] = u
                heapq.heappush(pq, (new_cost, v))

        peak_mem = max(peak_mem, len(pq) + len(cost))

    return None, expanded, peak_mem


# ======================= A*  =======================

def astar_experiment(start: str, goal: str, graph: Dict[str, List[str]]):
    """
    A* với heuristic = số ký tự khác nhau (Hamming distance).
    Trả về: (path, expanded_nodes, peak_memory)
    """
    import heapq

    start, goal = start.upper(), goal.upper()

    def h(word: str) -> int:
        return sum(1 for a, b in zip(word, goal) if a != b)

    pq = [(h(start), 0, start)]  # (f = g+h, g, node)
    g_cost = {start: 0}
    parent = {start: None}

    expanded = 0
    peak_mem = len(pq) + len(g_cost)

    while pq:
        f, g, u = heapq.heappop(pq)
        expanded += 1

        if u == goal:
            path: List[str] = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path)), expanded, peak_mem

        for v in graph[u]:
            new_g = g + 1
            if v not in g_cost or new_g < g_cost[v]:
                g_cost[v] = new_g
                parent[v] = u
                new_f = new_g + h(v)
                heapq.heappush(pq, (new_f, new_g, v))

        peak_mem = max(peak_mem, len(pq) + len(g_cost))

    return None, expanded, peak_mem


# ======================= RUN 1 CẶP =======================

def run_single_pair(start: str, goal: str, graph: Dict[str, List[str]]):
    result = {"start": start, "goal": goal}

    # BFS
    t0 = time.perf_counter()
    p, e, m = bfs_experiment(start, goal, graph)
    t1 = time.perf_counter()
    result["BFS_time_ms"] = (t1 - t0) * 1000
    result["BFS_expanded"] = e
    result["BFS_peak_mem"] = m
    result["BFS_path_len"] = len(p) if p else -1

    # IDS
    t0 = time.perf_counter()
    p, e, m = ids_experiment(start, goal, graph)
    t1 = time.perf_counter()
    result["IDS_time_ms"] = (t1 - t0) * 1000
    result["IDS_expanded"] = e
    result["IDS_peak_mem"] = m
    result["IDS_path_len"] = len(p) if p else -1

    # UCS
    t0 = time.perf_counter()
    p, e, m = ucs_experiment(start, goal, graph)
    t1 = time.perf_counter()
    result["UCS_time_ms"] = (t1 - t0) * 1000
    result["UCS_expanded"] = e
    result["UCS_peak_mem"] = m
    result["UCS_path_len"] = len(p) if p else -1

    # A*
    t0 = time.perf_counter()
    p, e, m = astar_experiment(start, goal, graph)
    t1 = time.perf_counter()
    result["Astar_time_ms"] = (t1 - t0) * 1000
    result["Astar_expanded"] = e
    result["Astar_peak_mem"] = m
    result["Astar_path_len"] = len(p) if p else -1

    return result


# ======================= MAIN =======================

def run_experiments(num_pairs: int = 10):
    print("Loading dictionary...")
    full_words = load_words("data/words.txt")
    words = filter_five_letter_words(full_words)
    print(f"Total 5-letter words: {len(words)}")

    print("Building graph...")
    graph = build_graph(words)
    print("Graph ready ✓")

    rows = []
    for i in range(num_pairs):
        start = random.choice(words)
        goal = random.choice(words)
        while goal == start:
            goal = random.choice(words)

        print(f"[{i+1}/{num_pairs}] {start} -> {goal}")
        row = run_single_pair(start, goal, graph)
        rows.append(row)

    with open("experiment_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\nDONE! Saved to experiment_results.csv")


if __name__ == "__main__":
    run_experiments(10)
