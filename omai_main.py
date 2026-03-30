"""
Jss Wealthtech - Main Entry Point
॥ जय श्री सांवरीया सेठ ि॥
"""
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from ui.desktop import JssDesktop
        from tkinter import Tk
        root = Tk()
        app = JssDesktop(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
