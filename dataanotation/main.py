import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):
    """
    Fetches a published Google Doc as HTML, parses a table of (x, char, y) triplets,
    and prints the decoded message in a grid, with y=0 at the top.
    """
    # Fetch the document HTML
    resp = requests.get(doc_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Parse all table rows, skipping header
    rows = soup.find_all('tr')[1:]
    points = []

    for row in rows:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        try:
            x = int(cells[0].get_text(strip=True))
            char = cells[1].get_text(strip=True)
            y = int(cells[2].get_text(strip=True))
            points.append((x, y, char))
        except (ValueError, IndexError):
            continue  # Skip malformed rows

    if not points:
        print("No data found.")
        return

    max_x = max(x for x, y, _ in points)
    max_y = max(y for x, y, _ in points)

    # Initialize grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y, char in points:
        # Use only the first character (in case of extra whitespace or multi-char)
        grid[y][x] = char[0] if char else ' '

    # Print grid with y=0 at the top, strip trailing spaces to match expected output
    for row in reversed(grid):
        print(''.join(row).rstrip())

if __name__ == "__main__":
    decode_secret_message(
        "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    )
