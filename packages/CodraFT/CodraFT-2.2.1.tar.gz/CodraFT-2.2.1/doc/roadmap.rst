Roadmap
=======

Next major release: DataLab
---------------------------

DataLab 1.0
^^^^^^^^^^^

.. figure:: images/DataLab-banner.png

    DataLab is the next major release of CodraFT

DataLab is a platform for data processing and visualization, with a focus on
extensibility, automation and reproducibility, thanks to its macro-command
system, a high-level Python API and a plugin system.

.. figure:: images/DataLab-Overview.png

    DataLab overview

DataLab is a complete rewrite of CodraFT, with a new architecture and
new features, including:

* Process isolation for running computations safely:

  * Execute a "computing server" in background, in another process
  * For each computation, send pickled data and computing function
    to the server and wait for the result
  * Application main window stays responsive during computations
  * It is then possible to stop any computation at any time by killing the
    server process and restarting it

* Image displaying performance optimization

* Support for plugins:

  * Custom processing features available in the "Plugins" menu
  * Custom I/O features: new file formats can be added to the standard I/O
    features for signals and images
  * Custom HDF5 features: new HDF5 file formats can be added to the standard
    HDF5 import feature
  * More features to come...

* New macro-command system:

  * New embedded Python editor
  * Scripts using the same API as high-level applicative test scenarios
  * Support for macro recording

* New XML-RPC server to allow external applications controlling
  CodraFT main features (open a signal or an image, open a HDF5 file, etc.)

* New "Computing parameters" group box to show last result input parameters

* New "Copy titles to clipboard" feature in "Edit" menu

* New image processing features:

  * Pixel binning operation (X/Y binning factors, operation: sum, mean, ...)
  * "Distribute on a grid" and "Reset image positions" in operation menu
  * Butterworth filter
  * Exposure processing features:
    * Gamma correction
    * Logarithmic correction
    * Sigmoïd correction
  * Restoration processing features:
    * Total variation denoising filter (TV Chambolle)
    * Bilateral filter (denoising)
    * Wavelet denoising filter
    * White Top-Hat denoising filter
  * Morphological transforms (disk footprint):
    * White Top-Hat
    * Black Top-Hat
    * Erosion
    * Dilation
    * Opening
    * Closing
  * Edge detection features:
    * Roberts filter
    * Prewitt filter (vertical, horizontal, both)
    * Sobel filter (vertical, horizontal, both)
    * Scharr filter (vertical, horizontal, both)
    * Farid filter (vertical, horizontal, both)
    * Laplace filter
    * Canny filter
  * Circle Hough transform (circle detection)
  * Image intensity levels rescaling
  * Histogram equalization
  * Adaptative histogram equalization
  * Blob detection methods:
    * Difference of Gaussian
    * Determinant of Hessian method
    * Laplacian of Gaussian
    * Blob detection using OpenCV
  * Result shapes and annotations are now transformed (instead of removed) when
    executing one of the following operations:
    * Rotation (arbitrary angle, +90°, -90°)
    * Symetry (vertical/horizontal)

Other ideas for future releases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Add support for multichannel timeseries

* Add support for timeseries

* Add a "Preferences" dialog box to setup all configurable parameters

Past milestones
---------------

CodraFT 2.2
^^^^^^^^^^^

* Optimize image visualization performance

* Add default image visualization settings in .INI configuration file

CodraFT 2.1
^^^^^^^^^^^

* "Open in a new window" feature: add support for multiple separate windows,
  thus allowing to visualize for example two images side by side

* New demo mode

* New command line option features (open/browse HDF5 files at startup)

* ROI features:

  - Add an option to extract multiples ROI on either
    one signal/image (current behavior) or one signal/image per ROI
  - Images: create ROI using array masks
  - Images: add support for circular ROI

CodraFT 2.0
^^^^^^^^^^^

* New data processing and visualization features (see below)

* Fully automated high-level processing features for internal testing purpose,
  as well as embedding CodraFT in a third-party software

* Extensive test suite (unit tests and application tests)
  with 90% feature coverage

CodraFT 1.7
^^^^^^^^^^^

* Major redesign

* Python 3.8 is the new reference

* Dropped Python 2 support

CodraFT 1.6
^^^^^^^^^^^

* Last release supporting Python 2
