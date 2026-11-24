from functions.grep import grep

# Test basic search
result = grep("calculator", "def ")
print("Test 1 - Search for 'def ' in calculator:")
print(result)
print()

# Test search with file extension filter
result = grep("calculator", "def ", file_extension=".py")
print("Test 2 - Search for 'def ' with .py extension:")
print(result)
print()

# Test search for non-existent pattern
result = grep("calculator", "nonexistent_pattern_xyz")
print("Test 3 - Search for non-existent pattern:")
print(result)
print()

# Test search outside working directory
result = grep("calculator", "def ", directory="/bin")
print("Test 4 - Search outside working directory (/bin):")
print(result)
print()

# Test search in non-existent directory
result = grep("calculator", "def ", directory="does_not_exist")
print("Test 5 - Search in non-existent directory:")
print(result)
print()

# Test search in a file instead of directory
result = grep("calculator", "def ", directory="main.py")
print("Test 6 - Search in a file (not a directory):")
print(result)
print()

# Test empty pattern
result = grep("calculator", "")
print("Test 7 - Empty pattern:")
print(result)