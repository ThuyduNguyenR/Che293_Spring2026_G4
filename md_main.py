import nglview as ng
import os
import webbrowser
import shutil

#gmx_path = '/home/nina/miniconda3/bin.AVX2_256/gmx'

if shutil.which('gmx') is None:
    gmx_path = os.getenv('gmx_path', '/home/nina/miniconda3/bin.AVX2_256/gmx')
else:
    gmx_path = shutil.which('gmx')

main_dir = os.getcwd()

class Protein:
    def __init__(self, pdbID, forcefield):
        self.pdbID = pdbID
        self.ff = forcefield

    def process(self):
        self.clean()
        self.generate()
        self.container()
        self.solvate()
        self.visProt_sol()

    def createAllView(self):
        view1 = ng.show_structure_file("{0}/{0}.pdb".format(self.pdbID))
        view2 = ng.show_structure_file("{0}/{0}_protein.pdb".format(self.pdbID))
        view3 = ng.show_structure_file("{0}/{0}_solv_viz.gro".format(self.pdbID))
        view3.add_representation(repr_type='ball+stick', selection='SOL')
        view3.camera = 'orthographic'
        return (view1, view2, view3)

    def writeAllHTML(self):
        views = self.createAllView()
        for x in range(len(views)):
            html_file = os.path.abspath("{0}/{1}.html".format(self.pdbID, self.pdbID+'_'+str(x)))
            ng.write_html(html_file, [views[x]])

    def viewColab(self, filename):
        view = ng.show_structure_file("{0}/{1}".format(self.pdbID, filename))
        view

    def viewHTML(self, html_file):
        webbrowser.open(f"{html_file}")

    def clean(self):
        os.system('grep -v HETATM {0}/{0}.pdb > {0}/{0}_protein_tmp.pdb'.format(self.pdbID))
        os.system('grep -v CONECT {0}/{0}_protein_tmp.pdb > {0}/{0}_protein.pdb'.format(self.pdbID))

    def generate(self):
        os.system(
            gmx_path + ' pdb2gmx -f {0}/{0}_protein.pdb -o {0}/{0}_processed.gro -p {0}/topol.top -i {0}/posre.itp -water tip3p -ff "{1}"'.format(self.pdbID, self.ff)
        )

    def container(self):
        os.system(
            gmx_path + ' editconf -f {0}/{0}_processed.gro -o {0}/{0}_newbox.gro -c -d 1.0 -bt dodecahedron'.format(self.pdbID)
        )

    def solvate(self):
        os.system(
            gmx_path + ' solvate -cp {0}/{0}_newbox.gro -cs spc216.gro -o {0}/{0}_solv.gro -p {0}/topol.top'.format(self.pdbID)
        )

    def visProt_sol(self):
        os.system(
            'sed -i "s|./{0}|{1}/{0}|g" {2}/topol.top'.format(self.ff, main_dir, self.pdbID)
        )
        os.system('touch {0}/viz.mdp'.format(self.pdbID))
        os.system(gmx_path + ' grompp -f {0}/viz.mdp -c {0}/{0}_solv.gro -p {0}/topol.top -o {0}/topol.tpr'.format(self.pdbID))
        os.system('printf "0\n" | ' + gmx_path + ' trjconv -f {0}/{0}_solv.gro -s {0}/topol.tpr -o {0}/{0}_solv_viz.gro -pbc mol -ur compact'.format(self.pdbID))


# prot = Protein("4ZZI", "charmm36-feb2026_cgenff-5.0")
# prot.process()
# prot.writeAllHTML()
# prot.viewHTML('4ZZI/4ZZI_0.html')