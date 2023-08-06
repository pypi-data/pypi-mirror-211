import argparse
from . import (
    __name__ as name,
    __description__ as description,
    __copyright__ as copyright,
    __version__ as version
)
from .start import main as start
from .config import get_config

def main():
    parser = argparse.ArgumentParser(
        prog = name,
        description = description,
        epilog = "Example: sqdconvert -in input_file.mp4 -out output_file.mp3"
    )

    parser.add_argument("-in", "--input",
                        help="input file for conversion")
    parser.add_argument("-out", "--output",
                        help="output file")
    parser.add_argument("-i", "--interactive",
                        action="store_true", help="start an interactive conversion")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print more output")
    parser.add_argument("-V", "--version",
                        action="version", version=name+" "+version)
    parser.add_argument("-l", "--license",
                        action="version", version=copyright+" - MIT License. For more information see: https://opensource.org/license/mit/",
                        help="show program's license and exit")
    
    config = get_config()

    args = parser.parse_args()
    start(args, config)

if __name__ == "__main__":
    main()