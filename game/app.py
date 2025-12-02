import os
import pickle
from game.logic import load_words, choose_secret, play_console
from game.gui_tk import run_gui
from solvers.bfs_solver import build_graph

DICT_PATH = "data/words.txt"


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


def run_app(mode="GUI"):
    words = load_words(DICT_PATH)
    if not words:
        print("Dictionary is empty or not found!")
        return

    if mode.upper() == "CONSOLE":
        secret = choose_secret(words)
        play_console(secret, words)
    else:
        graph = load_graph_cache(DICT_PATH, words)
        run_gui(words, graph)
