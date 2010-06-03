#!/usr/bin/python

from random   import seed, choice, randint
from optparse import OptionParser


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
            for k in xrange (l) :
                r.append (choice (self.charset))
            yield ''.join (r)
    # end def __iter__
# end class Random_Word

if __name__ == "__main__" :
    import sys
    cmd = OptionParser ()
    cmd.add_option \
        ( "-c", "--charset"
        , dest    = "charset"
        , help    = "charset from which to chose the words"
        , default = ''.join (chr (x) for x in xrange (ord ('a'), ord ('z') + 1))
        )
    cmd.add_option \
        ( "-m", "--minlen"
        , dest    = "minlen"
        , help    = "Minimum length for a word"
        , type    = "int"
        , default = 2
        )
    cmd.add_option \
        ( "-M", "--maxlen"
        , dest    = "maxlen"
        , help    = "Maximum length for a word"
        , type    = "int"
        , default = 7
        )
    cmd.add_option \
        ( "-n", "--nwords"
        , dest    = "nwords"
        , help    = "Number of words to generate"
        , type    = "int"
        , default = 5
        )
    cmd.add_option \
        ( "-r", "--randseed"
        , dest    = "randseed"
        , help    = "random seed"
        , type    = "int"
        , default = None
        )
    cmd.add_option \
        ( "-v", "--vvv"
        , dest    = "vvv"
        , help    = "send vvv before start"
        , default = False
        , action  = "store_true"
        )
    (opt, args) = cmd.parse_args ()
    if len (args) > 0 :
        cmd.print_help (sys.stderr)
        sys.exit (42)

    if opt.vvv :
        print "vvv "
    rw = Random_Word (opt.charset, opt.minlen, opt.maxlen, opt.randseed)
    print ''
    for n, r in enumerate (rw) :
        print r,
        if n + 1 == opt.nwords :
            break
    print
