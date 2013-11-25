molgenis-impute
===============

Rapid generation of genetic imputation scripts for grid/cluster/local environments


## About 
molgenis-impute is a tool for rapid generation and submission of scripts that perform genetic imputation. The generated scripts contain all rigorous quality control checks, data chunking, error handling and reporting. The tool is designed to be simple and straight-forward, for researchers that want to do imputation **now**, without limiting the available options of imputation tools.

molgenis-impute performs three main actions:
* liftover (from hg18 to hg19 genomic reference)
* phasing of a study panel
* imputation

## Requirements
molgenis-impute runs in any 64-bit x86 linux distribution and it requires the following tools:
* wget (or curl)
* tar
* unzip
* g++
* java 1.6 or higher
* python 2.7
* numpy

For example, to set up the environment in Ubuntu you can run:
```
sudo apt-get install -y git openjdk-6-jre g++ python-numpy unzip make zlib1g-dev 
```

Also note that imputation reference panels can take tens of GBs of disk space 

## Setup 
Initially, run the following to download all necessary tools for imputation:
```
python molgenis-impute.py --dl_tools
```

Then download a reference panel of your choice. To list all available reference panels for downloading, run: 
```
python molgenis-impute.py --list
```

To download a reference panel. Run:
```
python molgenis-impute.py --dl_reference < NAME >
```

where < NAME > is the name of the reference panel as provided by the --list option.

## Imputation study panel
A study panel should be in plink's PED and MAP format: http://pngu.mgh.harvard.edu/~purcell/plink/data.shtml . Moreover, the PED/MAP files should be splitted per chromosome and stored in a single directory. For example:

* my_study/chr1.ped
* my_study/chr1.map
* my_study/chr2.ped
* my_stydy/chr2.map
* ...

In this release we include a testing study panel in the directory: ```resources/GWAS/HapMap3/b36/``` . For information about how this study was prepared check the ```resources/GWAS/HapMap3/b36/README.txt``` file.

In molgenis-impute, in order to use a directory with a study panel in any of the analysis use the option: --study and provide the **root path** of that directory. For example:
```
python molgenis-impute.py --study /home/user/molgenis-impute/resources/GWAS/HapMap3/b36/ --action liftover --output /home/user/results
```

## Liftover
Liftovering is the process of changing the genomic assembly of a dataset from one version (usual older) to another (newer). To liftover a study panel from the hg18 genome assembly to hg19, run the following:
```
python molgenis-impute.py --study < STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action liftover
```
Under the hood molgenis-impute uses the liftOver tool from UCSC. The output will be stored in the directory defined with the ```--output``` option in ped/map format. The filenames will be:
* chr1.ped , chr1.map
* chr2.ped , chr2.map
* ...

The result of this process is in binary plink format.

## Phasing
Phasing is the process of determining the haplotype structure of genotype data. To phase a dataset it should be in PED/MAP format. The command is:
```
python molgenis-impute.py --study < STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action phase
```
Under the hood molgenis-impute uses the <a href="http://www.shapeit.fr/">SHAPEIT</a> tool. The output will be stored in the directory defined in the ```--output``` option in <a href="http://www.stats.ox.ac.uk/~marchini/software/gwas/file_format.html">genotype/sample</a> format.

## Impute
To impute a phased dataset run the following command:
```
python molgenis-impute.py --study < STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action impute --reference < REFERENCE NAME >
```
* ```< STUDY DIRECTORY >``` is the directory where the study panel exists. The study panel should be phased (preferrably with SHAPEIT) in the <a href="http://www.stats.ox.ac.uk/~marchini/software/gwas/file_format.html">genotype/sample</a> format. 
* ```< OUTPUT DIRECTORY>``` is the directory where the output will be stored
* ```< REFERENCE NAME >``` is the name of the reference panel that will be used for the imputation. To get a list of all reference panels available run:
```
python molgenis-impute.py --list
```

Under the hood molgenis-impute uses <a href="https://github.com/molgenis/systemsgenetics/tree/master/genotype-aligner">Genotype Aligner</a> for quality control and <a href="http://mathgen.stats.ox.ac.uk/impute/impute_v2.html">impute2</a> tool for imputation. 

