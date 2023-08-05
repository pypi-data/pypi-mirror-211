#!/usr/bin/env python3

args=[]

def print_debug(message):
   import sys
   if args.debug_mode:
      print(message, file=sys.stderr)

def size_string(size):
   import humanize
   return humanize.naturalsize(size) if args.human_readable_size else size
   
def rclone_ls(path):
   from rclone.rclone import Rclone
   import shlex
   import sys

   rc = Rclone()

   # python rclone bug workaround: by using '--copy-links', it does not complain about symbolic links. it does not show them neither.
   files=rc.ls(path, '--copy-links')  
   print_debug(files)

   sizes=[]
   for file in files:
      print_debug(f'trying {file}')

      size = rc.size(shlex.quote(f'{path}/{file}'))
      print_debug(size)
      print(f"{size_string(size['total_size'])}\t{file}")

      size['path'] = file
      sizes.append(size)

   total = sum(size['total_size'] for size in sizes)
   print(f"total:\t{size_string(total)}", file=sys.stderr)

   print_debug(sizes)


def main():
   import argparse

   parser = argparse.ArgumentParser()
   parser.description = 'List files/dirs and their sizes in a given rclone path. For instance: rclone_ls remote:/path'
   parser.add_argument("rclone_path", help="rclone path")
   parser.add_argument("-H", action="store_true", dest="human_readable_size", help="Use unit suffixes: Byte, Kilobyte, Megabyte...")
   parser.add_argument("--debug", action="store_true", dest="debug_mode", help="Enable debug mode")

   global args
   args = parser.parse_args()

   rclone_ls(args.rclone_path)


if __name__ == '__main__':
   main()
