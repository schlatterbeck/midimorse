
all: quick.ps quick.mid paris.ps paris.mid

quick.abc: genmorse.py
	echo "the quick brown fox jumps over the lazy dog" \
	   | genmorse.py -o quick.abc -t 'Quick Brown Fox' -n a -m 70

paris.abc: genmorse.py
	echo paris paris paris paris paris paris \
             paris paris paris paris paris paris \
	   | genmorse.py -o paris.abc -t 'Paris' -n a -f 20 -w 10

%.ps: %.abc
	abcm2ps -O $@ $<

%.mid: %.abc
	abc2midi $< -o $@

%.abc: %.txt
	cat $< | genmorse.py -o $@ -t '$@' -n a -f 20 -w 12

clean:
	rm -f quick.ps quick.mid quick.abc paris.abc paris.mid paris.ps
