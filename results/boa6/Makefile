
all: result.pickle

plot:
	python plot.py

result.pickle: invert.py seeds.json data.xyz
	python invert.py

clean:
	rm -rf *.pickle predicted.txt
