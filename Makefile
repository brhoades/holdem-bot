# site information
SITE=i.brod.es
DIR=/var/www/images/
URL=https://$(SITE)/
FILE:=$(shell mktemp /tmp/XXXXX.svg)
NAME:=$(shell basename $(FILE))

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

test_real:
	rm -f *log
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \
		"python2 bot.py --log --config config_1.json" \
		"python2 bot.py --log --config config_2.json"

test: test_ea

test_ea:
	rm -f *log
	java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \
		"python2 bot.py --log --config config_1.json --use-eval" \
		"python2 bot.py --log --config config_2.json --use-eval"

profile:
	-@ echo "Cleaning up" 
	-@ rm -f *log &> /dev/null
	-@ rm -f /tmp/profile_data_config_1.pyprof &> /dev/null
	-@ echo "Profiling..."
	-@ python2 -m cProfile -o /tmp/profile_data_config_1.pyprof bot.py \
		--config config_1.json --no-log --use-eval < profile_input/bot_input_p1.txt &> /dev/null
	@echo "Creating SVG"
	-@ pyprof2calltree2 -i /tmp/profile_data_config_1.pyprof -o /tmp/profile_data_config_1.callgrind
	gprof2dot  --format=callgrind --output=/tmp/out.dot /tmp/profile_data_config_1.callgrind
	 dot -Tsvg /tmp/out.dot -o$(FILE) &> /dev/null
	 @echo "Uploading $(FILE)"
	 chmod 775 $(FILE)
	 scp $(FILE) $(SITE):$(DIR)
	URL=$(URL)$(NAME)
	@echo "Uploaded: $(URL)"
	-@ echo $(URL) | xsel -c -i &> /dev/null

#java -cp ../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \
#	"python2 -m cProfile -o /tmp/profile_data_config_1.pyprof bot.py --config config_1.json --use-eval" \
#	"python2 -m cProfile -o /tmp/profile_data_config_2.pyprof bot.py --config config_2.json --use-eval" 
