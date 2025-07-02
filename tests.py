
from functions.get_file_content import get_file_content

result = get_file_content("calculator", "main.py")
print(result)

result2 = get_file_content("calculator", "pkg/calculator.py")
print(result2)

result3 = get_file_content("calculator", "/bin/cat")
print(result3)