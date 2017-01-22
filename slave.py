#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sys
import time


def main():
    for i in range(10):
        print("slave count {}".format(i))
        time.sleep(1)


if __name__ == '__main__':
    main()
    sys.exit(0)
