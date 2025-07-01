
from functions.get_files_info import get_files_info

result = get_files_info("calculator", ".")
print(f"Result for the current directory:\n{result}")


result2 = get_files_info("calculator", "pkg")
print(f"Result for 'pkg' directory:\n{result2}")

result3 = get_files_info("calculator", "/bin")
print(f"Result for '/bin' directory:\n{result3}")

result4 = get_files_info("calculator", "../")
print(f"Result for '../' directory:\n{result4}")
