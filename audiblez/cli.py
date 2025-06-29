# -*- coding: utf-8 -*-
import argparse
import sys

from audiblez.voices import voices, available_voices_str


def cli_main():
    voices_str = ', '.join(voices)
    epilog = ('example:\n' +
              '  audiblez book.epub -l en-us -v af_sky\n\n' +
              'to run GUI just run:\n'
              '  audiblez-ui\n\n' +
              'available voices:\n' +
              available_voices_str)
    default_voice = 'af_sky'

    parser = argparse.ArgumentParser(
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('epub_file_path', help='Path to the epub file')
    parser.add_argument('-v', '--voice', default=default_voice,
                        help=f'Choose narrating voice: {voices_str}')
    parser.add_argument('-p', '--pick', default=False,
                        help='Interactively select which chapters to read in the audiobook',
                        action='store_true')
    parser.add_argument('-s', '--speed', default=1.0,
                        help='Set speed from 0.5 to 2.0', type=float)
    parser.add_argument('-c', '--cuda', default=False,
                        help='Use GPU via Cuda in Torch if available',
                        action='store_true')
    parser.add_argument('-o', '--output', default='.',
                        help='Output folder for the audiobook and temporary files',
                        metavar='FOLDER')

    # ✅ New argument
    parser.add_argument('--list-chapters', action='store_true',
                        help='List chapter names and exit (no conversion)')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.cuda:
        import torch.cuda
        if torch.cuda.is_available():
            print('CUDA GPU available')
            torch.set_default_device('cuda')
        else:
            print('CUDA GPU not available. Defaulting to CPU')

    # ✅ New behavior: list chapters and exit
    if args.list_chapters:
        from core import list_chapters
        list_chapters(args.epub_file_path)
        sys.exit(0)

    from core import main
    main(args.epub_file_path, args.voice, args.pick, args.speed, args.output)


if __name__ == '__main__':
    cli_main()
