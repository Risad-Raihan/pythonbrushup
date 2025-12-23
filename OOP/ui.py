#------------------------------------------------------------
# ASCII UI for Web Research Agent
#------------------------------------------------------------


def render_header():
    print(
        """
╔════════════════════════════════════════════════════╗
║                                                    ║
║   🤖  W E B  R E S E A R C H  A G E N T              ║
║                                                    ║
║   Live Web • Grounded Answers • No Hallucination   ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
    )
    print("Ask anything. I’ll search the web before I answer.\n")


def prompt_user_question() -> str:
    print("┌─ Your question ────────────────────────────────────┐")
    return input("❯ ").strip()


def render_thinking():
    print("\n󰒓 Searching the web...")
    print("󰒓 Reading relevant sources...")
    print("󰒓 Compressing evidence...\n")


def render_short_answer(answer: str):
    lines = wrap_text(answer, width=52)

    print(
        "╔════════════════════════════════════════════════════╗"
    )
    print(
        "║  📌  Short Answer (grounded, ≤ 50 words)           ║"
    )
    print(
        "╠════════════════════════════════════════════════════╣"
    )

    for line in lines:
        print(f"║  {line.ljust(52)}  ║")

    print(
        "╚════════════════════════════════════════════════════╝\n"
    )


def ask_decision() -> str:
    print(
        """
┌────────────────────────────────────────────────────┐
│  Is this enough, or should I go deeper?             │
│                                                    │
│    [y] This is enough                              │
│    [m] Full explanation → Markdown (.md)           │
│                                                    │
└────────────────────────────────────────────────────┘
"""
    )

    while True:
        choice = input("❯ ").strip().lower()
        if choice in {"y", "m"}:
            return choice
        print("Please enter 'y' or 'm'.")


def render_generating_long():
    print("\n󰒓 Expanding reasoning...")
    print("󰒓 Writing structured explanation...")
    print("󰒓 Saving to file...\n")


def render_saved(filename: str):
    print(
        f"""
╔════════════════════════════════════════════════════╗
║  ✅  Explanation saved successfully                ║
╠════════════════════════════════════════════════════╣
║  File: {filename.ljust(45)}║
║  Format: Markdown                                 ║
║                                                    ║
║  You can open it in:                               ║
║  - Obsidian                                        ║
║  - VS Code                                         ║
║  - GitHub                                          ║
╚════════════════════════════════════════════════════╝
"""
    )


def ask_next_action() -> str:
    print(
        """
What next?

  [n] Ask another question
  [q] Quit
"""
    )

    while True:
        choice = input("❯ ").strip().lower()
        if choice in {"n", "q"}:
            return choice
        print("Please enter 'n' or 'q'.")


#------------------------------------------------------------
# Helper: text wrapping for box display
#------------------------------------------------------------

def wrap_text(text: str, width: int):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= width:
            current += (" " if current else "") + word
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines
