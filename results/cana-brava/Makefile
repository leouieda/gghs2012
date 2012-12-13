
all: result.pickle

plot:
	optirun python plot.py

seeds: pickseeds.py
	python pickseeds.py

result.pickle: invert.py seeds-larger.json seeds-smaller.json \
gravity-anomaly-residual.dat
	optirun python invert.py

clean:
	rm -rf result.pickle predicted.txt
