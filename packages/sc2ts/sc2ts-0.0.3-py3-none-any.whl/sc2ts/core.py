import pathlib
import collections.abc
import csv

import pyfaidx
import numpy as np

ALLELES = "ACGT-"

TIME_UNITS = "days"

REFERENCE_STRAIN = "Wuhan/Hu-1/2019"
REFERENCE_DATE = "2019-12-26"
REFERENCE_GENBANK = "MN908947"
REFERENCE_SEQUENCE_LENGTH = 29904

NODE_IS_MUTATION_OVERLAP = 1 << 21
NODE_IS_REVERSION_PUSH = 1 << 22
NODE_IS_RECOMBINANT = 1 << 23


__version__ = "undefined"
try:
    from . import _version

    __version__ = _version.version
except ImportError:
    pass


class FastaReader(collections.abc.Mapping):
    def __init__(self, path):
        self.reader = pyfaidx.Fasta(str(path))
        self.keys = list(self.reader.keys())

    def __getitem__(self, key):
        x = self.reader[key]
        h = np.array(x).astype(str)
        return np.append(["X"], h)

    def __iter__(self):
        return iter(self.keys)

    def __len__(self):
        return len(self.keys)


data_path = pathlib.Path(__file__).parent / "data"


def get_problematic_sites():
    return np.loadtxt(data_path / "problematic_sites.txt", dtype=np.int64)


__cached_reference = None


def get_reference_sequence():
    global __cached_reference
    if __cached_reference is None:
        reader = FastaReader(data_path / "reference.fasta")
        __cached_reference = reader[REFERENCE_GENBANK]
    return __cached_reference


__cached_genes = None


def get_gene_coordinates():
    global __cached_genes
    if __cached_genes is None:
        d = {}
        with open(data_path / "annotation.csv") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                d[row["gene"]] = (int(row["start"]), int(row["end"]))
        __cached_genes = d
    return __cached_genes
