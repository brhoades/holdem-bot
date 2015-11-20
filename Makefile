
default: score test

update:
	git submodule init
	git submodule update

score: $(wildcard score/*.cpp)
	make -C score

package: 
	rm ../holdem-bot.zip
	rm -rfv *log __pycache__
	find . -iname "*.pyc" -exec rm -vf {} \;
	zip -r -9 ../holdem-bot.zip *

test:
	rm -f *log
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \
		"python2 bot.py --log --config config_1.json" \
		"python2 bot.py --log --config config_2.json"

profile:
	rm -f *log
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \
		"python2 -m cProfile -o /tmp/profile_data_config_1.pyprof bot.py --log --config config_1.json" \
		"python2 bot.py --log --config config_2.json"
