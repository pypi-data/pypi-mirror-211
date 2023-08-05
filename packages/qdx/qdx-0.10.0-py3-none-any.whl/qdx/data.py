"""
Utilities for creating QC JSON files (https://molssi-qc-schema.readthedocs.io/en/latest/index.html)
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Literal, Optional

import dataclasses_json
from tap import Tap


@dataclass
class Vec3f(dataclasses_json.DataClassJsonMixin):
    """Vector for 3d coordinates."""

    x: float
    y: float
    z: float


@dataclass
class BindingSite(dataclasses_json.DataClassJsonMixin):
    """Details of a receptor binding site."""

    center: Vec3f
    size: Optional[Vec3f]


@dataclass
class FragAtom(dataclasses_json.DataClassJsonMixin):
    """Atom in a Fragment."""

    index: int  # internal index used for ordering
    element: str
    coords: list[float]
    neighbors: list[str]  # list of indexes for determining broken bonds
    residue: int


@dataclass
class Fragment(dataclasses_json.DataClassJsonMixin):
    """Represents sub-sections of a contigous molecular chain."""

    atoms: list[FragAtom]
    residues: list[tuple[int, Any]]

    first_atom_coords: str
    final_atom_coords: str

    charge: float


@dataclass
class Section(dataclasses_json.DataClassJsonMixin):
    """Represents different complete contiguous molecular chains - ie an unbroken protein chain."""

    atoms: list[FragAtom]
    residues: list[tuple[int, Any]]


QCMethods = Literal["RHF", "RIMP2"]

QCBasisSet = Literal[
    "STO-2G",
    "STO-3G",
    "STO-4G",
    "STO-5G",
    "STO-6G",
    "3-21G",
    "4-31G",
    "5-21G",
    "6-21G",
    "6-31G",
    "6-31G*",
    "6-31G**",
    "6-31+G",
    "6-31+G*",
    "6-31+G**",
    "6-31++G",
    "6-31++G*",
    "6-31++G**",
    "6-31G(2df,p)",
    "6-31G(3df,3pd)",
    "6-31G(d,p)",
    "6-311G",
    "6-311G*",
    "6-311G**",
    "6-311+G",
    "6-311+G*",
    "6-311+G**",
    "6-311++G",
    "6-311++G*",
    "6-311++G**",
    "6-311G(d,p)",
    "6-311G(2df,2pd)",
    "6-311+G(2d,p)",
    "6-311++G(2d,2p)",
    "6-311++G(3df,3pd)",
    "PCSeg-0",
    "PCSeg-1",
    "PCSeg-2",
    "cc-pVDZ-RIFIT",
    "aug-cc-pVDZ-RIFIT",
    "cc-pVTZ-RIFIT",
    "aug-cc-pVTZ-RIFIT",
    "cc-pVDZ",
    "aug-cc-pVDZ",
    "cc-pVTZ",
    "aug-cc-pVTZ",
]


class DataClassJsonMixin(dataclasses_json.DataClassJsonMixin):
    """Override dataclass mixin so that we don't have `"property": null,`s in our output"""

    dataclass_json_config = dataclasses_json.config(  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]


@dataclass
class QCJSONFragments(DataClassJsonMixin):
    """ "fragments" in qc json"""

    fragid: list[int] = field(default_factory=list)
    nfrag: int = 0
    broken_bonds: list[int] = field(default_factory=list)
    fragment_charges: list[int] = field(default_factory=list)
    frag_size: list[int] = field(default_factory=list)


@dataclass
class QCMol(DataClassJsonMixin):
    """ "molecule" in qc json"""

    geometry: list[float] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    fragments: QCJSONFragments = QCJSONFragments()


@dataclass
class QCModel(DataClassJsonMixin):
    """ "model" in qc json"""

    method: QCMethods = "RHF"
    fragmentation: bool = False
    basis: QCBasisSet = "6-31G*"
    aux_basis: str = "cc-pVDZ-RIFIT"


@dataclass
class QCSCF(DataClassJsonMixin):
    """ "keywords.scf" in qc json"""

    niter: int = 40
    ndiis: int = 12
    scf_conv: float = 1e-6
    dynamic_screening_threshold_exp: int = 10
    debug: bool | None = None
    convergence_metric: str = "diis"


