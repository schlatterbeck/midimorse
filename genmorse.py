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
    , 'Ä'    : '.-.-'
    , 'æ'    : '.-.-'
    , 'Æ'    : '.-.-'
    , 'å'    : '.--.-'
    , 'Å'    : '.--.-'
    , 'à'    : '.--.-'
    , 'À'    : '.--.-'
    , 'b'    : '-...'
    , 'c'    : '-.-.'
    , 'ç'    : '-.-..'
    , 'Ç'    : '-.-..'
    , '[ch]' : '----'
    , 'd'    : '-..'
    , 'e'    : '.'
    , 'è'    : '.-..-'
    , 'È'    : '.-..-'
    , 'é'    : '..-..'
    , 'É'    : '..-..'
    , 'f'    : '..-.'
    , 'g'    : '--.'
    , 'h'    : '....'
    , 'i'    : '..'
    , 'j'    : '.---'
    , 'k'    : '-.-' # also invitation to transmit
    , 'l'    : '.-..'
    , 'm'    : '--'
    , 'n'    : '-.'
    , 'ñ'    : '--.--'
    , 'Ñ'    : '--.--'
    , 'o'    : '---'
    , 'ö'    : '---.'
    , 'Ö'    : '---.'
    , 'p'    : '.--.'
    , 'q'    : '--.-'
    , 'r'    : '.-.'
    , 's'    : '...'
    , 'ß'    : '...--.'
    , 't'    : '-'
    , 'u'    : '..-'
    , 'ü'    : '..--'
    , 'Ü'    : '..--'
    , 'ð'    : '..--.'
    , 'v'    : '...-'
    , 'w'    : '.--'
    , 'x'    : '-..-'
    , 'y'    : '-.--'
    , 'z'    : '--..'
    , 'þ'    : '.--..'
    , 'Þ'    : '.--..'
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
    , '!'    : '-.-.--'
    , '/'    : '-..-.'
    , '-'    : '-....-'
    , '[ve]' : '...-.'    # Understood # Verstanden
    , '[eb]' : '.-...'    # Wait
    , '[sk]' : '...-.-'   # End of Work # Verkehrsende
    # '[sk]' : '..-.-'    # probably wrong
    , '&'    : '.-...'
    , '[hh]' : '........' # Error # Fehler
    , '[ka]' : '-.-.-'    # Spruchanfang
    , '[ar]' : '.-.-.'    # Starting Signal # Spruchende (sic)
    , '+'    : '.-.-.'
    , '[bt]' : '-...-'    # Pause
    , '='    : '-...-'
    , '('    : '-.--.'
    , ')'    : '-.--.-'
    , "'"    : '.----.'
    , '"'    : '.-..-.'
    , ';'    : '-.-.-.'
    , '_'    : '..--.-'
    , '$'    : '...-..-'
    , '@'    : '.--.-.'
    , '[sos]': '...---...' # SOS
}

bpm_wpm        =  5
steps_bpm      = 10
default_wpm    = 12
default_title  = 'quick brown fox'
default_midi   = 74
default_note   = 'a'

