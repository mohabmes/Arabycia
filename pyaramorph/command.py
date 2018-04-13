# command.py
# Command line interface to pyaramorph

import readline
import pyaramorph

def main():
    """ Read user input, analyze, output results. """
    analyzer = pyaramorph.Analyzer()
    print("Unicode Arabic Morphological Analyzer (press ctrl-d to exit)")
    while True:
        try:
            s = input("$ ")
            results = analyzer.analyze_text(s)
        except EOFError:
            print("Goodbye!")
            break

        for analyses in results:
            for solution in analyses:
                print(solution)

if __name__ == '__main__':
    main()

