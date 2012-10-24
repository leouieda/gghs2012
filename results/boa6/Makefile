
all: result.pickle

plot:
	python plot.py

result.pickle: invert.py seeds.json
	python invert.py

clean:
	rm -rf *.pickle predicted.txt
