import requests
from bs4 import BeautifulSoup


def print_secret_message(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    grid_data = {}
    max_x = 0
    max_y = 0

    for row in soup.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) != 3:
            continue

        try:
            x = int(cells[0].get_text(strip=True))
            character = cells[1].get_text(strip=True)
            y = int(cells[2].get_text(strip=True))
        except ValueError:
            continue

        grid_data[(x, y)] = character
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    for y in range(max_y, -1, -1):
        row_output = "".join(
            grid_data.get((x, y), " ")
            for x in range(max_x + 1)
        )

        print(row_output)

if __name__ == "__main__":
    doc_url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    print_secret_message(doc_url)