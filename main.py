import os
import pickle
from collections import deque
from game.logic import load_words, choose_secret, play_console
from game.gui_tk import run_gui
from solvers.bfs_solver import build_graph, bfs_solve
from solvers.dfs_solver import ids_solve

def load_graph_cache(dict_path, words):
    cache_file = dict_path.replace(".txt", "_graph.pkl")

    if os.path.exists(cache_file):
        print("Loading graph cache...")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    print("Building graph (first time)...")
    graph = build_graph(words)

    with open(cache_file, "wb") as f:
        pickle.dump(graph, f)

    return graph

def main():
    dict_path = "data/words.txt"

    MODE = "GUI"

    if MODE == "CONSOLE":
        words = load_words(dict_path)
        if not words:
            print("Dictionary is empty or not found!")
            return
        secret = choose_secret(words)
        play_console(secret, words)
    else:
        words = load_words(dict_path)
        graph = load_graph_cache(dict_path, words)
        run_gui(words, graph)
    # words = load_words(dict_path)
    # graph = load_graph_cache(dict_path, words)
    # print(bfs_solve("FOSSA", "DERNS", words, graph))
    

if __name__ == "__main__":
    main()
