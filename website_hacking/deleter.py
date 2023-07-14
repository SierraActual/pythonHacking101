import random

def delete_and_alphabetize_words(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
        total_words = len(words)
        words_to_delete = int(total_words * 0.93)
        random.shuffle(words)
        deleted_words = words[:words_to_delete]
        remaining_words = words[words_to_delete:]
        remaining_words.sort()
    
    new_file_path = 'short_sample_dirlist.txt'  # Replace with desired new file path
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(remaining_words)
    
    print(f"Deleted {len(deleted_words)} words from the original file.")
    print(f"Remaining words have been alphabetized and saved to '{new_file_path}'.")

# Example usage
file_path = 'sample_dirlist.txt'  # Replace with your file path
delete_and_alphabetize_words(file_path)
