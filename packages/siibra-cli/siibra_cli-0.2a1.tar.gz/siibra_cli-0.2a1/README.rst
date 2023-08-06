|License| 

siibracli - commandline client for interacting with brain atlases
=================================================================

Copyright 2020-2022, Forschungszentrum Jülich GmbH

*Authors: Big Data Analytics Group, Institute of Neuroscience and
Medicine (INM-1), Forschungszentrum Jülich GmbH*

.. intro-start

``siibra`` is a Python client for working with brain atlas frameworks
that integrate multiple brain parcellations and reference spaces across
different spatial scales, and connect them with a multimodal regional
data features. It aims to facilitate the programmatic and reproducible
incorporation of brain region features from different sources into
reproducible neuroscience workflows.

This repository implements a basic commandline interface (CLI) for siibra.

    **Note:** *``siibra-cli`` is still in development. While care is taken that it works reliably, its API is not yet stable and you may still encounter bugs when using it.*

``siibra`` provides structured acccess to parcellation schemes in
different brain reference spaces, including volumetric reference
templates at both macroscopic and microscopic resolutions as well as
surface representations. It supports both discretely labelled and
continuous (probabilistic) parcellation maps, which can be used to
assign brain regions to spatial locations and image signals, to retrieve
region-specific neuroscience datasets from multiple online repositories,
and to sample information from high-resolution image data. Among the
datasets anchored to brain regions are many different modalities from
in-vivo and post mortem studies, including regional information about
cell and transmitter receptor densties, structural and functional
connectivity, gene expressions, and more.

``siibra`` is mainly developed by the `Human Brain
Project <https://humanbrainproject.eu>`__ for accessing the `EBRAINS
human brain atlas <https://ebrains.eu/service/human-brain-atlas>`__. It
stores much of its contents in the `EBRAINS Knowledge
Graph <https://kg.ebrains.eu>`__, and is designed to support the
`OpenMINDS metadata
standards <https://github.com/HumanBrainProject/openMINDS_SANDS>`__. Its
functionalities include common actions known from the interactive viewer
``siibra explorer`` `hosted on
EBRAINS <https://atlases.ebrains.eu/viewer>`__. In fact, the viewer is a
good resource for exploring ``siibra``\ ’s core functionalities
interactively: Selecting different parcellations, browsing and searching
brain region hierarchies, downloading maps, identifying brain regions,
and accessing multimodal features and connectivity information
associated with brain regions. Feature queries in ``siibra`` are
parameterized by data modality and anatomical location, while the latter
could be a brain region, brain parcellation, or location in reference
space. Beyond the functionality of ``siibra-explorer``, the Python
library also supports a range of data analysis features suitable for
typical neuroscience workflows.

``siibra`` hides much of the complexity that would be required to
collect and interact with the individual paracellations,templates andd
data repositories. By encapsulating many aspects of interacting with
different maps and reference templates spaces, it also minimizes common
errors like misinterpretation of coordinates from different reference
spaces, mixing up label indices of brain regions, or utilisation of
inconsistent versions of parcellation maps. It aims to provide a safe
way of using maps defined across multiple spatial scales for
reproducible analysis.

.. intro-end

.. getting-started-start

Installation
------------

``siibra-cli`` is available on pypi. To install the latest released version,
simply run ``pip install siibra-cli``. In order to work with the latest
version from github, use
``pip install git+https://github.com/FZJ-INM1-BDA/siibra-cli.git@main``.

Access to EBRAINS
-----------------

``siibra`` retrieves much of its data from the `EBRAINS Knowledge
Graph <https://kg.ebrains.eu>`__, which requires authentication.
Therefore you have to provide an EBRAINS authentication token for using
all features provided by ``siibra``. Please make sure that you have a
valid EBRAINS user account by `registering to
EBRAINS <https://ebrains.eu/register/>`__. 

Help
----

If you run into issues, please open a ticket on `EBRAINS
support <https://ebrains.eu/support/>`__ or directly file bugs and
feature requests on
`github <https://github.com/FZJ-INM1-BDA/siibra-cli/issues>`__.

.. getting-started-end

.. acknowledgments-start

Acknowledgements
----------------

This software code is funded from the European Union’s Horizon 2020
Framework Programme for Research and Innovation under the Specific Grant
Agreement No. 945539 (Human Brain Project SGA3).

.. acknowledgments-end

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
