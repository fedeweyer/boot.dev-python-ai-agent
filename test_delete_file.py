from functions.delete_file import delete_file

# Create a test file first
from functions.write_file import write_file
write_file(".", "test_delete_target.txt", "This file will be deleted.")

# Test 1: Delete an existing file
print("Test 1: Delete existing file")
result = delete_file(".", "test_delete_target.txt")
print(result)

# Test 2: Delete a non-existent file
print("\nTest 2: Delete non-existent file")
result = delete_file(".", "nonexistent.txt")
print(result)

# Test 3: Try to delete a directory
print("\nTest 3: Try to delete a directory")
result = delete_file(".", "calculator")
print(result)

# Test 4: Try to delete outside working directory
print("\nTest 4: Delete outside working directory")
result = delete_file(".", "/tmp/test.txt")
print(result)

# Test 5: Delete a file in a subdirectory
print("\nTest 5: Delete file in subdirectory")
write_file(".", "subdir_test.txt", "subdir test")
import os
os.makedirs("test_subdir", exist_ok=True)
write_file(".", "test_subdir/nested.txt", "nested file")
result = delete_file(".", "test_subdir/nested.txt")
print(result)
# Clean up empty dir
os.rmdir("test_subdir")

print("\nAll delete tests completed.")
