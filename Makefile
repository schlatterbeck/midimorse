
all: quick.ps quick.mid

quick.abc: genmorse.py
	echo "the quick brown fox jumps over the lazy dog" \
	   | genmorse.py -o quick.abc -t 'Quick Brown Fox' -n a

%.ps: %.abc
	abcm2ps -O $@ $<

%.mid: %.abc
	abc2midi $< -o $@

clean:
	rm -f quick.ps quick.mid quick.abc
