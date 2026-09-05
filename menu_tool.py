from pathlib import Path

MENU_FILE = Path(__file__).resolve().parent / "menu.txt"


def search_menu(query: str) -> str:
    """
    Search the coffee shop menu for relevant items and prices.
    """
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as file:
            menu = file.read()
    except FileNotFoundError:
        return "Menu file is unavailable."

    query_words = query.lower().split()

    relevant_lines = []

    for line in menu.splitlines():
        line_lower = line.lower()

        if any(word in line_lower for word in query_words):
            relevant_lines.append(line)

    if relevant_lines:
        return "\n".join(relevant_lines)

    return menu