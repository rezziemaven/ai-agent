from config import MAX_CHARS
from functions.get_file_content import get_file_content

test_cases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]

for tc in test_cases:
    content = get_file_content(*tc)
    print("==================================")
    print(f"Reading contents of file {tc[1]}...")
    print("----------------------------------")
    if tc[1] == "lorem.txt":
        print("Content length:", len(content))
        print(
            "Truncation message at end:",
            f'[...File "{tc[1]}" truncated at {MAX_CHARS} characters]' in content,
        )
    if "Error: " in content:
        print(content)
        print(" ")
        continue
    print("Content:", content)
    print(" ")
print("==================================")
