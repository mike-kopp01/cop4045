# Michael Koppelmann Problem 5 Homework 1
# This is the entire Codex code that was created and pasted into VSCode
"""Caesar-cipher encryption utilities."""


def caesar(text: str, shift: int) -> str:
    """Return text with letters shifted by the given amount."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted = ""

    for character in text:
        if character.lower() in alphabet:
            original_index = alphabet.index(character.lower())
            shifted_character = alphabet[(original_index + shift) % len(alphabet)]
            encrypted += (
                shifted_character.upper()
                if character.isupper()
                else shifted_character
            )
        else:
            encrypted += character

    return encrypted


def decrypt_caesar(text: str, shift: int) -> str:
    """Return the clear text by reversing a Caesar-cipher shift."""
    return caesar(text, -shift)


def count_letters(text: str) -> dict[str, int]:
    """Count letters, ignoring case and non-alphabetic characters."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    counts = {letter: 0 for letter in alphabet}

    for character in text.lower():
        if character in alphabet:
            counts[character] += 1

    return counts


def display_letter_counts(counts: dict[str, int]) -> None:
    """Print each letter that appears and its frequency."""
    for letter, count in counts.items():
        if count > 0:
            print(f"{letter}: {count}")


def get_shift() -> int:
    """Prompt until the user enters a whole-number shift."""
    while True:
        try:
            return int(input("Enter the shift value: "))
        except ValueError:
            print("Please enter a whole number, such as 3 or -2.")


def main() -> None:
    """Run the Caesar-cipher terminal menu."""
    while True:
        print("\n--- Caesar Cipher Menu ---")
        print("1. Encrypt, decrypt, and analyze a message")
        print("2. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            message = input("Enter a message: ")
            shift = get_shift()

            encrypted_message = caesar(message, shift)
            decrypted_message = decrypt_caesar(encrypted_message, shift)

            print(f"\nCiphered text: {encrypted_message}")
            print("\nLetter frequency breakdown (ciphered text):")
            display_letter_counts(count_letters(encrypted_message))
            print(f"\nDeciphered text: {decrypted_message}")

        elif choice == "2":
            print("Goodbye!")
            break

        else:
            print("Please choose 1 or 2.")


if __name__ == "__main__":
    main()