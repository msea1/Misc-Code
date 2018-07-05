import argparse
import json

def parse_txt(journal_file, out_file):
    pass


def parse_json(journal_file, out_file):
    with open(journal_file) as fin:
        journal = json.load(fin)



parser = argparse.ArgumentParser(description='Turn Day One Journal into Markdown.')
parser.add_argument('i', help='Input file, exported from Day One')
parser.add_argument('o', help='Output file')
args = parser.parse_args()
# print(f'{args.i}')
# print(f'{args.o}')
if args.i.endswith('.txt'):
    parse_txt(args.i, args.o)
elif args.i.endswith('.json'):
    parse_json(args.i, args.o)
else:
    print(f'Invalid input file, needs to be a txt or json, not {args.i}')
    exit(1)

