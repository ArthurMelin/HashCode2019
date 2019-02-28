#!/usr/bin/python3

import itertools
import os
import random
import sys
from pprint import pprint


class Pic:
    def __init__(self, id, orientation, tags):
        self.id = id
        self.orientation = orientation
        self.tags = tags

    def __repr__(self):
        return 'Pic <%d, %s, %s>' % (self.id, self.orientation, self.tags)


def main(args):
    if len(args) != 1:
        print('usage: %s file' % sys.argv[0])
        return 1

    with open(args[0], 'rt') as f:
        lines = [line for line in f]

    lines = lines[1:]

    PICS = {}
    TAGS = {}

    for i, line in enumerate(lines):
        orientation, ntags, *tags = line.rstrip().split(' ')
        PICS[i] = Pic(i, orientation, tags)
        for tag in tags:
            if not tag in TAGS:
                TAGS[tag] = []
            TAGS[tag].append(i)


    slides = []
    prev = []

    N = len(PICS)


    def remove_pic(pic):
        del PICS[pic.id]
        if len(PICS) % 100 == 0:
            print('\r%d' % (100 * (N - len(PICS)) // N), end='')
        for tag in pic.tags:
            del TAGS[tag][TAGS[tag].index(pic.id)]
            if len(TAGS[tag]) == 0:
                del TAGS[tag]

    def make_slide():
        nonlocal prev

        def score(p):
            s = sum([tag in prev for tag in p.tags])
            return min([len(prev) - s, s, len(p.tags) - s])

        pics = iter([])
        for tag in prev:
            if tag in TAGS:
                pics = itertools.chain(pics, itertools.islice(map(lambda id: PICS[id], TAGS[tag]), 50))
        pics = list(pics)
        if len(pics) < 200:
            pics += itertools.islice(PICS.values(), 200 - len(pics))
        else:
            pics = random.sample(pics, 200)
        pic = max(pics, key=score)

        remove_pic(pic)
        if pic.orientation == 'H':
            prev = pic.tags
            return '%d' % pic.id
        elif pic.orientation == 'V':
            v = filter(lambda p: p.orientation == 'V', PICS.values())
            v = list(itertools.islice(v, 400))
            if len(v) == 0:
                return
            other = min(v, key=lambda p: sum([tag in pic.tags for tag in p.tags]))
            remove_pic(other)
            prev = pic.tags + other.tags
            return '%d %d' % (pic.id, other.id)

    while len(PICS):
        slide = make_slide()
        if slide:
            slides.append(slide)

    print()
    with open('out/' + args[0], 'wt') as f:
        f.write(str(len(slides)) + '\n')
        f.writelines(map(lambda s: s + '\n', slides))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
