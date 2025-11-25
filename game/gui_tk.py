import tkinter as tk
from tkinter import messagebox
from typing import List

from .logic import load_words, choose_secret, check_guess, is_valid_guess
from solvers.bfs_solver import bfs_solve
from solvers.dfs_solver import ids_solve
from solvers.astar_solver import astar_solve
from solvers.ucs_solver import ucs_solve


WORD_LENGTH = 5

COLOR_BG = "#121213"
COLOR_EMPTY = "#3a3a3c"
COLOR_TYPING = "#787c7e"      # ô đang nhập
COLOR_GREEN = "#6aaa64"
COLOR_YELLOW = "#c9b458"
COLOR_GRAY = "#787c7e"
COLOR_TEXT = "#ffffff"

COLOR_KEY_DEFAULT = "#202020"
COLOR_KEY_TEXT = "#ff8800"    # chữ cam
COLOR_KEY_GREEN = "#6aaa64"
COLOR_KEY_YELLOW = "#c9b458"
COLOR_KEY_GRAY = "#3a3a3c"


class WordleGUI:
    def __init__(self, root: tk.Tk, words: List[str], graph):
        self.root = root
        self.words = words
        self.graph = graph
        self.secret = choose_secret(words)

        self.current_row = 0
        self.current_col = 0
        self.game_over = False

        self.root.title("Wordle – Python Version")
        self.root.configure(bg=COLOR_BG)

        print(f"(DEBUG) Secret word is: {self.secret}")

        self.cells_all_rows = []
        self.settings_window = None

        self._build_title()
        self._build_board()
        self._build_keyboard()

        self.root.bind("<Key>", self.on_physical_key)
        self.root.bind("<BackSpace>", lambda e: self.on_backspace())
        self.root.bind("<Return>", lambda e: self.on_enter())

        # Tạo sẵn 6 hàng trống
        for _ in range(6):
            self._create_row()

    def on_physical_key(self, event):
        ch = event.char.upper()
        if "A" <= ch <= "Z":
            self.on_key_press(ch)

    # ======================================================
    # TITLE
    # ======================================================
    def _build_title(self):
        header = tk.Frame(self.root, bg=COLOR_BG)
        header.pack(fill="x", pady=(5, 0)) 

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=1)


        # TITLE nằm ở cột giữa (col=1)
        title = tk.Label(
            header,
            text="WORDLE",
            font=("Helvetica", 40, "bold"),
            fg="#00e6e6",
            bg=COLOR_BG
        )
        title.grid(row=0, column=1, pady=10)

        # SETTINGS BUTTON nằm góc phải (col=2)
        settings_btn = tk.Button(
            header,
            text="⚙",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_BG,
            fg="#00e6e6",
            bd=0,
            command=self.open_settings
        )
        settings_btn.grid(row=0, column=2, sticky="ne", padx=20)


    def open_settings(self):
        # Nếu cửa sổ đã mở rồi
        if self.settings_window is not None and tk.Toplevel.winfo_exists(self.settings_window):
            self.settings_window.lift()       
            self.settings_window.focus_force() 
            return

        # Nếu chưa có 
        self.settings_window = tk.Toplevel(self.root)
        win = self.settings_window

        win.title("Settings")
        win.configure(bg=COLOR_BG)
        win.geometry("300x350")

        # Khi user đóng cửa sổ 
        def on_close():
            self.settings_window = None
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(
            win, text="Solver Options",
            font=("Helvetica", 18, "bold"),
            bg=COLOR_BG, fg="#00e6e6"
        ).pack(pady=10)

        tk.Button(
            win, text="Run BFS Solver",
            font=("Helvetica", 14, "bold"),
            bg="#333333", fg="white",
            command=lambda: self.run_solver("bfs")
        ).pack(pady=5)

        tk.Button(
            win, text="Run DFS Solver",
            font=("Helvetica", 14, "bold"),
            bg="#333333", fg="white",
            command=lambda: self.run_solver("dfs")
        ).pack(pady=5)


        tk.Button(
            win, text="Run UCS Solver",
            font=("Helvetica", 14, "bold"),
            bg="#333333", fg="white",
            command=lambda: self.run_solver("ucs")
        ).pack(pady=5)

        tk.Button(
            win, text="Run A* Solver",
            font=("Helvetica", 14, "bold"),
            bg="#333333", fg="white",
            command=lambda: self.run_solver("astar")
        ).pack(pady=5)

        # RESET BUTTON
        tk.Button(
            win, text="Reset Game",
            font=("Helvetica", 14, "bold"),
            bg="#552222",     
            fg="white",
            command=self.restart_game
        ).pack(pady=10)

    def restart_game(self):
        """Reset toàn bộ game về trạng thái ban đầu."""

        # Tạo lại secret mới
        self.secret = choose_secret(self.words)
        print(f"(DEBUG) New secret word is: {self.secret}")

        # Reset trạng thái nội bộ
        self.game_over = False
        self.current_row = 0
        self.current_col = 0

        # Xóa tất cả row cũ trên GUI
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        self.cells_all_rows.clear()

        # Tạo lại đúng 6 hàng trống ban đầu
        for _ in range(6):
            self._create_row()

        # Reset keyboard màu sắc
        for ch, btn in self.key_buttons.items():
            btn.config(bg=COLOR_KEY_DEFAULT, fg=COLOR_KEY_TEXT)

        # Scroll về đầu
        self.canvas.yview_moveto(0.0)

    def run_solver(self, mode):
        if self.game_over:
            return

        start_word = self.cells_all_rows[0][0].cget("text") or self.words[0]
        goal_word = self.secret

        if mode == "bfs":
            path = bfs_solve(start_word, goal_word, self.words, self.graph)
        elif mode == "dfs":
            path = ids_solve(start_word, goal_word, self.words, self.graph)
        elif mode == "ucs":
            path = ucs_solve(start_word, goal_word, self.words, self.graph)
        elif mode == "astar":
            path = astar_solve(start_word, goal_word, self.words, self.graph)
        else:
            return

        if not path:
            messagebox.showwarning("No path", "Không tìm được đường đi!")
            return

        # Loại bỏ start_word vì solver spit cả start
        if path[0] == start_word:
            path = path[1:]

        self.run_guess_sequence(path)

    def run_guess_sequence(self, guesses):
        self.solver_guesses = guesses
        self.solver_index = 0

        def do_step():
            if self.solver_index >= len(self.solver_guesses):
                return

            guess = self.solver_guesses[self.solver_index]

            # nhập guess vào row
            for i, ch in enumerate(guess):
                cell = self.cells_all_rows[self.current_row][i]
                cell.config(text=ch, bg=COLOR_TYPING)

            self.current_col = 5
            self.on_enter()

            self.solver_index += 1

            if not self.game_over:
                self.root.after(900, do_step)

        do_step()

    # ======================================================
    # BOARD + SCROLL
    # ======================================================
    def _build_board(self):
        board_container = tk.Frame(self.root, bg=COLOR_BG)
        board_container.pack()

        self.canvas = tk.Canvas(
            board_container,
            width=500,
            height=420,
            bg=COLOR_BG,
            highlightthickness=0,
        )
        self.canvas.pack(side="left")

        scrollbar = tk.Scrollbar(
            board_container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Enable mousewheel scroll when cursor is inside canvas/board
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        self.inner_frame.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.inner_frame.bind("<Leave>", lambda e: self._unbind_mousewheel())


    def _on_mousewheel(self, event):
        # Windows
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Linux
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")


    def _bind_mousewheel(self):
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)


    def _unbind_mousewheel(self):
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    # ======================================================
    # CREATE ONE ROW
    # ======================================================
    def _create_row(self):
        row_cells = []
        row_index = len(self.cells_all_rows)

        for c in range(WORD_LENGTH):
            lbl = tk.Label(
                self.inner_frame,
                text="",
                width=4,
                height=2,
                font=("Helvetica", 24, "bold"),
                bg=COLOR_EMPTY,
                fg=COLOR_TEXT,
                relief="ridge",
                bd=3,
            )
            lbl.grid(row=row_index, column=c, padx=5, pady=5)

            lbl.bind("<Enter>", lambda e: self._bind_mousewheel())
            lbl.bind("<Leave>", lambda e: self._unbind_mousewheel())

            row_cells.append(lbl)

        self.cells_all_rows.append(row_cells)


    # ======================================================
    # KEYBOARD
    # ======================================================
    def _build_keyboard(self):
        kb_frame = tk.Frame(self.root, bg=COLOR_BG)
        kb_frame.pack(pady=20)

        layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        self.key_buttons = {}

        # Row 1
        for r, row in enumerate(layout):
            row_frame = tk.Frame(kb_frame, bg=COLOR_BG)
            row_frame.pack()

            for ch in row:
                btn = tk.Button(
                    row_frame,
                    text=ch,
                    font=("Helvetica", 14, "bold"),
                    width=4,
                    height=2,
                    fg=COLOR_KEY_TEXT,
                    bg=COLOR_KEY_DEFAULT,
                    command=lambda c=ch: self.on_key_press(c)
                )
                btn.pack(side="left", padx=3, pady=3)
                self.key_buttons[ch] = btn

        # Special keys
        bottom = tk.Frame(kb_frame, bg=COLOR_BG)
        bottom.pack()

        enter_btn = tk.Button(
            bottom,
            text="ENTER",
            font=("Helvetica", 14, "bold"),
            width=6,
            height=2,
            fg=COLOR_KEY_TEXT,
            bg=COLOR_KEY_DEFAULT,
            command=self.on_enter
        )
        enter_btn.pack(side="left", padx=3)

        back_btn = tk.Button(
            bottom,
            text="←",
            font=("Helvetica", 14, "bold"),
            width=4,
            height=2,
            fg=COLOR_KEY_TEXT,
            bg=COLOR_KEY_DEFAULT,
            command=self.on_backspace
        )
        back_btn.pack(side="left", padx=3)


    # ======================================================
    # INPUT: PRESS LETTER
    # ======================================================
    def on_key_press(self, ch):
        if self.game_over:
            return
        if self.current_col >= WORD_LENGTH:
            return

        cell = self.cells_all_rows[self.current_row][self.current_col]
        cell.config(text=ch, bg=COLOR_TYPING)

        self.current_col += 1


    # ======================================================
    # BACKSPACE
    # ======================================================
    def on_backspace(self):
        if self.game_over:
            return
        if self.current_col == 0:
            return

        self.current_col -= 1
        cell = self.cells_all_rows[self.current_row][self.current_col]
        cell.config(text="", bg=COLOR_EMPTY)


    # ======================================================
    # ENTER → CHECK WORD WITH ANIMATION
    # ======================================================
    def on_enter(self):
        if self.game_over:
            return
        if self.current_col < WORD_LENGTH:
            return

        guess = "".join(
            self.cells_all_rows[self.current_row][i].cget("text")
            for i in range(WORD_LENGTH)
        )

        if not is_valid_guess(guess, self.words):
            messagebox.showwarning("Invalid word", f"{guess} is not in dictionary!")
            return

        feedback = check_guess(self.secret, guess)

        # Animation + color update
        self.animate_row(self.current_row, guess, feedback)

        if all(ch == "G" for ch in feedback):
            self.game_over = True
            messagebox.showinfo("You win!", f"Secret word: {self.secret}")
            return

        # Next row
        self.current_row += 1
        self.current_col = 0

        if self.current_row >= len(self.cells_all_rows):
            self._create_row()
            self.canvas.yview_moveto(1.0)


    # ======================================================
    # ANIMATION FLIP
    # ======================================================
    def animate_row(self, row_index, guess, feedback):
        cells = self.cells_all_rows[row_index]

        def flip_cell(i):
            if i >= WORD_LENGTH:
                return

            cell = cells[i]

            # Shrink
            cell.config(width=2)
            self.root.after(100, lambda: expand(i))

        def expand(i):
            color = (
                COLOR_GREEN if feedback[i] == "G" else
                COLOR_YELLOW if feedback[i] == "Y" else
                COLOR_GRAY
            )

            cell = cells[i]
            cell.config(width=4, bg=color)

            # Update keyboard color
            self.update_keyboard(guess[i], feedback[i])

            self.root.after(100, lambda: flip_cell(i + 1))

        flip_cell(0)


    # ======================================================
    # KEYBOARD COLOR UPDATE
    # ======================================================
    def update_keyboard(self, ch, status):
        btn = self.key_buttons[ch]

        if status == "G":
            btn.config(bg=COLOR_KEY_GREEN)
        elif status == "Y":
            if btn.cget("bg") != COLOR_KEY_GREEN:
                btn.config(bg=COLOR_KEY_YELLOW)
        else:
            if btn.cget("bg") not in (COLOR_KEY_GREEN, COLOR_KEY_YELLOW):
                btn.config(bg=COLOR_KEY_GRAY)


# ======================================================
# RUN GUI
# ======================================================
def run_gui(words, graph):
    root = tk.Tk()
    WordleGUI(root, words, graph)
    root.mainloop()
