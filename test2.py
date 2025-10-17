from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer(filename='input.pdb')
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens()
PDBFile.writeFile(fixer.topology, fixer.positions, open('input_fixed.pdb', 'w'))
