import argparse
import json
import os
from typing import Optional


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='VSCode snippet -> UltiSnips')
    parser.add_argument('filename', type=argparse.FileType(mode='rb'))
    parser.add_argument('--priority', type=int, default=None, required=False)
    return parser


def convert(vscode: dict, priority: Optional[int]) -> str:
    strip_prefix = ''
    if len(vscode) > 1:
        strip_prefix = os.path.commonprefix(
            list(item['prefix'] for item in vscode.values())
        )

    result = [
        '# Autoconverted from visual studio code',
        '',
    ]
    if priority is not None:
        result.extend([f'priority {priority}', ''])

    for name, info in sorted(vscode.items(), key=lambda kv: kv[0]):
        if isinstance(info['body'], list):
            info['body'] = '\n'.join(info['body'])
        info['prefix'] = info['prefix'][len(strip_prefix):]
        result.append("""\
snippet {prefix} "{name}"
{body}
endsnippet
""".format(name=name, **info))
    return '\n'.join(result)


def main():
    parser = build_parser()
    args = parser.parse_args()
    vscode = json.load(args.filename)
    print(convert(vscode, priority=args.priority))


if __name__ == '__main__':
    main()
