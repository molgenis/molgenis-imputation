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
molgenis-impute runs in any 64-bit x86 Linux distribution and it requires the following tools:
* wget (or curl)
* tar
* unzip
* bunzip2
* g++
* java 1.6 or higher
* python 2.7
* numpy

For example, to set up the environment in Ubuntu you can run:
```
sudo apt-get update
sudo apt-get install -y git openjdk-6-jre g++ python-numpy unzip make zlib1g-dev 
```

Also note that imputation reference panels can take tens of GBs of disk space 

## Setup 
To install MOLGENIS-impute download the latest release from <a href="https://github.com/molgenis/molgenis-imputation/releases">here</a>.

For the .tar.gz file, uncompress it with: ```tar zxvf < FILENAME > ```. 
For the .zip file, uncompress it with: ```unzip < FILENAME > ```. 

To get the cutting edge latest version, clone this repository:
```
git clone https://github.com/kantale/molgenis-imputation.git 
```

Initially, run the following to download all necessary tools for imputation:
```
python molgenis-impute.py --dl_tools
```

By default the files will be installed in the molgenis_imputation directory in the current location. To change this use the ```--installation_dir < DIR >``` option.

The next step is to download a reference panel of your choice. To list all available reference panels either for direct use or for downloading, run: 
```
python molgenis-impute.py --list
```

To download a reference panel, run: (you can skip this step if you only want to use the pre-installed testing reference panel named "test_reference")
```
python molgenis-impute.py --dl_reference < NAME >
```

where < NAME > is the name of the reference panel as provided by the --list option.

this will install the reference panel to the default location: ```molgenis_imputation/resources/imputationReference```. To select a custom location use the ```--reference_dir < DIR > ``` option. 

Example:
```
python molgenis-impute.py --dl_reference GIANT.metabo.phase1_release_v3.20101123
```

*ATTENTION* This command will fail if you haven't installed the tools and datasets first, with the --dl_tools option. 

## Imputation study panel
A study panel should be in plink's PED and MAP format: http://pngu.mgh.harvard.edu/~purcell/plink/data.shtml . Moreover, the PED/MAP files should be splitted per chromosome and stored in a single directory. For example:

* my_study/chr1.ped
* my_study/chr1.map
* my_study/chr2.ped
* my_stydy/chr2.map
* ...

In this release we include a testing study panel in the directory: ```molgenis_imputation/resources/GWAS/small``` . For information about how this study was prepared check the ```molgenis_imputation/resources/GWAS/small/README.txt``` file.

In molgenis-impute, in order to use a directory with a study panel in any of the analysis use the option: --study and provide the **absolute path** of that directory. 

## Liftover (Step 1)
Liftovering is the process of changing the genomic assembly of a dataset from one version (usual older) to another (newer). To liftover a study panel from the hg18 genome assembly to hg19, run the following:
```
python molgenis-impute.py --study < STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action liftover
```
For Example:
```
python molgenis-impute.py --study `pwd`/molgenis_imputation/resources/GWAS/small/ --output `pwd`/results_liftover --action liftover
```

Under the hood molgenis-impute uses the liftOver tool from UCSC. The output will be stored in the directory defined with the ```--output``` option in ped/map format. The filenames will be:
* chr1.ped , chr1.map
* chr2.ped , chr2.map
* ...

The result of this process is in binary plink format.

## Phasing (Step 2)
Phasing is the process of determining the haplotype structure of genotype data. To phase a dataset it should be either in plink text format (PED/MAP) or binary (BED/BIM/FAM). The format is automatically detected. Moreover files should be **aligned in the hg19 genetic reference**. The command is:
```
python molgenis-impute.py --study < STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action phase
```
For example:
```
python molgenis-impute.py --study `pwd`/results_liftover --output `pwd`/results_phase --action phase
```
Under the hood molgenis-impute uses the <a href="http://www.shapeit.fr/">SHAPEIT</a> tool. The output will be stored in the directory defined in the ```--output``` option in <a href="http://www.stats.ox.ac.uk/~marchini/software/gwas/file_format.html">genotype/sample</a> format.

