# game/gui_tk.py

import tkinter as tk
from tkinter import messagebox
from typing import List

from .logic import load_words, choose_secret, check_guess, is_valid_guess


MAX_ATTEMPTS = 6
WORD_LENGTH = 5

# Màu giống Wordle gốc
COLOR_BG = "#121213"
COLOR_EMPTY = "#3a3a3c"
COLOR_GREEN = "#6aaa64"
COLOR_YELLOW = "#c9b458"
COLOR_GRAY = "#787c7e"
COLOR_TEXT = "#ffffff"


class WordleGUI:
    def __init__(self, root: tk.Tk, words: List[str]):
        self.root = root
        self.words = words
        self.secret = choose_secret(words)
        self.current_row = 0
        self.game_over = False

        self.root.title("Wordle – Python Version")
        self.root.configure(bg=COLOR_BG)

        # Debug cho dễ test – muốn ẩn thì comment dòng dưới
        print(f"(DEBUG) Secret word is: {self.secret}")

        self._build_board()
        self._build_input_area()

    def _build_board(self):
        """Tạo lưới 6x5 bằng Label."""
        self.cells = []

        board_frame = tk.Frame(self.root, bg=COLOR_BG)
        board_frame.pack(pady=20)

        for r in range(MAX_ATTEMPTS):
            row_cells = []
            for c in range(WORD_LENGTH):
                lbl = tk.Label(
                    board_frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Helvetica", 18, "bold"),
                    bg=COLOR_EMPTY,
                    fg=COLOR_TEXT,
                    relief="ridge",
                    bd=2,
                )
                lbl.grid(row=r, column=c, padx=4, pady=4)
                row_cells.append(lbl)
            self.cells.append(row_cells)

    def _build_input_area(self):
        """Ô nhập từ + nút Submit + nút Restart."""
        input_frame = tk.Frame(self.root, bg=COLOR_BG)
        input_frame.pack(pady=10)

        self.entry = tk.Entry(
            input_frame,
            width=10,
            font=("Helvetica", 16),
            justify="center",
        )
        self.entry.grid(row=0, column=0, padx=5)
        self.entry.focus_set()

        submit_btn = tk.Button(
            input_frame,
            text="Guess",
            font=("Helvetica", 12, "bold"),
            command=self.on_submit,
        )
        submit_btn.grid(row=0, column=1, padx=5)

        restart_btn = tk.Button(
            input_frame,
            text="Restart",
            font=("Helvetica", 12),
            command=self.restart_game,
        )
        restart_btn.grid(row=0, column=2, padx=5)

        # Enter = submit
        self.root.bind("<Return>", lambda event: self.on_submit())

    def restart_game(self):
        """Reset toàn bộ board + chọn secret mới."""
        self.secret = choose_secret(self.words)
        self.current_row = 0
        self.game_over = False
        print(f"(DEBUG) New secret word is: {self.secret}")

        for r in range(MAX_ATTEMPTS):
            for c in range(WORD_LENGTH):
                lbl = self.cells[r][c]
                lbl.config(text="", bg=COLOR_EMPTY)

        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def on_submit(self):
        if self.game_over:
            return

        guess = self.entry.get().strip().upper()

        if not is_valid_guess(guess, self.words):
            messagebox.showwarning(
                "Invalid Guess",
                "Guess must be a valid 5-letter word in the dictionary.",
            )
            return

        feedback = check_guess(self.secret, guess)
        self._update_row_display(guess, feedback)

        if all(ch == "G" for ch in feedback):
            messagebox.showinfo("You win!", f"You guessed the word: {self.secret}")
            self.game_over = True
            return

        self.current_row += 1
        self.entry.delete(0, tk.END)

        if self.current_row >= MAX_ATTEMPTS:
            messagebox.showinfo("Game Over", f"Out of attempts. The word was: {self.secret}")
            self.game_over = True

    def _update_row_display(self, guess: str, feedback: List[str]):
        """Hiển thị chữ + màu cho hàng hiện tại."""
        row = self.current_row
        for i in range(WORD_LENGTH):
            ch = guess[i]
            status = feedback[i]
            lbl = self.cells[row][i]
            lbl.config(text=ch)

            if status == "G":
                color = COLOR_GREEN
            elif status == "Y":
                color = COLOR_YELLOW
            else:
                color = COLOR_GRAY

            lbl.config(bg=color)


def run_gui(dict_path: str = "data/words.txt"):
    """Hàm entry dùng trong main.py"""
    words = load_words(dict_path)
    if not words:
        raise RuntimeError("Dictionary is empty or not found!")

    root = tk.Tk()
    app = WordleGUI(root, words)
    root.mainloop()
