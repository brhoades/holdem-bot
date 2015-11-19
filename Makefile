test:
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem "python2 bot.py --config config_2.json" "python2 bot.py --config config_2.json"

update:
	git submodule init
	git submodule update

default: test