## Impute (Step 3)
To impute a phased dataset run the following command:
```
python molgenis-impute.py --study < PHASED STUDY DIRECTORY > --output < OUTPUT DIRECTORY >  --action impute --reference < REFERENCE NAME >
```
For example:
```
python molgenis-impute.py --study `pwd`/results_phase --reference test_reference --output `pwd`/results_impute --action impute
```

The options that this command takes are:
* ```< STUDY DIRECTORY >``` is the directory where the study panel exists. The study panel should be phased (preferrably with SHAPEIT) in the <a href="http://www.stats.ox.ac.uk/~marchini/software/gwas/file_format.html">genotype/sample</a> format. 
* ```< OUTPUT DIRECTORY>``` is the directory where the output will be stored
* ```< REFERENCE NAME >``` is the name of the reference panel that will be used for the imputation. To get a list of all reference panels available run:
```
python molgenis-impute.py --list
```

Under the hood molgenis-impute uses <a href="https://github.com/molgenis/systemsgenetics/tree/master/Genotype-Harmonizer">Genotype Harmonizer</a> for quality control and <a href="http://mathgen.stats.ox.ac.uk/impute/impute_v2.html">impute2</a> tool for imputation. 

The imputation task is split in many chunks. The split is 2-dimensional: according to genomic position and according to samples: 
* The genomic position split is per 5.000.000 distance. You can change this with the ```--position_batch_size``` option.
* The sample split is done so that each chunk should have approximately the same number of samples. The default setting is that each sample chunk should have at least 500 samples but not more than twice this value (1000=2*500). To change the default value of 500, use the ```--sample_batch_size```option. 

By default molgenis-impute will perform imputation for all chromosomes located in the reference panel. You can limit the imputation chromosomes with the option ```--chromosomes < comma separated values of chromosomes >``` For example: ```--chromosomes 1,3,8```

If the reference panel is not in the default directory (the < current directory >/resources/imputationReference). Define the custom directory with the ```--reference_dir``` parameter. For example the following options: ```--reference_dir /my/custom/dir --reference 1000GP``` will assume that the reference panel is installed in /my/custom/dir/1000GP directory. 

By default molgenis-impute assumes that java is in the PATH of the execution system. If this is not the case, use the option ```--java_executable``` to define the path to java executable. For example: ```--java_executable /path/to/java```

## Example
The molgenis-impute distribution includes an example study panel. This panel is part of the HapMap3 release 2 dataset (first 100 samples, first 10Mbp) and is located in the ```resources/GWAS/small``` directory. For more info about this test dataset you can take a look at resources/GWAS/small/README.md. You can impute this dataset with a subset of GIANT release of 1000 Genomes Project that is also included in the distribution in the directory ```resources/imputationReference/test_reference/```
* liftover from hg18 to hg19:

```
python molgenis-impute.py --study `pwd`/molgenis_imputation/resources/GWAS/small/ --output `pwd`/results_liftover --action liftover
```
* phase:

```
python molgenis-impute.py --study `pwd`/results_liftover --output `pwd`/results_phase --action phase
```
* impute:

```
python molgenis-impute.py --study `pwd`/results_phase --reference test_reference --output `pwd`/results_impute --action impute
```

The final results of this proccess will be at the ```results_impute``` directory. The ``` `pwd` ``` part in the paths is to make sure that the paths are absolute (pwd is the Linux command to Print the Working Directory).

## Add a new reference panel
To add a new reference panel create a new directory in ```molgenis_imputation/resources/imputationReference``` (or in any custom location in case you are using the ```--reference_dir``` option). The name of the directory will be the name of the new reference panel. In this directory, store the reference panel in Variant Called Format (VCF). The files should have .vcf extension. Moreover each chromosome should be in a separate file and the name of the file should have at any point a chr< CHROMOSOME NUMBER > part. The naming should be consistent for all files. For example:
* 1000GP_chr1.vcf
* 1000GP_chr2.vcf
* ...

