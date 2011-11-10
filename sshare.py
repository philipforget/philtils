#!/usr/bin/env python

import hashlib
import sys
import os


class Main():
    def __init__(self, args):
        for filename in args[1:]:
            ext = '.' + filename.split('.')[-1].lower() if filename.find('.') >= 0 else ""
            md = hashlib.md5()
            with open(filename, 'rb') as file:
                md.update(file.read())

            target = '{md_sum}{ext}'.format(
                md_sum = md.hexdigest()[:6],
                ext = ext)

            os.system(
                'scp "{source}" "aprtr:/home/www/aprtr.com/share/{target}"'.format(
                    source = filename,
                    target = target
                )
            )

            print 'http://aprtr.com/share/%s' % target


if __name__ == '__main__':
    Main(sys.argv)