class abc :
    """ Class for generating morse code in abc notation
        Spacing: We use the word "paris" .-.- .- .-. .. ...
        dot = "dit" = length 1, dash = "dah" = length 3
        for intra-character pause with length = 1
        and inter-character pause with length = 3
        spacing at word boundary is counted as 7
        which results in a word length
        for paris of 1+1+3+1+1+1+3+3 +1+1+3+3 +1+1+3+1+1+3 +1+1+1+3
        +1+1+1+1+1+7 = 50 and an average character length of 10 -- for
        the 5 letter word paris. So we set the steps_bpm by default to 10
        (10 unit-1 steps per character) and the bpm_wpm multiplier to 5
        (5 characters per word). Comparing this to other morse code
        samples that claim a certain speed seems to confirm this
        formula.
        For Farnsworth spacing (adding more pause to an otherwise faster
        signal) we use a multiplier for the notes to get as close as
        possible to the given pause speed. The farnsworth_wpm speed
        needs to be higher than the given wpm speed. We use the
        farnsworth speed for generating the characters and then add
        enough pause to come down to the wmp speed.

        The following formula gives the timing of the pause per
        character *in farnsworth_wpm* timing -- C is the inter-character
        timing, W is the inter-word timing.

         31     4C     W     50
        ---- + ---- + ---- = ---
        fwpm   fwpm   fwpm   wpm

        50 fwpm         19             50 fwpm        19
        ------- - 31 =  -- C           ------- - 31 = -- W
          wpm            3              wpm            7

        For solving this, we need the timing for C and W:

              3
         C  = - W
              7

        solved for C and W we get:

        150 * fwpm   93             350 * fwpm     217
        ---------- - --  = C        ----------  -  ---  = W
         19 * wpm    19              19 * wpm      19

        fwpm stands for the faster farnsworth_wpm speed. Each character
        has 10 units, we need to make longer pauses in farnsworth timing
        to reach the same per-character speed in wpm. If wpm==fwpm, we
        get the normal inter-character timing of 3 dits and inter-word
        spacing of 7 dits. For faster fwpm we get larger C and W.
        C and W are measured in farnsworth-timing dits.
    """
    def __init__ \
        ( self
        , ofile
        , wpm            = default_wpm
        , title          = default_title
        , midi           = default_midi
        , note           = default_note
        , farnsworth_wpm = default_wpm
        ) :
        self.multiplier = m = 1
        self.wpm        = wpm
        self.fwpm       = farnsworth_wpm
        pause_add       = 0
        if self.fwpm < self.wpm :
            self.fwpm = self.wpm
        if self.fwpm > self.wpm :
            self.multiplier = m = 8
        self.ditpause   = self.multiplier
        self.dahpause   = int \
            ((m * 150. * self.fwpm) / (19. * self.wpm) -  93. * m / 19. + 0.5)
        self.wpause     = int \
            ((m * 350. * self.fwpm) / (19. * self.wpm) - 217. * m / 19. + 0.5)
        self.pause      = self.wpause
        self.file       = ofile
        self.title      = title
        self.midi       = midi
        self.note       = note
        self.tcount     = 0
        self.takt       = 8 * self.multiplier # M: 4/4
        self.taktcount  = 0
        self.closed     = False

        self.file.write \
            ('X: 1\nT: %s\nM: 4/4\nL: 1/%s\n'
            % (self.title, 8 * self.multiplier)
            )
        self.file.write ('Q: 1/8=%d\n' % (self.fwpm * bpm_wpm * steps_bpm))
        self.file.write ('K: C\n')
        self.file.write ("%%%%MIDI program %s\n" % self.midi)
    # end def __init__

    def update (self, str) :
        for i in string.lower (str) :
            if i in string.whitespace :
                self.pause = self.wpause
            if code.has_key (i) : 
                self._output_char (code [i])
    # end def update

    def _output_char (self, coded_char) :
        if self.pause < self.dahpause : self.pause = self.dahpause
        for i in coded_char :
            self.o_map [i](self)
            self.pause = self.ditpause
    # end def _output_char

    def _output_takt (self) :
        if self.takt == self.taktcount :
            self.file.write ('| ')
            self.taktcount = 0
            self.tcount += 1
            if self.tcount > 5 :
                self.file.write ('\n')
                self.tcount = 0

    def _output_length (self, symbol, length, bind = 0) :
        """ Output a symbol with length length.
            Precondition: Symbol does not cross next takt boundary
            bind: can be 0 (never) 1 (all but last) or 2 (all)
        """
        b1 = b2 = ''
        if bind :
            b1 = '-'
        if bind > 1 :
            b2 = '-'
        for i in (64, 48, 32, 24, 16, 12, 8, 6, 4, 3, 2) :
            while length >= i :
                assert (length != 1)
                b = b1
                if length == i :
                    b = b2
                self.file.write ('%s%d%s ' % (symbol, i, b))
                length -= i
        if length :
            self.file.write ('%s%s ' % (symbol, b2))
    # end def _output_length

    def _output_symbol (self, symbol, length, bind = False) :
        """ Output a symbol with length length.
            Symbol might cross next takt boundary
        """
        while length > self.takt - self.taktcount :
            l = self.takt - self.taktcount
            length         -= l
            self.taktcount += l
            self._output_length (symbol, l, 2 * bind)
            self._output_takt   ()
        if length :
            self.taktcount += length
            self._output_length (symbol, length, bind)
            self._output_takt   ()
    # end def _output_symbol

    def _output_pause (self) :
        self._output_symbol ('z', self.pause)
        self.pause = 0

    def _output_dit (self) :
        self._output_pause  ()
        self._output_symbol (self.note, self.multiplier, True)

    def _output_dah (self) :
        self._output_pause ()
        self._output_symbol (self.note, 3 * self.multiplier, True)
    
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
    cmd.add_option \
        ( "-f", "--farnsworth-wpm"
        , dest    = "fwpm"
        , help    = "Farnsworth speed in words per minute"
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
        , wpm            = options.wpm
        , title          = options.title
        , midi           = options.midi
        , note           = options.note
        , farnsworth_wpm = options.fwpm
        )
    cw.update (str)
