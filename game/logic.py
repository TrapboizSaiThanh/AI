# game/logic.py

import random
from typing import List


def load_words(path: str) -> List[str]:
    """Load 5-letter words from file, uppercase hết cho đồng nhất."""
    words = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) == 5 and w.isalpha():
                words.append(w)
    return words


def choose_secret(words: List[str]) -> str:
    """Randomly pick a secret word."""
    return random.choice(words)


def check_guess(secret: str, guess: str) -> List[str]:
    """
    Compare guess với secret, trả về list 5 ký tự:
    - 'G' = Green (đúng chữ, đúng vị trí)
    - 'Y' = Yellow (đúng chữ, sai vị trí)
    - 'B' = Gray (không nằm trong từ)
    """
    secret = secret.upper()
    guess = guess.upper()

    if len(secret) != 5 or len(guess) != 5:
        raise ValueError("secret and guess must both be 5 letters")

    result = ["B"] * 5
    secret_chars = list(secret)

   
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = "G"
            secret_chars[i] = None  

  
    for i in range(5):
        if result[i] == "G":
            continue
        if guess[i] in secret_chars:
            result[i] = "Y"
            idx = secret_chars.index(guess[i])
            secret_chars[idx] = None

    return result


def is_valid_guess(guess: str, dictionary: List[str]) -> bool:
    """Check guess hợp lệ: 5 chữ cái, có trong dictionary."""
    guess = guess.strip().upper()
    return len(guess) == 5 and guess.isalpha() and guess in dictionary


def play_console(secret: str, dictionary: List[str]) -> None:
    """Version console đơn giản để test logic trước."""
    MAX_ATTEMPTS = 6
    attempt = 0

    print("Welcome to Wordle (console version)!")
  
    print(f"(DEBUG) Secret word is: {secret}")

    while attempt < MAX_ATTEMPTS:
        guess = input(f"Guess #{attempt + 1}: ").strip().upper()

        if not is_valid_guess(guess, dictionary):
            print("Invalid guess. Must be a valid 5-letter word in the dictionary.")
            continue

        feedback = check_guess(secret, guess)
        print("Feedback:", " ".join(feedback))

        if all(ch == "G" for ch in feedback):
            print("You got it! 🎉")
            return

        attempt += 1

    print(f"Out of attempts. The word was: {secret}")
