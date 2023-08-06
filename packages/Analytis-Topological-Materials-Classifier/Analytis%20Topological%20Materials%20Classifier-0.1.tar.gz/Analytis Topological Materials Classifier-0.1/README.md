# Overview
We are following the Topological Quantum Chemistry option detailed here:
[BCSD Magnetic Topological Material Classifier](https://www.cryst.ehu.es/cgi-bin/cryst/programs/magnetictopo.pl?tipog=gmag)

The objective is to take in a material and tell if DFT calculations indicate that this exhibits a symmetry-indicated topological phase.  The workflow goes as:

1. Run DFT calculation for bands including magnetic structure using DFT submission generator
2. Figure out the Magnetic Space Group using [findsym](https://iso.byu.edu/iso/findsym.php)
3. Generate input file (trace.txt), Mvasp2trace or irvsp.
4. Put input file into the above classifier
5. Output results in a nice way
    * VESTA file with magnetic ground structure

# Examples
ErVO3_NLC.txt
LiFeP2O7_LCEBR.txt 
Nd2CuO4_SEBR.txt 
U3As4_ES.txt



# Alternatives to this approach
The Mvasp2trace option only uses VASP files and does not talk to Quantum Espresso.   However, the Quantum Espresso output files can be converted to VASP files using [QE-to-VASP.py](src/QE-to-VASP.py)

In addition, [Atomsk](https://atomsk.univ-lille.fr/) has been used to interface between Quantum Espresso codes.

Many of the calculations that help the calculations backend is described in these two works:
[Representations in Magnetic Systems](https://arxiv.org/abs/1706.09272)
[Magnetic Topological Quantum Chemistry](https://www.nature.com/articles/s41467-021-26241-8)

The previous iterations for create input files to the TQC classifier are: 

* irRep [Github](https://github.com/stepan-tsirkin/irrep), [Paper](https://www.sciencedirect.com/science/article/abs/pii/S0010465521003386?via%3Dihub)
* irvsp [Github](https://github.com/zjwang11/irvsp/blob/master/src_irvsp_v2.tar.gz), [Paper](https://arxiv.org/abs/2002.04032), [Installation](https://ashour.dev/DFT+Technical/Compiling+irvsp)
* qeirreps [Github](https://github.com/qeirreps/qeirreps), [Paper](https://arxiv.org/abs/2006.00194)


Other _classification schemes_ exist here:
* Gao et. al implementation [Online Calculator](http://tm.iphy.ac.cn/TopMat_1651msg.html), [Paper](http://tm.iphy.ac.cn/TopMat_1651msg.html)
* Omar Ashour's Z2/Z4 index calculation for Time Reversal Symmetric and/or Inversion symmetric systems [Github](https://github.com/oashour/AbInitioTopo.jl)

# Resources
For more information on Magnetic Space Groups, see:
[BYU Magnetic Space Groups](https://stokes.byu.edu/iso/magneticspacegroupshelp.php)
[Wyckoff Postion Nomenclature](https://www.iucr.org/news/newsletter/volume-28/number-1/not-so-elementary,-my-dear-wyckoff)



