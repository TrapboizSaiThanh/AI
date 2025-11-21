from game.logic import load_words
from solvers.bfs_solver import bfs_solve


def main():
    dict_path = "data/words.txt"
    words = load_words(dict_path)

    start = "ARISE"
    goal = "SMART"

    path = bfs_solve(start, goal, words)
    print("BFS path:", path)


if __name__ == "__main__":
    main()
