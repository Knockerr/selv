import sqlite3

# Connect do db.
conn = sqlite3.connect("servers.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def cleanDb():
    cursor.execute("DELETE FROM servers WHERE uuid NOT IN ('demoUuid', 'demoUuid2')")
    conn.commit()


rows = cursor.execute("SELECT * FROM servers")
print([dict(row) for row in cursor.fetchall()])


# import httpx
# from bs4 import BeautifulSoup
# import json
#
#
# async def scrape_getbukkit():
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             "https://getbukkit.org/download/spigot",
#             headers={"User-Agent": "Mozilla/5.0"}
#         )
#
#     soup = BeautifulSoup(response.text, "html.parser")
#     panes = soup.select(".download-pane")
#
#     result = {}
#
#     for pane in panes:
#         version = pane.select_one("h2").text.strip()
#         download_url = pane.select_one("a.btn-download")["href"]
#
#         result[version] = {
#             "url": download_url
#         }
#
#     return result
#
#
# import asyncio
#
# data = asyncio.run(scrape_getbukkit())
# print(json.dumps(data, indent=2))