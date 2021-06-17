#!/usr/bin/python3

from __future__ import print_function
from random   import seed, choice, randint
from argparse import ArgumentParser


class Random_Word (object) :
    """ Generate random words from the given charset in the given
        length range.
    """
    def __init__ (self, charset, minlen = 2, maxlen = 7, randseed = None) :
        if randseed :
            seed (randseed)
        self.minlen  = minlen
        self.maxlen  = maxlen
        self.charset = charset
    # end def __init__

    def __iter__ (self) :
        """ Iterator to return next random word """
        while True :
            l = randint (self.minlen, self.maxlen)
            r = []
            for k in range (l) :
                r.append (choice (self.charset))
            yield ''.join (r)
    # end def __iter__
# end class Random_Word

if __name__ == "__main__" :
    import sys
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( "-c", "--charset"
        , dest    = "charset"
        , help    = "charset from which to chose the words"
        , default = ''.join (chr (x) for x in range (ord ('a'), ord ('z') + 1))
        )
    cmd.add_argument \
        ( "-m", "--minlen"
        , dest    = "minlen"
        , help    = "Minimum length for a word"
        , type    = int
        , default = 2
        )
    cmd.add_argument \
        ( "-M", "--maxlen"
        , dest    = "maxlen"
        , help    = "Maximum length for a word"
        , type    = int
        , default = 7
        )
    cmd.add_argument \
        ( "-n", "--nwords"
        , dest    = "nwords"
        , help    = "Number of words to generate"
        , type    = int
        , default = 5
        )
    cmd.add_argument \
        ( "-r", "--randseed"
        , dest    = "randseed"
        , help    = "random seed"
        , type    = int
        )
    cmd.add_argument \
        ( "-v", "--vvv"
        , dest    = "vvv"
        , help    = "send vvv before start"
        , default = False
        , action  = "store_true"
        )
    args = cmd.parse_args ()

    if args.vvv :
        print ("vvv ")
    rw = Random_Word (args.charset, args.minlen, args.maxlen, args.randseed)
    print ('')
    for n, r in enumerate (rw) :
        print (r, end = ' ')
        if n + 1 == args.nwords :
            break
    print ()
