.PHONY: wedge flat clean


wedge:
	cd wedge; optirun python invert.py

flat:
	cd flat; optirun python invert.py

clean:
	rm -rf wedge/*.pickle wedge/predicted.txt
	rm -rf flat/*.pickle flat/predicted.txt
