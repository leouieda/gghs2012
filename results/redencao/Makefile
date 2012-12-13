.PHONY: wedge flat clean


wedge:
	cd wedge; optirun python invert.py

flat:
	cd flat; optirun python invert.py

clean-fig:
	rm -rf wedge/*.png wedge/*.pdf flat/*.png flat/*.pdf

clean:
	rm -rf wedge/*.pickle wedge/predicted.txt
	rm -rf flat/*.pickle flat/predicted.txt
