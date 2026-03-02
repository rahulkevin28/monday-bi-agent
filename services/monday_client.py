import requests


class MondayClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }

    def fetch_board(self, board_id):
        """
        Fetch ALL items from a Monday board using cursor-based pagination.
        """

        all_items = []
        cursor = None

        while True:
            if cursor:
                query = f"""
                {{
                  boards (ids: {board_id}) {{
                    items_page (limit: 100, cursor: "{cursor}") {{
                      cursor
                      items {{
                        name
                        column_values {{
                          id
                          text
                          value
                          type
                        }}
                      }}
                    }}
                  }}
                }}
                """
            else:
                query = f"""
                {{
                  boards (ids: {board_id}) {{
                    items_page (limit: 100) {{
                      cursor
                      items {{
                        name
                        column_values {{
                          id
                          text
                          value
                          type
                        }}
                      }}
                    }}
                  }}
                }}
                """

            response = requests.post(
                self.url,
                json={"query": query},
                headers=self.headers,
                timeout=30
            )

            if response.status_code != 200:
                raise Exception(
                    f"Monday API HTTP Error {response.status_code}: {response.text}"
                )

            data = response.json()

            if "errors" in data:
                raise Exception(f"Monday API Error: {data['errors']}")

            page = data["data"]["boards"][0]["items_page"]
            items = page["items"]
            cursor = page["cursor"]

            all_items.extend(items)

            # Stop when no more pages
            if not cursor:
                break

        return all_items