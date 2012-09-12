
all: result.pickle


seeds: pickseeds.py
	python pickseeds.py

result.pickle: invert.py seeds.json gravity-anomaly-residual.dat
	python invert.py

clean:
	rm -rf result.pickle predicted.txt
