#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-9 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import sys
import string
from   optparse import OptionParser

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

bpm_wpm       =  5
steps_bpm     = 12
default_wpm   = 12
default_title = 'quick brown fox'
default_midi  = 74
default_note  = 'a'

class abc :
    def __init__ \
        ( self
        , ofile
        , wpm   = default_wpm
        , title = default_title
        , midi  = default_midi
        , note  = default_note
        ) :
        self.file      = ofile
        self.wpm       = wpm
        self.title     = title
        self.midi      = midi
        self.note      = note
        self.pause     = 5
        self.tcount    = 0
        self.takt      = 8 # M: 4/4
        self.taktcount = 0
        self.closed    = False
        self.file.write ('X: 1\nT: %s\nM: 4/4\nL: 1/8\n' % self.title)
        self.file.write ('Q: 1/8=%d\nK: C\n' % (self.wpm * bpm_wpm * steps_bpm))
        self.file.write ("%%%%MIDI program %s\n" % self.midi)
    # end def __init__

    def update (self, str) :
        for i in string.lower (str) :
            if i in string.whitespace :
                self.pause = 5
            if code.has_key (i) : 
                self._output_char (code [i])
    # end def update

    def _output_char (self, coded_char) :
        if self.pause < 3 : self.pause = 3
        for i in coded_char :
            self.o_map [i](self)
            self.pause = 1
    # end def _output_char

    def _output_takt (self) :
        if self.takt == self.taktcount :
            self.file.write ('| ')
            self.taktcount = 0
            self.tcount += 1
            if self.tcount > 5 :
                self.file.write ('\n')
                self.tcount = 0

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
        self.file.write ('%s ' % self.note)
        self.taktcount += 1
        self._output_takt ()

    def _output_dah (self) :
        self._output_pause ()
        length = l = 3
        if l > self.takt - self.taktcount :
            l = self.takt - self.taktcount
        if l < length :
            self.file.write ('%s%d- ' % (self.note, l))
            self.taktcount += l
            self._output_takt ()
            self.file.write ('%s%d ' % (self.note, length - l))
            self.taktcount += (length - l)
        else :
            self.file.write ('%s3 ' % self.note)
            self.taktcount += l
        self._output_takt ()
    
    def close (self) :
        if not self.closed :
            self.closed = True
            self.pause = self.takt - self.taktcount
            self._output_pause ()
            self.file.write ('\n')
            self.file.close ()
    # end def close
    __del__ = close

    o_map = { '.' : _output_dit, '-' : _output_dah }
# end class abc

if __name__ == '__main__' :
    cmd = OptionParser ()
    cmd.add_option \
        ( "-i", "--input"
        , dest    = "input"
        , help    = "Input File, default is stdin"
        )
    cmd.add_option \
        ( "-o", "--output"
        , dest    = "output"
        , help    = "Output File, default is stdout"
        )
    cmd.add_option \
        ( "-m", "--midi"
        , dest    = "midi"
        , help    = "Midi instrument (patch/program) number"
        , type    = "int"
        , default = default_midi
        )
    cmd.add_option \
        ( "-n", "--note"
        , dest    = "note"
        , help    = "Note to play in abc notation"
        , default = default_note
        )
    cmd.add_option \
        ( "-t", "--title"
        , dest    = "title"
        , help    = "Title of song, used for typesetting music"
        , default = default_title
        )
    cmd.add_option \
        ( "-w", "--wpm"
        , dest    = "wpm"
        , help    = "Speed in words per minute"
        , type    = "int"
        , default = default_wpm
        )
    (options, args) = cmd.parse_args ()
    if len (args) > 0 :
        cmd.print_help (sys.stderr)
        sys.exit (42)

    if options.input :
        ifile = open (options.input)
    else :
        ifile = sys.stdin
    if options.output :
        ofile = open (options.output, "w")
    else :
        ofile = sys.stdout

    str = "".join (ifile.readlines ())

    cw = abc \
        ( ofile
        , wpm   = options.wpm
        , title = options.title
        , midi  = options.midi
        , note  = options.note
        )
    cw.update (str)
