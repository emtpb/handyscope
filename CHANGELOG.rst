*********
Changelog
*********

This project follows the guidelines of `Keep a changelog`_ and adheres to
`Semantic versioning`_.

.. _Keep a changelog: https://keepachangelog.com/
.. _Semantic versioning: https://semver.org/


`1.3.0`_ 2026-05-19
===================

Added
-----
* Add example scripts for the signal generator and oscilloscope functionalities

Changed
-------
* Change to pyproject.toml
* Migrate from deprecated pkg_resources to importlib

Fixed
-----
* Fix tests


`1.2.0`_ 2024-07-22
===================

Added
-----
* Support for non-amd64 Linux architectures.
* Slots to avoid accidental creation of dynamic properties.

Fixed
-----
* Minor bugs and documentation issues.
* Code formatting issues.


`1.1.0`_ 2023-26-04
===================

Added
-----
* Added additional properties
* Updated libtiepie to version 0.9.16.

Changed
-------
* Differentiate between 32 and 64 bit dlls on windows.
* API changes regarding generating callbacks.
* API changes when retrieving data from specified channels.
* Evaluate the trig holdoff in the measure method of the oscilloscope.

Fixed
-----
* Fix wrong library call for burst sample count.
* Some tests


`1.0.0`_ 2019-11-11
===================

Added
-----
* Initial implementation as already used in production.
* libtiepie version 0.6.3.


.. _1.3.0: https://github.com/emtpb/handyscope/releases/tag/1.3.0
.. _1.2.0: https://github.com/emtpb/handyscope/releases/tag/1.2.0
.. _1.1.0: https://github.com/emtpb/handyscope/releases/tag/1.1.0
.. _1.0.0: https://github.com/emtpb/handyscope/releases/tag/1.0.0
