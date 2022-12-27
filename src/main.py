import argparse
from pathlib import Path

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("title")
    parser.add_argument("--yratio", type=float, default=1.414)  # A4
    args = parser.parse_args()

    subtitle, title = args.title.split("{sub}", 1)

    # One line per page
    print(
        "\n".join(
            str(svg) for svg in render(parse(args.file), title, subtitle, args.yratio)
        )
    )


if __name__ == "__main__":
    main()
