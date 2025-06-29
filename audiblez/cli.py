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
    parser.add_argument('-v', '--voice', default=default_voice, help=f'Choose narrating voice: {voices_str}')
    parser.add_argument('-p', '--pick', default=False, help='Interactively select which chapters to read in the audiobook', action='store_true')
    parser.add_argument('-s', '--speed', default=1.0, help='Set speed from 0.5 to 2.0', type=float)
    parser.add_argument('-c', '--cuda', default=False, help='Use GPU via Cuda in Torch if available', action='store_true')
    parser.add_argument('-o', '--output', default='.', help='Output folder for the audiobook and temporary files', metavar='FOLDER')
    parser.add_argument('--list-chapters', action='store_true', help='List chapter names in the EPUB without converting to audio')

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

    from audiblez.core import main

    if args.list_chapters:
        def list_chapter_event(event_type, **kwargs):
            if event_type == 'CORE_STARTED':
                print("Running audiblez to detect chapters (no conversion will happen)...")
            elif event_type == 'CORE_SELECTED_CHAPTERS':
                print("📚 Chapters Detected:")
                for i, chapter in enumerate(kwargs.get('chapters', []), start=1):
                    print(f"  {i}. {chapter.get_name()}")
                sys.exit(0)

        main(
            file_path=args.epub_file_path,
            voice=args.voice,
            pick_manually=args.pick,
            speed=args.speed,
            output_folder=args.output,
            post_event=list_chapter_event
        )
        return

    # Normal execution
    main(
        file_path=args.epub_file_path,
        voice=args.voice,
        pick_manually=args.pick,
        speed=args.speed,
        output_folder=args.output
    )


if __name__ == '__main__':
    cli_main()
