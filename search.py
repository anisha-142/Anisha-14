import os

def search_files():
    workspace = r"d:\Campusplacement"
    keywords = ["php", "ai", "data", "science", "marketing", "digital"]
    extensions = (".pdf", ".pptx", ".ppt", ".docx", ".doc")
    
    print("Searching for matching files...")
    matches = []
    for root, dirs, files in os.walk(workspace):
        # Skip env virtualenv folder
        if "env" in root.split(os.sep):
            continue
        for file in files:
            file_lower = file.lower()
            if file_lower.endswith(extensions):
                if any(kw in file_lower for kw in keywords):
                    matches.append(os.path.join(root, file))
                    
    print(f"Found {len(matches)} files:")
    for path in sorted(matches):
        print(path)

if __name__ == "__main__":
    search_files()
