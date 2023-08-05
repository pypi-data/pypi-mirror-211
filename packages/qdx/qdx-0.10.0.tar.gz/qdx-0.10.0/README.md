# QDX-py: Python SDK for the QDX API

This package exposes a simple provider and CLI for the different tools exposed by the QDX GraphQL API.

## Usage

### As a library

``` python
import json
from pathlib import Path

import qdx
from  qdx.data import run_convert, QDXV1QCMol, QDXV1QCInput

URL = "url to the qdx api"
TOKEN = "your qdx access token"

# get our client to talk with the API
client = qdx.QDXProvider(url=URL, 
                         access_token=TOKEN)

# path to protein pdb with correct charges and protonation
protein_pdb = Path("./examples/4w9f_prepared_protein.pdb")
# path to ligand sdf with correct charges and protonation
ligand_sdf = Path("./examples/3JU_prepared.sdf")

# convert pdb to qdxf
protein_qdxf = client.obabel_to_complex(file=protein_pdb, format="pdb")
# convert ligand sdf to qdxf
ligand_qdxf = client.obabel_to_complex(file=ligand_sdf, format="sdf")

# We need to treat the ligand as a single fragment
ligand_qdxf["topology"]["fragments"] = [[ x for x, _ in enumerate(ligand_qdxf["topology"]["symbols"])]]
ligand_qdxf["topology"]["fragment_charges"] = [0]

# We also need to drop connectivity information (temporary)
ligand_qdxf["topology"]["connectivity"] = []

# fragment protein
fragged_protein = client.fragment_complex(protein_qdxf, backbone_steps=5)

# combine fragmented protein and ligand into a single complex
complex = client.combine_complexes(fragged_protein, ligand_qdxf)

# create a qdx/hermes input file for complex
qdx_input = qdx.data.run_convert(json.dumps(complex), "qdxcomplex2qdxv1")

# Configure input for lattice calculation
qdx_input.model.fragmentation = True
qdx_input.keywords.frag.lattice_energy_calc = True
# The reference monomer should be the final fragment,
# as that will be the ligand
qdx_input.keywords.frag.reference_monomer = len(
    qdx_input.molecule.fragments) - 1
qdx_input.keywords.frag.monomer_cutoff = 20
qdx_input.keywords.frag.dimer_cutoff = 10

qdx_input.model.method = "RIMP2"

# Start hermes calculation - 
# remember to set tags that reference your system
proc = client.start_quantum_energy_calculation(
    qdx_input, tags=["rimp2", "4w9f", "3ju", "manual_prep", "debug_charges"])


# Fetch results - you will have to run this multiple times until
# the calculation is done
result = client.get_proc(proc)
```


### As a CLI

``` sh
# All cli calls have these standard arguments, referred to as … in future examples
qdx --url QDX_API_URL --access-token QDX_ACCESS_TOKEN

# Post a hermes job, returning a task id
… --post-quantum-energy < ./path_to_qdxv1_input.json

# Retrieve the hermes job, or its progress
… --get-proc TASK_ID

## Other functions
# Return a qdx complex json object and save it as complex.json
… --pdb-to-complex PATH_TO_PDB_FILE > complex.json

# Prepare a protein for quauntum energy calculation
… --prepare-protein simulation --poll < ./complex.json > prepped_protein_complex.json

# Fragment a qdx complex json object
… --fragment-complex [MIN_STEPS_ALONG_PROTEIN_BACKBONE_BEFORE_CUTTING_AT_C-C_BOND] < prepped_protein_complex.json > fragmented_protein_complex.json

# Prepare a ligand for quauntum energy calculation
… --prepare-ligand simulation --poll < ./path_to_ligand.sdf > prepped_ligand_complex.json

# Combine protein and ligand complexes for simulation

… --combine-complexes ./prepped_protein_complex.json < ./prepped_ligand_complex.sdf > protein_ligand_complex.json

# Convert a qdx complex into a qdx input file
… --convert ./protein_ligand_complex.json --direction qdxcomplex2qdxv1 > qdx_input.json

# Convert a qdx complex into a exess input file
… --convert ./protein_ligand_complex.json --direction qdxcomplex2exess > exess_input.json

# Convert a qdx input file into an exess input file
… --convert qdx_input.json --direction qdxv12exess > exess_input.json
```

