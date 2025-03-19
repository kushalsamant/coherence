import sys
import os

def split_markdown_by_chapters(input_file):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    chapters = []
    current_chapter = []
    chapter_count = 0

    for line in lines:
        if line.strip().startswith("**"):  # Detect chapter heading
            if current_chapter:
                chapters.append(current_chapter)
                current_chapter = []
            chapter_count += 1
        current_chapter.append(line)

    if current_chapter:
        chapters.append(current_chapter)

    # Save each chapter as a separate Markdown file
    for i, chapter in enumerate(chapters, start=1):
        chapter_filename = f"chapter_{i}.md"
        with open(chapter_filename, "w", encoding="utf-8") as chapter_file:
            chapter_file.writelines(chapter)
        print(f"Saved: {chapter_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_markdown.py <input_markdown_file>")
    else:
        split_markdown_by_chapters(sys.argv[1])
