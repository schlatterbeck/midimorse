#!/usr/local/bin/python

import sys
import string

code = \
    { 'a'    : '.-'
    , 'ä'    : '.-.-'
    , 'b'    : '-...'
    , 'c'    : '-.-.'
    , 'ch'   : '----'
    , 'd'    : '-..'
    , 'e'    : '.'
    , 'f'    : '..-.'
    , 'g'    : '--.'
    , 'h'    : '....'
    , 'i'    : '..'
    , 'j'    : '.---'
    , 'k'    : '-.-'
    , 'l'    : '.-..'
    , 'm'    : '--'
    , 'n'    : '-.'
    , 'o'    : '---'
    , 'ö'    : '---.'
    , 'p'    : '.--.'
    , 'q'    : '--.-'
    , 'r'    : '.-.'
    , 's'    : '...'
    , 't'    : '-'
    , 'u'    : '..-'
    , 'ü'    : '..--'
    , 'v'    : '...-'
    , 'w'    : '.--'
    , 'x'    : '-..-'
    , 'y'    : '-.--'
    , 'z'    : '--..'
    , '1'    : '.----'
    , '2'    : '..---'
    , '3'    : '...--'
    , '4'    : '....-'
    , '5'    : '.....'
    , '6'    : '-....'
    , '7'    : '--...'
    , '8'    : '---..'
    , '9'    : '----.'
    , '0'    : '-----'
    , '.'    : '.-.-.-'
    , ','    : '--..--'
    , ':'    : '---...'
    , '?'    : '..--..'
    , '/'    : '-..-.'
    , '-'    : '-....-'
    , '(ve)' : '...-.'
    , '(eb)' : '.-...'
    , '(err)': '........'
    , '(ka)' : '-.-.-'
    , '(ar)' : '.-.-.'
    , '='    : '-...-'
    , '('    : '-.--.'
    , ')'    : '-.--.-'
    , "'"    : '.----.'
    , ';'    : '-.-.-.'
    , '_'    : '..--.-'
    , '(sk)' : '..-.-'
}

bpm_wpm = 5
steps_bpm = 12

class abc :
    def __init__ (self, file, wpm) :
        self.file      = file
        self.wpm       = wpm
        self.pause     = 5
        self.count     = 0
        self.takt      = 8 # M: 4/4
        self.taktcount = 0
        self.file.write ('X: 1\nT: quick brown fox\nM: 4/4\nL: 1/8\n')
        self.file.write ('Q: 1/8=%d\nK: C\n' % (self.wpm * bpm_wpm * steps_bpm))
        self.file.write ("%%MIDI program 74\n")
    # end def __init__

    def update (self, str) :
        for i in string.lower (str) :
            if i in string.whitespace :
                self.pause = 5
            if code.has_key (i) : 
                self._output_char (code [i])
                self.count += 1
    # end def update

    def _output_char (self, coded_char) :
        if self.count >= 10 :
            self.file.write ('\n')
            self.count = 0
        if self.pause < 3 : self.pause = 3
        for i in coded_char :
            self.o_map [i](self)
            self.pause = 1
    # end def _output_char

    def _output_takt (self) :
        if self.takt == self.taktcount :
            self.file.write ('| ')
            self.taktcount = 0

    def _output_pause (self) :
        while (self.pause) :
            pause = self.pause
            if pause > self.takt - self.taktcount :
                pause = self.takt - self.taktcount
            self.pause -= pause
            self.taktcount += pause
            for i in (8, 6, 4, 3, 2) :
                while pause >= i :
                    self.file.write ('z%d ' % i)
                    pause -= i
            if pause :
                self.file.write ('z ')
            self._output_takt ()

    def _output_dit (self) :
        self._output_pause ()
        self.file.write ('a ')
        self.taktcount += 1
        self._output_takt ()

    def _output_dah (self) :
        self._output_pause ()
        length = l = 3
        if l > self.takt - self.taktcount :
            l = self.takt - self.taktcount
        if l < length :
            self.file.write ('a%d- ' % l)
            self.taktcount += l
            self._output_takt ()
            self.file.write ('a%d ' % (length - l))
            self.taktcount += (length - l)
        else :
            self.file.write ('a3 ')
            self.taktcount += l
        self._output_takt ()

    o_map = { '.' : _output_dit, '-' : _output_dah }
# end class abc

file = sys.stdin
if len (sys.argv) > 1 : file = open (sys.argv [1])
str = "".join (file.readlines ())

ofile = sys.stdout

cw = abc (ofile, 12)
cw.update (str)
