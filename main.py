from game.logic import load_words, choose_secret, play_console
from game.gui_tk import run_gui


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
        run_gui(dict_path)


if __name__ == "__main__":
    main()
