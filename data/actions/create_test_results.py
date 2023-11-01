import os

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "output", "results"
    )
)

if os.path.exists(BASE_DIR):
    total_test_results = len(os.listdir(BASE_DIR))
    path = os.path.join(BASE_DIR, f"TestResults{total_test_results+1}.csv")
    with(open(path, mode="x", encoding="utf-8")):
        pass
