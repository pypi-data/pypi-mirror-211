from pathlib import Path
import argparse

from poetry2rye.convert import convert


def main():
    parser = argparse.ArgumentParser(
        prog="poetry2rye",
        description="A simple tool to migrate your Poetry project to rye",
        )
    parser.add_argument("-p", "--path", default="./")
    
    args = parser.parse_args()
    
    project_path = Path(args.path)
    convert(project_path)
