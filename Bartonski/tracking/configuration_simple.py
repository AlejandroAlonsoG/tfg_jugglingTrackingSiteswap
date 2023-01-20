import sys
import json
import argparse

parser = argparse.ArgumentParser(allow_abbrev=True)

parser.add_argument(
    'VIDEO FILE', type=str,
    help='Input video file'
)