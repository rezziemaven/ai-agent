from functions.run_python_file import run_python_file

test_cases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt"),
]

for tc in test_cases:
    print("==================================")
    print(f"Attempting to run {tc[1]}...")
    print("----------------------------------")
    print(run_python_file(*tc))
    print(" ")
print("==================================")