The imputation task is split according many chunks. The split is 2-dimensional: according to genomic position and according to samples: 
* The genomic position split is per 5.000.000 distance. You can change this with the ```--position_batch_size``` option.
* The sample split is done so that each chunk should have approximately the same number of samples. The default setting is that each sample chunk should have at least 500 samples but not more than twice this value (1000=2*500). To change the default value of 500, use the ```--sample_batch_size```option. 

By default molgenis-impute will perform imputation for all chromosomes located in the reference panel. You can limit the imputation chromosomes with the option ```--chromosomes < comma separated values of chromosomes >``` For example: ```--chromosomes 1,3,8```

## Example
The molgenis-impute distribution includes an example study panel. This panel is part of the HapMap3 release 2 dataset and is located in the ```resources/GWAS/HapMap3/b36/``` directory. You can impute this dataset with GIANT release of 1000 Genomes Project by following the following steps (in the presented order). For these examples we assume that you have installed all necessary tools with the ```--dl_tools``` options and installed the reference panel with the ```--dl_reference GIANT.phase1_release_v3.20101123``` option.
* liftover from hg18 to hg19:
```
python molgenis-impute.py --study `pwd`/resource/GWAS/HapMap3/b36/ --output `pwd`/results_liftover --action liftover
```
* phase:
```
python molgenis-impute.py --study `pwd`/results_liftover --output `pwd`/results_phase --action phase
```
* impute:
```
python molgenis-impute.py --study `pwd`/results_phase --reference GIANT.phase1_release_v3.20101123 --output `pwd`/results_impute --action impute
```

The final results of this proccess will be at the ```results_impute``` directory. The ``` `pwd` ``` part in the paths is to make sure that the complete path from the root is included (pwd is the Linux command to Print the Working Directory).

## Add a new reference panel
To add a new reference panel create a new directory in ```resources/imputationReference```. The name of the directory will be the name of the new reference panel. In this directory, store the reference panel in compressed (with gzip) Variant Called Format (VCF). The files should have .vcf.gz extension. Moreover each chromosome should be in a separate file and the name of the file should have at any point a chr< CHROMOSOME NUMBER > part. The naming should be consistent for all files. For example:
* 1000GP_chr1.vcf.gz
* 1000GP_chr2.vcf.gz
* ...
Then run:
```
python molgenis-impute.py --add_reference
```
This checks the existence of the *.vcf.gz files in all new directories and makes the appropriate format coversions from compressed gzip to impute2's hap and legend files. You don't need to do anything else. 

Alternatively, if you want to install your own .hap and .legend files, you can place them in a new directory under ```resources/imputationReference```. Each chromosome should be in a separate pair of files. Moreover the files should be compressed with gzip and the files' extensions should be: .haps.gz and .legend.gz . For example: 1000_GP_chr1.haps.gz and 1000_GP_chr1.legend.gz

## Additional parameters
* ```--dl_tools```: set the installation directory for imputation tools. Default: < currrent working dir >/tools 
* ```--reference_dir```: set the installation directory for the imputation reference panels. Default: < currrent working dir >/resources/imputationReference
* ```--nosubmit```: Do not submit for execution the generated scripts. 

## License 
This software is under the Simplified BSD Licese.

## About
* Main development: 
    * <a href="alexandros.kanterakis@gmail.com">Alexandros Kanterakis</a>
* Contributors:
    * <a href="patrickdeelen@gmail.com">Patrick Deelen</a>
    * <a hreF="freerk.van.dijk@gmail.com">Freerk Van Dijk</a>
    * <a href="h.v.byelas@gmail.com">George Byelas</a>
    * <a href="m.dijkstra.work@gmail.com">Martijn Dijkstra</a>
* Supervision:
    * <a href="m.a.swertz@gmail.com">Morris Swertz</a>
* The code is also hosted in pypedia (http://www.pypedia.com/index.php/Imputation). To obtain the code of imputation.py from pypedia run:
```
curl http://www.pypedia.com/index.php?get_code=%23Imputation\(\)  > imputation.py 
```

## Contact 
Alexandros Kanterakis
<br><a href="alexandros.kanterakis@gmail.com">alexandros.kanterakis@gmail.com</a>
<br> Genetica 
<br> UMCG 
<br> Postbus 30 001 
<br> 9700 RB Groningen 
<br> The Netherlands


