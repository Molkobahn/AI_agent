from functions.run_python_file import run_python_file

result1 = run_python_file("calculator", "main.py")
print(result1)

result2 = run_python_file("calculator", "tests.py")
print(result2)

result3 = run_python_file("calculator", "../main.py")
print(result3)

result4 = run_python_file("calculator", "nonexistent.py")
print(result4)