You don't need to do anything else. The next time you run molgenis-impute.py it will detect the new files and do the appropriate conversions. Plase take note that some conversion take a considerable amount of time, specially for large vcf files. 

This is the recommended way for installing a new reference panel. Alternatively, if you want to install your own .haps and .legend files, you can place them in a new directory under ```molgenis_imputation/resources/imputationReference```. Each chromosome should be in a separate pair of files. If the files are uncompressed the extension should be .haps and .legend . Optionally, the files can be compressed with gzip and the files' extensions should be: .haps.gz and .legend.gz . For example: 1000_GP_chr1.haps.gz and 1000_GP_chr1.legend.gz. Finally either the .vcf or the compressed .vcf.gz should also exist in this directory for each chromosome. **IMPORTANT:** The .vcf.gz files should **not** be compressed with gzip, but with bgzip instead. bgzip is installed in tools/tabix-0.2.6/ . 

There are more alternative ways to install a reference panel. In general molgenis-impute supports the following reference panels formats:
* [SHAPEIT2 Format](http://www.shapeit.fr/pages/m02_formats/hapssample.html): Files should be per chromosome. Example: chr1_SHAPEIT.haps and chr1_SHAPEIT.sample (The _SHAPEIT part is necessary in order to make a distiction from impute2 .haps files)
* [Impute2 Format](http://mathgen.stats.ox.ac.uk/impute/impute_v2.html#-h): Files shoud be per chromosome. Example: chr1.haps , chr1.legend . There should also be a SINGLE .sample file. 
* [Impute2 Format](http://mathgen.stats.ox.ac.uk/impute/impute_v2.html#-h) compressed: Files should be per chromosome. Example: chr1.haps.gz , chr1.legend.gz . There should also be a SINGLE .sample file (not compressed). This is the default format of the reference panels available from impute2. For example: http://mathgen.stats.ox.ac.uk/impute/data_download_1000G_phase1_integrated_SHAPEIT2_9-12-13.html 
* VCF: A single vcf file.
* VCF compressed. A single compressed (with bgzip NOT gzip) vcf file. Example panel.vcf.gz

For all these files molgenis-compute will try to do its best to apply the appropriate conversions before performing imputation. If you have a special request or you notice a bug please let me know!

To make use of the new reference in the imputation step use the option --reference < REFERENCE_NAME >. The < REFERENCE_NAME > is the name of the created directory under ```molgenis_imputation/resources/imputationReference``` . (If unsure run python molgenis-impute.py --list for a list of available reference panels)

## Additional parameters
* ```--installation_dir```: set the installation directory for imputation tools and resources. Default: < currrent working dir >/molgenis_imputation 
* ```--reference_dir```: set the installation directory for the imputation reference panels. Default: < currrent working dir >/molgenis_imputation/resources/imputationReference
* ```--nosubmit```: Do not submit for execution the generated scripts. 
* ```--results```: Same as ```--output```

## Notes 
All scripts detect if the output files are in place and in case they are, the execution is skipped. This helps in cases when an execution get abruptly stopped, to resume from the last succesful execution step. By selecting a different results directory or deleting the generated results you can repeat the analysis.

## License 
This software is under the Simplified BSD Licese.

## About
* Main development: 
    * <a href="mailto:alexandros.kanterakis@gmail.com">Alexandros Kanterakis</a>
* Contributors:
    * <a href="mailto:patrickdeelen@gmail.com">Patrick Deelen</a>
    * <a href="mailto:freerk.van.dijk@gmail.com">Freerk Van Dijk</a>
    * <a href="mailto:h.v.byelas@gmail.com">George Byelas</a>
    * <a href="mailto:m.dijkstra.work@gmail.com">Martijn Dijkstra</a>
* Supervision:
    * <a href="mailto:m.a.swertz@gmail.com">Morris Swertz</a>
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


