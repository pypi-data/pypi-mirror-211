"Processing" menu
=================

.. image:: /images/shots/i_processing.png

Linear calibration
    Create a new image which is a linear calibration
    of each selected image with respect to Z axis:

    .. list-table::
        :header-rows: 1
        :widths: 40, 60

        * - Parameter
          - Linear calibration
        * - Z-axis
          - :math:`z_{1} = a.z_{0} + b`

Thresholding
    Apply the thresholding to each selected image.

Clipping
    Apply the clipping to each selected image.

Moving average
    Compute moving average of each selected image
    (implementation based on `scipy.ndimage.uniform_filter <https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html>`_).

Moving median
    Compute moving median of each selected image
    (implementation based on `scipy.signal.medfilt <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.medfilt.html>`_).

Wiener filter
    Compute Wiener filter of each selected image
    (implementation based on `scipy.signal.wiener <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.wiener.html>`_).

FFT
    Create a new image which is the Fast Fourier Transform (FFT)
    of each selected image.

Inverse FFT
    Create a new image which is the inverse FFT of each selected image.
