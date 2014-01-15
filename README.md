Slides and code for the talk given at the 2012 International Symposium on
Gravity, Geoid and Height Systems (GGHS), in Venice, Italy.

Slides in PDF format are available on figshare:
[doi:10.6084/m9.figshare.156859](http://dx.doi.org/10.6084/m9.figshare.156859)

Citation:

Uieda, L. and V. C. F. Barbosa (2012), Rapid 3D inversion of gravity and
gravity gradient data to test geologic hypotheses, International Symposium on
Gravity, Geoid and Height Systems.

# Rapid 3D inversion of gravity and gravity gradient data to test geologic hypotheses

**Leonardo Uieda and Valéria C. F. Barbosa**

Forward modeling of potential fields is a useful way to incorporate the
interpreter's knowledge about the geology of the interpretation area into the
model. However, this can be a very tedious task. This is specially true when
modeling in 3D and trying to fit multiple components, e.g., in gravity
gradiometry. The interpreter is required to simultaneously supervise the data
fit and the construction of geologically realistic 3D bodies. This problem is
partially solved by methods of geophysical inversion, which automatically fit
the data. Conversely, inverse problems introduce other challenges of their own.
Most geophysical inverse problems are ill-posed because their solutions are
neither unique nor stable. Thus, they require the introduction of prior
information, usually through regularizing functions. Moreover, 3D inverse
problems are very computationally expensive. Recent developments in potential
field inversion have proposed different regularizing functions to transform
the ill-posed problem into a well-posed one. Also, several techniques, like
data compression and parallel computation, have been applied to overcome the
computational complexity. We call attention to the method of potential field
inversion by planting anomalous densities. This method uses an iterative
algorithm to automatically grow the anomalous bodies around user-specified
prismatic elements called "seeds", which have fixed density contrasts and
positions. These seeds provide a first estimate of the skeletal outlines of
the presumed anomalous bodies. Then, the inversion iteratively concentrates
mass around this "skeleton" in a way that both fits the observed data and
yields compact bodies. Therefore, the interpreter can easily impose prior
information on the inversion through the seeds. The interpreter needs only to
supply a few seeds that specify the sources' skeleton, eliminating the
exhaustive task of specifying the complete geometry of multiple sources.
Moreover, the interpreter is liberated from the time- consuming procedure of
yielding a reasonable fit to the data. Due to its high computational
efficiency, the method of planting anomalous densities can be used to quickly
test geologic hypothesis of different locations and density contrasts for
presumed sources. To test a hypothesis, one would choose the locations and
density contrasts of the seeds accordingly and verify if the inversion result
is able to fit the observed data. If it is not able, then the hypothesis can
be rejected and a new one can be formulated and tested. Otherwise, there is no
reason to reject the hypothesis on the basis of the geophysical data. Thus,
the method can be viewed as a an enhanced forward modeling. The method of
planting anomalous densities can be used with both gravity and gravity gradient
data. This makes it an ideal tool to interpret compact geologic bodies using
the new generation GOCE data. We present applications to synthetic and real
data that illustrate the usefulness of our method.

## Method used

Results presented were obtained using the method of
**planting anomalous densities**
(see [my personal page](http://www.fatiando.org/people/uieda/)
for download links):

Uieda, L., and V. C. F. Barbosa (2012a), Robust 3D gravity gradient inversion
by planting anomalous densities, Geophysics, 77(4), G55-G66,
doi:10.1190/geo2011-0388.1.

Uieda, L., and V. C. F. Barbosa (2012b), Use of the "shape-of-anomaly" data
misfit in 3D inversion by planting anomalous densities, SEG Technical Program
Expanded Abstracts, 1-6, doi:10.1190/segam2012-0383.1.

This method is implemented in software
[Fatiando a Terra](https://github.com/leouieda/fatiando).
To run the results, you'll need the 0.1 version.
See the [documentation](https://fatiando.readthedocs.org/en/v0.1/)
for instructions.

If you run into any trouble trying to run the results, contact
[Leonardo Uieda](http://www.fatiando.org/people/uieda/).


## Data

* Quadrilatero Ferrifero: The FTG data was provided by Vale and is not made available here
* Registro do Araguaia: Data was digitized from Dutra et al. (2012)
* Redenção: Data was digitized from de Oliveira et al. (2008)


## References

de Oliveira, D. C., R. Dall’Agnol, J. B. Corrêa da Silva, and J. A. Costa de Almeida (2008), Gravimetric, radiometric, and magnetic susceptibility study of the Paleoproterozoic Redenção and Bannach plutons, eastern Amazonian Craton, Brazil: Implications for architecture and zoning of A-type granites, Journal of South American Earth Sciences, 25(1), 100–115, doi:10.1016/j.jsames.2007.10.003.

Dutra, A. C., Y. R. Marangoni, and T. C. Junqueira-Brod (2012), Investigation of the Goiás Alkaline Province, Central Brazil: Application of gravity and magnetic methods, Journal of South American Earth Sciences, 33(1), 43–55, doi:10.1016/j.jsames.2011.06.004.


