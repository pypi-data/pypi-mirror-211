# README

ODAMNet is a Python package to study molecular relationship between environmental factors (called chemicals here) and 
rare diseases. 

The [ODAMNet documentation][ODAMNet documentation] is available in ReadTheDocs.

This tool was created within the framework of the [EJRP-RD project][EJPRD].

## Installation 

### From PyPI

ODAMNet is available in [Python package][pypi]. You can easily install it using `pip`.

```console
$ python3 -m pip install odamnet
```

### From Conda

ODAMNet is also available in [bioconda][bioconda] using ``conda``.

```console
$ conda install odamnet
```

### From Github

1. Clone the repository from GitHub

```console
$ git clone https://github.com/MOohTus/ODAMNet.git
```

2. Then, install it

```console
$ python3 -m pip install -e ODAMNet/
```

*If it's not working, try to update pip using pip install pip --upgrade*

## Usage

Three different approaches are available: 

- Overlap analysis
- Active Modules Identification (AMI, using [DOMINO][DOMINO])
- Random Walk with Restart (RWR, using [multiXrank][multiXrank])

```console
$ odamnet [overlap|domino|multixrank|networkCreation|networkDownloading] [ARGS]
```

## Examples

Three approaches are implemented to study relationships between genes targeted by chemicals (retrieved automatically 
from the [Comparative Toxicogenomics Database][CTD] (CTD)) and rare diseases (retrieved automatically from 
[WikiPathways][WikiPathways]).

### Overlap analysis

The first approach computes the overlap between chemical target genes and rare disease pathways. It is looking for 
direct associations, i.e. chemical target genes that are part of rare disease pathways.

Give your chemicals list into `--chemicalsFile` input. 

```console
$ odamnet overlap --chemicalsFile FILENAME
```

### Active Module Identification (AMI)

The Active Module Identification is performed using DOMINO tool. 

DOMINO defines target genes as *active genes* to search for active modules using a biological network 
(e.g. protein-protein interaction network, PPI). Then, an overlap analysis is performed between identified active 
modules and rare disease pathways. 

Give your chemicals list and your biological network into `--chemicalsFile` and `--networkFile` respectively. 

```console
$ odamnet domino --chemicalsFile FILENAME --networkFile FILENAME
```

### Random Walk with Restart (RWR)

The Random Walk with Restart is performed using multiXrank Python package. This approach mesures the proximity of every node 
(e.g. genes and diseases) to the target genes within a multilayer network. The multilayer network is composed of genes networks 
and rare disease pathway network. Diseases and genes are linked using a bipartite.  

Give your chemicals list into `--chemicalsFile` input. 

MultiXrank needs a configuration file (`--configPath`), networks directory (`--networksPath`),
the target genes file (`--seedsFile`) and a name to write the result into network file (`--sifFileName`). 

```console
$ odamnet multixrank --chemicalsFile FILENAME --configPath PATH --networksPath PATH --seedsFile FILENAME --sifFileName FILENAME
```

*You can have more details about the configuration file in the [documentation page][doc].*

### Other functions

#### Network and bipartite creation

For the RWR, you should need to create a rare disease pathways network to integrate disease information into the multilayer.
ODAMNet creates a disconnected network (no connection between disease nodes) and its corresponding bipartite that connects 
diseases with genes that are involved in. 

Give a path to save generated disease network and disease-gene bipartite using `--networksPath` and `--bipartitePath`
respectively.

```console
$ odamnet networkCreation --networksPath PATH --bipartitePath PATH
```
*Rare disease pathways are retrieved automatically from WikiPathways.*

#### Network downloading

ODAMNet allows you to download automatically biological networks from [NDEx][NDEx] using the network ID (`--netUUID`). 
You can choose the network name file with `--networkFile`.

```console
$ odamnet networkDownloading --netUUID TEXT --networkFile FILENAME
```

[ODAMNet documentation]: https://odamnet.readthedocs.io/
[pypi]: https://pypi.org/project/ODAMNet/
[bioconda]: https://bioconda.github.io/index.html
[EJPRD]: https://www.ejprarediseases.org/
[DOMINO]: http://domino.cs.tau.ac.il
[multiXrank]: https://multixrank-doc.readthedocs.io/en/latest/index.html
[WikiPathways]: https://www.wikipathways.org/
[CTD]: https://ctdbase.org/
[NDEx]: https://www.ndexbio.org/
[doc]: https://odamnet.readthedocs.io/en/latest/pages/formats/Input.html#configuration-file
