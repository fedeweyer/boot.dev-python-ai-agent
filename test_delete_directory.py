from functions.delete_directory import delete_directory

# Create test directories and files first
from functions.write_file import write_file
import os

# Create a directory to delete
os.makedirs("test_delete_dir", exist_ok=True)
write_file(".", "test_delete_dir/file1.txt", "file 1")
write_file(".", "test_delete_dir/file2.txt", "file 2")
os.makedirs("test_delete_dir/subdir", exist_ok=True)
write_file(".", "test_delete_dir/subdir/nested.txt", "nested file")

# Test 1: Delete an existing directory with contents
print("Test 1: Delete existing directory with contents")
result = delete_directory(".", "test_delete_dir")
print(result)

# Test 2: Delete a non-existent directory
print("\nTest 2: Delete non-existent directory")
result = delete_directory(".", "nonexistent_dir")
print(result)

# Test 3: Try to delete a file (not a directory)
print("\nTest 3: Try to delete a file")
write_file(".", "test_delete_file.txt", "this is a file")
result = delete_directory(".", "test_delete_file.txt")
print(result)

# Test 4: Try to delete outside working directory
print("\nTest 4: Delete outside working directory")
result = delete_directory(".", "/tmp/test_dir")
print(result)

# Test 5: Delete a directory in a subdirectory
print("\nTest 5: Delete directory in subdirectory")
os.makedirs("test_parent", exist_ok=True)
os.makedirs("test_parent/child_dir", exist_ok=True)
write_file(".", "test_parent/child_dir/file.txt", "child file")
result = delete_directory(".", "test_parent/child_dir")
print(result)
# Clean up parent
os.rmdir("test_parent")

print("\nAll delete directory tests completed.")