@dataclass
class QCFrag(DataClassJsonMixin):
    """ "keywords.frag" in qc json"""

    reference_fragment: Optional[int] = None
    method: str = "MBE"
    fragmentation_level: int = 2
    ngpus_per_node: int = 4
    subset_of_fragments_to_calculate: Optional[list[int]] = None
    monomer_cutoff: int = 40
    monomer_mp2_cutoff: int = 40
    dimer_cutoff: int = 40
    dimer_mp2_cutoff: int = 40
    trimer_mp2_cutoff: int = 20
    lattice_energy_calc: bool = False
    trimer_cutoff: int = 30


@dataclass
class QCKeywords(DataClassJsonMixin):
    """ "keywords" in qc json"""

    scf: QCSCF = QCSCF()
    frag: QCFrag = QCFrag()


@dataclass
class QCInput(DataClassJsonMixin):
    """Final qc json input file"""

    molecule: QCMol = QCMol()
    model: QCModel = QCModel()
    keywords: QCKeywords = QCKeywords()
    driver: str = "energy"


@dataclass
class QDXV1QCMol(DataClassJsonMixin):
    """ "molecule" in qc json"""

    geometry: list[float] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    fragments: Optional[list[list[int]]] = field(default_factory=list)
    connectivity: Optional[list[tuple[int, int, int]]] = field(default_factory=list)
    fragment_charges: Optional[list[int]] = field(default_factory=list)


@dataclass
class QDXV1QCInput(DataClassJsonMixin):
    """Final qc json input file"""

    topology: QDXV1QCMol = QDXV1QCMol()
    model: QCModel = QCModel()
    keywords: QCKeywords = QCKeywords()
    driver: str = "energy"


@dataclass
class QCResults(DataClassJsonMixin):
    """Energy results parsed from an EXESS run"""

    calculated_fragments: int
    date: str
    final_hf_energy: float
    final_mp_energy: float
    nmer_distances: dict[str, float]
    nmer_hf_energies: dict[str, float]
    nmer_mp2_ss_energies: dict[str, float]
    nmer_mp2_os_energies: dict[str, float]
    input_file: str
    log_name: str
    num_atoms: int
    un_converged_fragments: int
    run_time: float
    xyzs: list[str]


@dataclass
class QDXV1Energy(DataClassJsonMixin):
    energy_type: Literal["lattice", "SPE"] | None  # Whether the calculation is lattice against a ref. monomer
    hf_total: float  # Final single-point energy (HF)
    mp_ss_total: float  # Final single-point energy correction (MP2 same-spin)
    mp_os_total: float  # Final single-point energy correction (MP2 opposite-spin)

    hf: list[float]  # HF energy per fragment group
    mp_ss: list[float]  # MP2 same-spin corrections per fragment group
    mp_os: list[float]  # MP2 opposite-spin corrections per fragment group
    n_mers: list[list[int]]  # Fragment groups
    n_mer_distances: list[float] | None  # Distances between fragments


TupleAtom = tuple[str, list[float]]


def qc_get_fragment_atoms(m: QCMol) -> list[list[TupleAtom]]:
    frags: list[list[TupleAtom]] = []
    for aidx, f in enumerate(m.fragments.fragid):
        while len(frags) < f:
            frags.append([])
        frags[f - 1].append((m.symbols[aidx], m.geometry[aidx * 3 : aidx * 3 + 3]))
    return frags


def exess_qc_mol_to_qdx_v1_mol(mol: QCMol) -> QDXV1QCMol:
    """Turns a Exess/Hermes molecule input object into a compliant qc input object"""
    frags: list[list[int]] = []
    for aidx, f in enumerate(mol.fragments.fragid):
        while len(frags) < f:
            frags.append([])
        frags[f - 1].append(aidx)
    bpairs = zip(*[iter(mol.fragments.broken_bonds)] * 2, strict=True)
    connectivity: list[tuple[int, int, int]] = [(x - 1, y - 1, 1) for x, y in bpairs]  # type: ignore
    return QDXV1QCMol(
        mol.geometry,
        mol.symbols,
        frags,
        connectivity,
        mol.fragments.fragment_charges,
    )


def qdx_v1_qc_mol_to_exess_mol(mol: QDXV1QCMol) -> QCMol:
    """Turns a compliant molecule input object into a Exess/Hermes qc input object.

    NOTE: only broken bonds will be retained as connectivity information
    """
    fragids = list(range(len(mol.symbols)))
    if mol.fragments:
        for i, frag in enumerate(mol.fragments):
            for j in frag:
                fragids[j] = i + 1
                # fragids.append(i + 1)
            # remove intra-fragment bonds
            if mol.connectivity:
                mol.connectivity = [x for x in mol.connectivity if x[0] not in frag or x[1] not in frag]

    broken_bonds = []

    if mol.connectivity:
        for a1, a2, _ in mol.connectivity:
            broken_bonds.extend([a1 + 1, a2 + 1])

    return QCMol(
        mol.geometry,
        mol.symbols,
        QCJSONFragments(
            fragids,
            len(mol.fragments or []),
            broken_bonds,
            mol.fragment_charges or [],
            [len(x) for x in mol.fragments or []],
        ),
    )


