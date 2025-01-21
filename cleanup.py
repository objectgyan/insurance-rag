import shutil
from pathlib import Path

def cleanup():
    # Remove the chroma directory
    chroma_dir = Path("data/chroma")
    if chroma_dir.exists():
        shutil.rmtree(chroma_dir)
        print(f"Removed {chroma_dir}")

    # Remove the __pycache__ directories
    for pycache in Path().rglob("__pycache__"):
        shutil.rmtree(pycache)
        print(f"Removed {pycache}")

    # Remove any .chroma directories
    for chroma in Path().rglob(".chroma"):
        shutil.rmtree(chroma)
        print(f"Removed {chroma}")

if __name__ == "__main__":
    cleanup()