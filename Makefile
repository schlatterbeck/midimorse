
all: quick.ps quick.mid paris.ps paris.mid

quick.abc: genmorse.py
	echo "the quick brown fox jumps over the lazy dog" \
	   | genmorse.py -o quick.abc -t 'Quick Brown Fox' -n a -m 70

paris.abc: genmorse.py
	echo paris paris paris paris paris paris \
             paris paris paris paris paris paris \
	   | genmorse.py -o paris.abc -t 'Paris' -n a

%.ps: %.abc
	abcm2ps -O $@ $<

%.mid: %.abc
	abc2midi $< -o $@

clean:
	rm -f quick.ps quick.mid quick.abc paris.abc paris.mid paris.ps
