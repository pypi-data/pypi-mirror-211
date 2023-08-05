import sys
from pathlib import Path
from typing import Literal, Optional, Union
import json

from datargs import argsclass, parse

from .calcq import run
from .data import QDXV1QCInput, QDXV1QCMol, run_convert
from .api import PrepTypes, QDXProvider


from typing import List


@argsclass(description="Post quantum energy")
class PostQuantumEnergy:
    input_data: Path
    tags: Optional[List[str]]


@argsclass(description="Prepare protein")
class PrepareProtein:
    input_data: Path
    prep_for: PrepTypes
    tags: Optional[List[str]]
    poll: Optional[bool]


@argsclass(description="Prepare ligand")
class PrepareLigand:
    input_data: Path
    prep_for: PrepTypes
    tags: Optional[List[str]]
    poll: Optional[bool]


@argsclass(description="Get quantum energy")
class GetQuantumEnergy:
    proc_id: str


@argsclass(description="Delete process")
class DeleteProc:
    proc_id: str


@argsclass(description="Tag process")
class TagProc:
    proc_id: str
    tags: List[str]


@argsclass(description="Untag process")
class UntagProc:
    proc_id: str
    tags: List[str]


@argsclass(description="Convert PDB to complex")
class PdbToComplex:
    pdb_path: Path


@argsclass(description="Combine complexes")
class CombineComplexes:
    combine_complexes: Path
    input_data: Path


@argsclass(description="Fragment complex")
class FragmentComplex:
    input_data: Path
    fragments: int


@argsclass(description="Charge fragments")
class ChargeFragments:
    input_data: Path


@argsclass(description="Convert between formats")
class Convert:
    input_data: Path
    direction: Literal[
        "qdxv12exess",
        "exess2qdxv1",
        "qdxcomplex2qdxv1",
        "qdxcomplex2exess",
        "qdxtopology2exess",
        "qdxtopology2qdxv1",
    ]
    lattice: Optional[int] = None


@argsclass(description="QDX CLI")
class QDXArgs:
    url: str
    access_token: str
    action: Union[
        PostQuantumEnergy,
        GetQuantumEnergy,
        DeleteProc,
        TagProc,
        UntagProc,
        PdbToComplex,
        FragmentComplex,
        ChargeFragments,
        Convert,
        PrepareProtein,
        PrepareLigand,
        CombineComplexes,
    ]


def handle_post_quantum_energy(provider: QDXProvider, action):
    with action.input_data.open() as f:
        return provider.start_quantum_energy_calculation(
            QDXV1QCInput.from_json(f.read()), tags=action.tags or []
        )


def handle_get_quantum_energy(provider: QDXProvider, action):
    return provider.get_proc(action.proc_id).to_json()


def handle_delete_proc(provider: QDXProvider, action):
    return provider.delete_proc(action.proc_id)


def handle_tag_proc(provider: QDXProvider, action):
    return provider.tag_proc(action.proc_id, action.tags or [])


def handle_untag_proc(provider: QDXProvider, action):
    results = []
    for tag in action.tags or []:
        results.append(provider.untag_proc(action.proc_id, tag))
    return results


def handle_pdb_to_complex(provider: QDXProvider, action):
    return json.dumps(provider.pdb_to_complex(action.pdb_path))


def handle_combine_complexes(provider: QDXProvider, action):
    with action.combine_complexes.open() as cc, action.input_data.open() as id:
        return json.dumps(provider.combine_complexes(json.loads(cc.read()), json.load(id)))


def handle_fragment_complex(provider: QDXProvider, action):
    with action.input_data.open() as f:
        return json.dumps(provider.fragment_complex(json.load(f), action.fragments))


def handle_charge_fragments(provider: QDXProvider, action):
    with action.input_data.open() as f:
        complex_data = json.load(f)
    topology = QDXV1QCMol().from_dict(complex_data["topology"])
    res = run(topology)
    return res.to_json() if res else None


def handle_convert(provider: QDXProvider, action: Convert):
    with action.input_data.open() as f:
        res = run_convert(f.read(), action.direction).to_dict()
        if action.lattice:
            keywords = res.get("keywords")
            if keywords is not None:
                keywords["frag"].update({"lattice_energy_calc": True})
                if action.lattice > 0:
                    keywords["frag"].update({"reference_monomer": action.lattice})
                else:
                    if action.direction.endswith("qdxv1"):
                        keywords["frag"].update(
                            {"reference_monomer": len(res["molecule"]["fragments"]) - int(action.lattice)}
                        )
                    else:
                        keywords["frag"].update(
                            {
                                "reference_monomer": max(res["molecule"]["fragments"]["fragid"])
                                - int(action.lattice)
                            }
                        )

        return json.dumps(res, indent=2)


def handle_prepare_protein(provider: QDXProvider, action):
    with action.input_data.open() as f:
        id = provider.start_protein_prep(json.load(f), prep_for=action.prep_for, tags=action.tags or [])
    return json.dumps(provider.poll_proc(id).data["term"]) if action.poll else id


def handle_prepare_ligand(provider: QDXProvider, action):
    with action.input_data.open() as f:
        id = provider.start_ligand_prep(f.read(), prep_for=action.prep_for, tags=action.tags or [])
    return json.dumps(provider.poll_proc(id).data["term"]) if action.poll else id


action_handler_map = {
    PostQuantumEnergy: handle_post_quantum_energy,
    GetQuantumEnergy: handle_get_quantum_energy,
    DeleteProc: handle_delete_proc,
    TagProc: handle_tag_proc,
    UntagProc: handle_untag_proc,
    PdbToComplex: handle_pdb_to_complex,
    CombineComplexes: handle_combine_complexes,
    FragmentComplex: handle_fragment_complex,
    ChargeFragments: handle_charge_fragments,
    Convert: handle_convert,
    PrepareProtein: handle_prepare_protein,
    PrepareLigand: handle_prepare_ligand,
}


def main():
    args = parse(QDXArgs)

    provider = QDXProvider(args.url, args.access_token)

    action = args.action
    handler = action_handler_map.get(type(action))

    if handler:
        result = handler(provider, action)
        if result:
            print(result)


if __name__ == "__main__":
    main()
