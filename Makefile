test:
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem "python2 bot.py" "python2 bot.py"

update:
	git submodule init
	git submodule update

default: test
