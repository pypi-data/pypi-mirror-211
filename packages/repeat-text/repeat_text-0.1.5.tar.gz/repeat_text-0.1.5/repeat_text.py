import argparse
from termcolor import colored

def repeat(text, color):
    """Repeats the given text in the specified color."""
    colored_text = colored(text, color)
    print(colored_text)

def main():
    """Parses command-line arguments and runs the repeat command."""
    parser = argparse.ArgumentParser(description='Repeat text in a specified color')
    parser.add_argument('text', type=str, help='the text to repeat')
    parser.add_argument('--color', choices=['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'], default='white', help='the color to use')
    args = parser.parse_args()

    repeat(args.text, args.color)

if __name__ == '__main__':
    main()