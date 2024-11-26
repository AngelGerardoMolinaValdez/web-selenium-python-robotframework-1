import os

__BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "data"
    )
)

OPEN_NEW_ACCOUNT_DATA_PATH = os.path.join(__BASE_PATH, "open_new_account.csv")