def qcresults_to_qdx_v1_energy(results: QCResults):
    n_mers = []
    hf = []
    mp_os = []
    mp_ss = []
    nmer_distances = []
    energy_type = "lattice"
    reference = None

    mp_os_total = 0
    mp_ss_total = 0

    for k, v in results.nmer_hf_energies.items():
        mers = list(map(int, k.split(":")))
        if len(mers) > 1:
            if reference:
                if reference != mers[0]:
                    energy_type = "SPE"
            else:
                reference = mers[0]

        n_mers.append(mers)
        hf.append(v)
        mp_os.append(results.nmer_mp2_os_energies.get(k))
        mp_ss.append(results.nmer_mp2_ss_energies.get(k))
        nmer_distances.append(results.nmer_distances.get(k))
        if len(mers) > 1:
            mp_os_total += results.nmer_mp2_os_energies.get(k) or 0
            mp_ss_total += results.nmer_mp2_ss_energies.get(k) or 0

    if energy_type != "lattice":
        mp_os_total = sum(results.nmer_mp2_os_energies.values())
        mp_ss_total = sum(results.nmer_mp2_ss_energies.values())

    return QDXV1Energy(
        energy_type=energy_type,
        hf_total=results.final_hf_energy,
        mp_os_total=mp_os_total,
        mp_ss_total=mp_ss_total,
        hf=hf,
        mp_os=mp_os,
        mp_ss=mp_ss,
        n_mers=n_mers,
        n_mer_distances=nmer_distances,
    )


class QCJsonArgs(Tap):
    input: Path
    direction: Literal["qdxv12exess", "exess2qdxv1", "qdxcomplex2qdxv1", "qdxcomplex2exess"]


def run_convert(
    data: str,
    direction: Literal[
        "qdxv12exess",
        "exess2qdxv1",
        "qdxcomplex2qdxv1",
        "qdxcomplex2exess",
        "qdxtopology2exess",
        "qdxtopology2qdxv1",
    ],
):
    """Convert between multiple exess/hermes formats."""
    match direction:
        case "qdxcomplex2qdxv1":
            input_json = json.loads(data)
            input = QDXV1QCMol.from_dict(input_json["topology"])
            return QDXV1QCInput(input, QCModel(), QCKeywords(QCSCF(), QCFrag(), QCRIMP2()))
        case "qdxcomplex2exess":
            input_json = json.loads(data)
            input = QDXV1QCMol.from_dict(input_json["topology"])
            n = qdx_v1_qc_mol_to_exess_mol(input)
            return QCInput(n, QCModel(), QCKeywords(QCSCF(), QCFrag(), QCRIMP2()))
        case "exess2qdxv1":
            input = QCInput.from_json(data)
            n = exess_qc_mol_to_qdx_v1_mol(input.molecule)
            return QDXV1QCInput(n, input.model, input.keywords, input.driver)
        case "qdxv12exess":
            input = QDXV1QCInput.from_json(data)
            n = qdx_v1_qc_mol_to_exess_mol(input.molecule)
            return QCInput(n, input.model, input.keywords, input.driver)
        case "qdxtopology2exess":
            input_json = json.loads(data)
            input = QDXV1QCMol.from_dict(input_json)
            n = qdx_v1_qc_mol_to_exess_mol(input)
            return QCInput(n, QCModel(), QCKeywords(QCSCF(), QCFrag(), QCRIMP2()))
        case "qdxtopology2exess":
            input_json = json.loads(data)
            input = QDXV1QCMol.from_dict(input_json)
            return QDXV1QCInput(input, QCModel(), QCKeywords(QCSCF(), QCFrag(), QCRIMP2()))
        case _:
            raise ValueError(f"Unknown direction {direction}")


def main():
    """Entrypoint to qdx format conversion helpers
    Parse arguments and write output to files
    """
    args = QCJsonArgs().parse_args()
    with open(args.input) as f:
        print(run_convert(f.read(), args.direction).to_json(indent=2))


if __name__ == "__main__":
    main()
