
"""
molgenis-impute v.0.7.0
Alexandros Kanterakis, alexandros.kanterakis@gmail.com

Please read README.md for documentation.

"""

import re
import os
import glob
import uuid
import argparse

from subprocess import call

defaults = {

	'current_job_id' : None,
	'molgenis_compute_sh' : 'molgenis-compute/molgenis-compute-core-0.0.1-SNAPSHOT/molgenis_compute.sh',

	'liftover_pipeline_dir' : 'molgenis-pipelines-master/compute5/Liftover_genome_build_PEDMAP',
	'phase_pipeline_dir' : 'molgenis-pipelines-master/compute5/Imputation_shapeit_phasing',
	'impute_pipeline_dir' : 'molgenis-pipelines-master/compute5/Imputation_impute2',

	'study_example' : 'resources/GWAS/HapMap3/b36',
	'hg18tohg19_chain' : 'resources/liftover/hg18ToHg19.over.chain',

	'liftover_results_dir' : 'results/liftover',
	'phase_results_dir' : 'results/phase',
	'impute_results_dir' : 'results/impute',

	'generated_liftover_dir' : 'generated/liftover',
	'generated_phase_dir' : 'generated/phase',
	'generated_impute_dir' : 'generated/impute',

	'genetic_map' : 'resources/genetic_map/genetic_map_chr${chr}_combined_b37.txt',
	'phase_results_dir' : 'results/phasing',

	'cwd' : os.getcwd(),
	'tools_dir' : 'tools',
	'files_link' : 'http://molgenis26.target.rug.nl/downloads/molgenis-impute-files.tgz',
	'files_file' : 'molgenis-impute-files.tgz',
	'reference_dir' : 'resources/imputationReference',
	'shapeit_link' : 'http://www.shapeit.fr/script/get.php?id=18',
	'shapeit_file' : 'shapeit.v2.r644.linux.x86_64.tgz',
	'shapeit_dir' : 'shapeit.v2.r644.linux.x86_64',
	'impute2_link' : 'http://mathgen.stats.ox.ac.uk/impute/impute_v2.3.0_x86_64_static.tgz',
	'impute2_file' : 'impute_v2.3.0_x86_64_static.tgz',
	'impute2_dir' : 'impute_v2.3.0_x86_64_static',
	'liftover_link' : 'http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/liftOver',
	'liftover_file' : 'liftOver',
	'liftover_dir' : 'liftOverUcsc-20120905',
	'plink_link' : 'http://pngu.mgh.harvard.edu/~purcell/plink/dist/plink-1.07-x86_64.zip',
	'plink_file' : 'plink-1.07-x86_64.zip',
	'plink_dir' : 'plink-1.07-x86_64',
	'vcftools_link' : 'http://downloads.sourceforge.net/project/vcftools/vcftools_0.1.11.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fvcftools%2Ffiles%2F&ts=1374814925&use_mirror=heanet',
	'vcftools_file' : 'vcftools_0.1.11.tar.gz',
	'vcftools_dir' : 'vcftools_0.1.11',
	'genotypeAligner_link' : 'http://www.molgenis.org/jenkins/job/systemsgenetics/nl.systemsgenetics%24genotype-aligner/lastBuild/artifact/nl.systemsgenetics/genotype-aligner/1.1.0/genotype-aligner-1.1.1-jar-with-dependencies.jar',
	'genotypeAligner_file' : 'GenotypeAligner.jar',
	'genotypeAligner_dir' : 'genotype_aligner/GenotypeAligner-1.1.1',

	'reference_panels' : [
		('GIANT.phase1_release_v3.20101123', 
			"""
	Reduced GIANT all population panel (monomorphic and singleton sites, 1092 individuals)
	Dataset description taken from: http://genome.sph.umich.edu/wiki/Minimac:_1000_Genomes_Imputation_Cookbook
	Link: ftp://share.sph.umich.edu/1000genomes/fullProject/2012.03.14/GIANT.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz
			"""
		),
		('GIANT.metabo.phase1_release_v3.20101123',
			"""
	Metabochip (http://www.plosgenetics.org/article/info%3Adoi%2F10.1371%2Fjournal.pgen.1002793) specific reference panel. This reduced reference panel is a time saver, since it focuses on the well-imputable fine-mapping regions.
 	Dataset description taken from: http://genome.sph.umich.edu/wiki/Minimac:_1000_Genomes_Imputation_Cookbook 
	Link: ftp://share.sph.umich.edu/1000genomes/fullProject/2012.03.14/GIANT.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz
			"""
		),
		],

	#Link is available here: http://genome.sph.umich.edu/wiki/Minimac:_1000_Genomes_Imputation_Cookbook
	'GIANT.phase1_release_v3.20101123_link' : 'ftp://share.sph.umich.edu/1000genomes/fullProject/2012.03.14/GIANT.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz',
	'GIANT.phase1_release_v3.20101123_dir' : 'GIANT.phase1_release_v3.20101123',
	'GIANT.phase1_release_v3.20101123_file' : 'GIANT.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz',
	'GIANT.phase1_release_v3.20101123_vcfgz' : 'chr@CHR@.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz',
	'GIANT.phase1_release_v3.20101123_hapsgz' : 'chr@CHR@.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.haps.gz',
	'GIANT.phase1_release_v3.20101123_legendgz' : 'chr@CHR@.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.legend.gz',
	'GIANT.phase1_release_v3.20101123_actions' : 'cdreference_mkdir_dldir_untardir_cdcwd_convertVCF2Impute2',

	#Link is available here: http://genome.sph.umich.edu/wiki/Minimac:_1000_Genomes_Imputation_Cookbook
	'GIANT.metabo.phase1_release_v3.20101123_link' : 'ftp://share.sph.umich.edu/1000genomes/fullProject/2012.03.14/GIANT.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz',
	'GIANT.metabo.phase1_release_v3.20101123_dir' : 'GIANT.metabo.phase1_release_v3.20101123',
	'GIANT.metabo.phase1_release_v3.20101123_file' : 'GIANT.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz.tgz',
	'GIANT.metabo.phase1_release_v3.20101123_vcfgz' : 'chr@CHR@.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.vcf.gz',
	'GIANT.metabo.phase1_release_v3.20101123_hapsgz' : 'chr@CHR@.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.haps.gz',
	'GIANT.metabo.phase1_release_v3.20101123_legendgz' : 'chr@CHR@.metabo.phase1_release_v3.20101123.snps_indels_svs.genotypes.refpanel.ALL.legend.gz',
	'GIANT.metabo.phase1_release_v3.20101123_actions' : 'cdreference_mkdir_dldir_untardir_cdcwd_convertVCF2Impute2',

	#Also available from here: http://genome.sph.umich.edu/wiki/Minimac:_1000_Genomes_Imputation_Cookbook
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_link' : 'http://mathgen.stats.ox.ac.uk/impute/ALL_1000G_phase1integrated_v3_impute_macGT1.tgz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_dir' : 'ALL_1000G_phase1integrated_v3_impute_macGT1',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_file' : 'ALL_1000G_phase1integrated_v3_impute_macGT1.tgz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_hapgz' : 'ALL_1000G_phase1integrated_v3_chr@CHR@_impute_macGT1.hap.gz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_legendgz' : 'ALL_1000G_phase1integrated_v3_chr@CHR@_impute_macGT1.legend.gz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1_actions' : 'cdreference_dl_untar_mkdirImpute2_mv_cdcwd_gunzip2IMPUTE2',

	#Source http://mathgen.stats.ox.ac.uk/impute/data_download_1000G_phase1_integrated.html
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_link' : 'http://mathgen.stats.ox.ac.uk/impute/ALL_1000G_phase1integrated_v3_impute.tgz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_dir' : 'ALL_1000G_phase1integrated_v3_impute',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_file' : 'ALL_1000G_phase1integrated_v3_impute.tgz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_hapgz' : 'ALL_1000G_phase1integrated_v3_chr@CHR@_impute.hap.gz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_legendgz' : 'ALL_1000G_phase1integrated_v3_chr@CHR@_impute.legend.gz',
#	'1000GP_ALL_1000G_phase1integrated_v3_impute_actions' : 'cdreference_dl_untar_mkdirImpute2_mv_cdcwd_gunzip2IMPUTE2',
	
	#ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/
#	'1000GP_phase1_release_v3.20101123.snps_indels_svs' : 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/',

	#Chromosome length
	"b37_chr_1" : 249250621,
	"b37_chr_2" : 243199373,
	"b37_chr_3" : 198022430,
	"b37_chr_4" : 191154276,
	"b37_chr_5" : 180915260,
	"b37_chr_6" : 171115067,
	"b37_chr_7" : 159138663,
	"b37_chr_8" : 146364022,
	"b37_chr_9" : 141213431,
	"b37_chr_10" : 135534747,
	"b37_chr_11" : 134996516,
	"b37_chr_12" : 133851895,
	"b37_chr_13" : 115169878,
	"b37_chr_14" : 107349540,
	"b37_chr_15" : 102531392,
	"b37_chr_16" : 90354753,
	"b37_chr_17" : 81195210,
	"b37_chr_18" : 78077248,
	"b37_chr_19" : 59128983,
	"b37_chr_20" : 63025520,
	"b37_chr_21" : 48129895,
	"b37_chr_22" : 51304566,
}


def get_reference_files(dir, extension):
	"""
	Get a stem for all files in a directory.
	Replace chrXX references, with @CHR@
	"""

	reference_q = os.path.join(dir, '*.' + extension)
	reference_files = glob.glob(reference_q)
	if not reference_files:
		print 'Warning: Could not find *.%s files in custom reference directory: %s' % (extension, dir)
		return
	reference_filenames = [os.path.split(x)[1] for x in reference_files]
	#Check if there is a chromosome identifer in the filenames
	stem_d = {}
	for reference_filename in reference_filenames:
		s = re.search(r'chr([\d]+)', reference_filename)
		if s:
			chromosome = s.group(1)
			if int(chromosome) in range(1,23):
				stem = reference_filename.replace('chr' + chromosome, 'chr@CHR@')
				if stem_d.has_key(chromosome):
					print 'Warning: Do not know which if these two files is a proper %s file for chromosome %s: %s, %s' % (extension, chromosome, stem[chromosome][1], reference_filename)
					return
				else:
					stem_d[chromosome] = stem
	#Check if all stems are the same:
	stem_set = set([values for values in stem_d.itervalues()])
	if len(stem_set) > 1:
		print 'Warning: the \'chr<chromosome>\' part in the name of the *.%s files should be in the same position for all the files' % (extension)
		print 'These are not the same:'
		print '\n'.join(stem_set)
		return
	if len(stem_set) == 0:
 		print 'Warning: could not find any chr<chromosome> part in *.%s files' % (extension)
		return

	return list(stem_set)[0] 


def add_custom_reference_panels(verbose=False):
	"""
	Searches for reference panels that are not in the defaults dictionary.
	If any found, it is added
	"""

	global defaults

	reference_panels = [x[0] for x in defaults['reference_panels']]

	for dir_entry in glob.glob(os.path.join(defaults['reference_dir'], '*')):
		if os.path.isdir(dir_entry):
			reference_name = os.path.split(dir_entry)[1]
			if reference_name not in reference_panels:
				#Try to add this to the reference panels
				if verbose:
					print 'Adding custom reference: ' + reference_name
				defaults[reference_name + '_dir' ] = reference_name
				for extension, ext_name in [('vcf.gz', '_vcfgz'), ('haps.gz', '_hapsgz'), ('legend.gz', '_legendgz')]:
					stem = get_reference_files(dir_entry, extension)
					if stem:
						defaults[reference_name + ext_name] = stem

def setup_download_command():
	"""
	Assess which download command is available in the system
	"""
	global defaults

	#Check if wget exists..
	if which('wget'):
		download_command = lambda link, output_file : 'wget -O %s %s' % (output_file, link)
	elif which('curl'):
		#download_command = lambda link, output_file : 'curl %s > %s' % (link, output_file)
		download_command = lambda link, output_file : (system, ['curl %s' % (link)], {'stdout' : output_file})
	else:
		raise Exception('Error: At least one of the wget or curl tools should be installed')

	defaults['download_command'] = download_command

def which(program):
	"""
	Emulates the behavior of the unix 'which' command
	Code taken and adjusted from here: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
	"""

	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

def system(command, stdout=None, verbose=False, dummy=False):
	"""
	Execute a system command and return the return code
	command should be a string
	"""

	if verbose:
		print 'Running:', command
		if stdout:
			print '   Saving to file:', stdout

	stdf = None
	if stdout:
		stdf = open(stdout, 'wb')

	ret = 0
	if not dummy:
		ret = call(command.split(), stdout=stdf)

	if stdf:
		stdf.close()

	return ret

def system_many(commands, stdout=None, verbose=False, dummy=False):
	"""
	Executes a list of commands. Stops if the commands returns a non-zero code
	"""
	for command in commands:

		command_type = type(command).__name__ 
		if command_type == 'str':
			ret = system(command, stdout=stdout, verbose=verbose, dummy=dummy)

			if ret:
				raise Exception('Problem while running: %s' % command)

		elif command_type == 'tuple':
			if len(command) == 2:
				command[0](**command[1])
			elif len(command) == 3:
				command[0](*command[1], **command[2])
			else:
				raise Exception('Don\'t know how to run: ' + str(command)) 

		else:
			raise Exception('Internal error: Malformated command: ' + str(command))

def mkdir(dir_name, verbose=False):
	"""
	Make directory
	"""

	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
		if verbose:
			print 'Created directory:', dir_name

	else:
		if verbose:
			print 'Directory: %s already exists.' % dir_name

def chdir(dir_name, verbose=False):
	"""
	Change directory
	"""

	os.chdir(dir_name)

	if verbose:
		print 'Changed dir:', dir_name

def check_file_exists(file_name, verbose = False):
	"""
	Check if a file exists
	"""

	if not os.path.isfile(file_name):
		raise Exception('File: ' + file_name + ' does not exist.')

def convert_vcf_to_Impute2(input_vcf_filename, output_Impute2_stem, verbose=False):
	"""
	Forms the command with vcftools that convert vcf files to Impute2
	"""

	global defaults

	command = []
	command += [os.path.join(defaults['tools_dir'], defaults['vcftools_dir'], 'bin', 'vcftools')]
	command += ['--gzvcf']
	command += [input_vcf_filename]
	command += ['--IMPUTE']
	command += ['--out']
	command += [output_Impute2_stem]

	return ' '.join(command)

def gunzip_to_IMPUTE2(input_gzip_file, output_filename, verbose=False):
	"""
	Forms the command to gunzip a reference panel in IMPUTE2 format
	"""

	check_command_if_exists('gunzip', verbose=verbose)

	command = []
	command += ['gunzip']
	command += ['-c']
	command += [input_gzip_file]
	command += ['>']
	command += [output_filename]

	return (system, [' '.join(command[0:3])], {'stdout' : command[4], 'verbose' : verbose})

def install_tool(tool_name, install_actions, verbose=False, dummy=False):
	"""
	Runs the usual scripts needed to install a linux application
	"""

	if verbose:
		print 'Installing tool:', tool_name

	setup_download_command()

	commands = []
	for action in install_actions.split('_'):

		if action == 'cdtools':
			commands += [(chdir, {'dir_name' : defaults['tools_dir'], 'verbose' : verbose})]
		elif action == 'cdtooldir':
			commands += [(chdir, {'dir_name' : defaults[tool_name + '_dir'], 'verbose' : verbose})]
		elif action == 'checkfileexists':
			commands += [(check_file_exists, {'file_name' : defaults[tool_name + '_file'], 'verbose' : verbose})]
		elif action == 'cdreference':
			commands += [(chdir, {'dir_name' : defaults['reference_dir'], 'verbose' : verbose})]
		elif action == 'cdcwd':
			commands += [(chdir, {'dir_name' : defaults['cwd'], 'verbose' : verbose})]
		elif action == 'mkdir':
			commands += [(mkdir, {'dir_name' : defaults[tool_name + '_dir'], 'verbose' : verbose})] #Mkdir
		elif action == 'dl':
			commands += [defaults['download_command'](defaults[tool_name + '_link'], defaults[tool_name + '_file'])]   #Download file
		elif action == 'dldir':
			commands += [defaults['download_command'](defaults[tool_name + '_link'], os.path.join(defaults[tool_name + '_dir'], defaults[tool_name + '_file']))]   #Download file
		elif action == 'untar':
			commands += ['tar zxvf %s' % defaults[tool_name + '_file']] # Untar file
		elif action == 'untardir':
			commands += ['tar zxvf %s -C %s' % (os.path.join(defaults[tool_name + '_dir'], defaults[tool_name + '_file']), defaults[tool_name + '_dir'])] # Untar file
		elif action == 'unzip':
			commands += ['unzip %s' % defaults[tool_name + '_file']] #Unzip file
		elif action == 'mv':
			commands += ['mv %s %s' % (defaults[tool_name + '_file'], os.path.join(defaults[tool_name + '_dir'], defaults[tool_name + '_file']))]
		elif action == 'makeexecdir':
			commands += ['chmod a+x %s' % os.path.join(defaults[tool_name + '_dir'], defaults[tool_name + '_file'])]
		elif action == 'make':
			commands += [(chdir, {'dir_name' : defaults[tool_name + '_dir'], 'verbose' : verbose})]
			commands += ['make']
			commands += [(chdir, {'dir_name' : '..', 'verbose' : verbose})]
		elif action == 'convertVCF2Impute2':
			vcftools_output_chr = os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], defaults[tool_name + '_haps'].replace('.haps', ''))
			commands += [convert_vcf_to_Impute2(input_vcf_filename = os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], defaults[tool_name + '_vcfgz'].replace('@CHR@', str(chromosome))), output_Impute2_stem = vcftools_output_chr.replace('@CHR@', str(chromosome))) for chromosome in range(1, 23)]
			commands += [('mv %s.impute.hap %s.haps' % (vcftools_output_chr, vcftools_output_chr)).replace('@CHR@', str(chromosome)) for chromosome in range(1,23)]
			commands += [('mv %s.impute.legend %s.legend' % (vcftools_output_chr, vcftools_output_chr)).replace('@CHR@', str(chromosome)) for chromosome in range(1,23)]
			commands += [('gzip %s.haps' % (vcftools_output_chr)).replace('@CHR@', str(chromosome)) for chromosome in range(1,23)]
			commands += [('gzip %s.legend' % (vcftools_output_chr)).replace('@CHR@', str(chromosome)) for chromosome in range(1,23)]
		elif action == 'gunzip2IMPUTE2':
			commands += [gunzip_to_IMPUTE2(os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], defaults[tool_name + '_hapgz'].replace('@CHR@', str(chromosome))), os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], 'Impute2', str(chromosome) + '.impute.hap'), verbose=verbose) for chromosome in range(1,23)]
			commands += [gunzip_to_IMPUTE2(os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], defaults[tool_name + '_legendgz'].replace('@CHR@', str(chromosome))), os.path.join(defaults['reference_dir'], defaults[tool_name + '_dir'], 'Impute2', str(chromosome) + '.impute.hap'), verbose=verbose) for chromosome in range(1,23)]
		elif action[0:5] == 'mkdir':
			commands += [(mkdir, {'dir_name' : os.path.join(defaults[tool_name + '_dir'], action[5:]), 'verbose' : verbose})]
		else:
			raise Exception('Invalid action: %s' % action)

	system_many(commands, verbose=verbose, dummy=dummy)

def check_command_if_exists(tool_name, verbose = False):
	"""
	Check if a command exists
	"""

	if not which(tool_name):
		raise Exception('Could not find tool:' + tool_name)

	if verbose:
		print 'Command: ', tool_name, ' exists.'

def dl_tools(verbose=False, dummy=False):
	"""
	Downloads all necessary tools for the imputation pipeline
	"""

	global defaults

	#Make dir
	mkdir(defaults['tools_dir'])

	#Check if necessary tools exists
	check_command_if_exists('tar', verbose=verbose)
	check_command_if_exists('unzip', verbose=verbose)
	check_command_if_exists('g++', verbose=verbose)

	#Download necessary files
	install_tool('files', install_actions='dl_untar', verbose=verbose, dummy=dummy)

	#Download and install shapeit
	install_tool('shapeit', install_actions = 'cdtools_mkdir_dldir_untardir_cdcwd', verbose=verbose)

	#Download and install impute2
	install_tool('impute2', install_actions = 'cdtools_dl_untar_mv_cdcwd', verbose=verbose)

	#Download and install liftover
	install_tool('liftover', install_actions = 'cdtools_mkdir_dldir_makeexecdir_cdcwd', verbose=verbose)

	#Download and install plink
	install_tool('plink', install_actions = 'cdtools_dl_unzip_mv_cdcwd', verbose=verbose)

	#Download and install vcftools
	install_tool('vcftools', install_actions = 'cdtools_dl_untar_make_mv_cdcwd', verbose=verbose)

	#Checj if genotypeAligner is already installed
	install_tool('genotypeAligner', install_actions = 'cdtools_cdtooldir_checkfileexists_cdcwd', verbose=verbose)

	print 'All tools installed'


def dl_reference(reference_name, verbose=False):
	"""
	Downloads a reference set
	"""

	global defaults

	#Create dir
	mkdir(defaults['reference_dir'])

	#Check if this name is supported
	if reference_name not in [x[0] for x in defaults['reference_panels']]:
		raise Exception('Unknown reference panel name: ' + str(reference_name) + '. Use --list option to see availabe reference panels')	

	install_tool(reference_name, defaults[reference_name + '_actions'], verbose=verbose)

def random_id():
	"""
	Returns the first part of a random uuid. http://en.wikipedia.org/wiki/Universally_unique_identifier
	"""
	return str(uuid.uuid4()).split('-')[0]

def get_job_id():
	"""
	Return the current job id. A unique id for the current run. 
	"""
	global defaults

	if not defaults['current_job_id']:
                job_id = random_id()
                defaults['current_job_id']
        else:
                job_id = defaults['current_job_id']

	return job_id

def get_chr_pedmap_files(dir, extension='ped'):
	"""
	Returns all files in the form:
	<dir>/chr<CHROMOSOME>.ped
	<dir>/chr<CHROMOSOME>.map 
	"""

	file_list = glob.glob(os.path.join(dir, 'chr*.%s' % extension))
	if not file_list:
		return []
 
	chromosomes = []
	for file_name in file_list:
		found = re.search(r'([\d]+)\.%s$' % extension, file_name)
		if found:
			chromosome = found.group(1)
			if chromosome in [str(x) for x in range(1, 23)]:
				chromosomes += [chromosome]
 			else:
				print 'Warning: Ignoring file: %s in study dir' % file_name

	return chromosomes

def worksheet_writer(worksheet_data):
	"""
	Saves worksheet data in csv format
	"""
	return '\n'.join([','.join(x) for x in map(list, zip(*worksheet_data))]) + '\n'

def worksheet_filenamer(job_id):
	"""
	Creates a worksheet filename
	"""
	return 'worksheet_' + job_id + '.csv'

def worksheet_path_filenamer(pipeline_name, job_id):
	"""
	Returns the full path of a worksheet
	"""
	#return os.path.join(defaults['cwd'], defaults[pipeline_dir], worksheet_filename)
	worksheet_path = os.path.join(defaults['cwd'], generated_dir_namer(pipeline_name, job_id)) 
	#Make sure this directory exists
	mkdir(worksheet_path)
	worksheet_filename = worksheet_filenamer(job_id)
	return os.path.join(worksheet_path, worksheet_filename)

def worksheet_saver(worksheet_filename, worksheet_data, verbose = False):
	"""
	Saves a worksheet file
	"""
	if verbose:
		print 'Saving worksheet file :%s' % worksheet_filename
	worksheet_file = open(worksheet_filename, 'wb')
	worksheet_file.write(worksheet_writer(worksheet_data))
	worksheet_file.close()

def create_worksheet(job_id, pipeline_name, worksheet_data, verbose = False):
	"""
	Creates the worksheet file
	"""
	worksheet_filename_path = worksheet_path_filenamer(pipeline_name, job_id)
	worksheet_saver(worksheet_filename_path, worksheet_data, verbose)

def generated_dir_namer(pipeline_name, job_id):
	"""
	Creates a name for the directory of the generated scripts 
	"""
	return defaults['generated_' + pipeline_name + '_dir'] + '_' + job_id

def results_dir_namer(pipeline_name, job_id):
	"""
	Creates the name of the directory where the results will be stored
	"""
	return os.path.join(defaults['cwd'], defaults[pipeline_name + '_results_dir'] + '_' + job_id)

def molgenis_command_formatter(pipeline_name, job_id, backend):
	"""
	Format the command that generates the scripts
	"""
	command = [
		'sh',
		defaults['molgenis_compute_sh'],
		'--generate',
		'--path', defaults[pipeline_name + '_pipeline_dir'],
		'--workflow', 'workflow.csv',
		'--parameters', 'parameters.csv',
		worksheet_path_filenamer(pipeline_name, job_id),
		'--rundir', generated_dir_namer(pipeline_name, job_id),
		'--backend', backend,
		'--database', 'none',
	]
	
	return command

def submit_generated_script(pipeline_name, job_id, backend):
	"""
	submit generated scripts for execution
	"""

	generated_dir = generated_dir_namer(pipeline_name, job_id)

	print 'Generated %s scripts in: %s' % (backend, generated_dir)
	print 'Submitting..'
	chdir(generated_dir)
	system('sh submit.sh')
	chdir(defaults['cwd'])
	print 'Finished %s' % pipeline_name 

def worksheet_generate_submit(job_id, pipeline_name, worksheet_data, backend, verbose):
	"""
	Create worksheet, 
	Generate scripts
	Submit generated scripts
	"""
	create_worksheet(job_id, pipeline_name, worksheet_data, verbose)

	command = molgenis_command_formatter(pipeline_name, job_id, backend)
	system(' '.join(command), verbose=verbose, dummy=dummy)

	submit_generated_script(pipeline_name, job_id, backend)

	generated_dir = generated_dir_namer(pipeline_name, job_id)

def perform_phase(study, results, backend, verbose=False, dummy=False):
        """
        Generates and submits the phasing scripts
        """

	global defaults

	#Get job id
	job_id = get_job_id()

	if study == 'example':
		#Check if liftovered data exist
		example_ped_file = os.path.join(liftovered_results_dir, 'chr1', 'chr1.ped')
		example_map_file = os.path.join(liftovered_results_dir, 'chr1', 'chr1.map')
		if not os.path.exists(example_ped_file) or not os.path.exists(example_map_file):
			print 'Testing liftovered data do not exist. Generating ..'
			perform_liftover('example', backend, verbose=verbose, dummy=dummy)
	else:
		#Try to locate study data
		chromosomes = get_chr_pedmap_files(study)

	worksheet_data = [
		['project'] + [job_id for x in chromosomes],
		['m'] + [os.path.join(defaults['cwd'], defaults['genetic_map'].replace('@CHR@', chromosome)) for chromosome in chromosomes],
#		['outputFolder'] + [os.path.join(defaults['cwd'], defaults['phase_results_dir'] + '_' + job_id) for chromosome in chromosomes],
		['outputFolder'] + [results for chromosome in chromosomes],
		['chr'] + chromosomes,
		['studyData'] + [ ' '.join([os.path.join(study, 'chr' + chromosome + '.' + x) for x in ['ped', 'map']])  for chromosome in chromosomes],
		['studyDataType'] + ['PED' for chromosome in chromosomes],
	]

	worksheet_generate_submit(job_id, 'phase', worksheet_data, backend, verbose)

def perform_liftover(study, results, backend, verbose=False, dummy=False):
	"""
	Generates and submits the liftover scripts
	"""

	global defaults

	job_id = get_job_id()

	if study == 'example':
		study = defaults['study_example']
		if verbose:
			print 'Using example data: %s', study

	#Get the chromosome files available in this dir
	chromosomes = get_chr_pedmap_files(study)
	if not chromosomes:
		raise Exception('Could not find any file named chr<1-22>.ped in %s' % study)

	worksheet_data = [
		['study'] + [job_id for chomosome in chromosomes],
		['studyInputDir'] + [study for chromosome in chromosomes],
		['liftOverChainFile'] + [os.path.join(defaults['cwd'], defaults['hg18tohg19_chain']) for chromosome in chromosomes],
#		['outputFolder'] + [os.path.join(defaults['cwd'], defaults['liftover_results_dir'] + '_' + job_id) for chromosome in chromosomes],
		['outputFolder'] + [results for chromosome in chromosomes],
		['chr'] + chromosomes,
	]

	worksheet_generate_submit(job_id, 'liftover', worksheet_data, backend, verbose)

def chr_pos_generator(chromosomes, position_interval = 5000000):
	"""
	Generates th chr position intervals for the imputation job
	"""

	for chromosome in chromosomes:
		length = defaults['b37_chr_' + chromosome]
		for from_pos in range(1, length, position_interval):
			yield (chromosome, from_pos, from_pos + position_interval - 1)

def perform_impute(study, results, reference, backend, verbose=False, dummy=False):
	"""
	Generates and submits the imputation scripts
	"""

	global defaults

	job_id = get_job_id()

	reference_dir = os.path.join(defaults['cwd'], defaults['reference_dir'], defaults[reference + '_dir'])

	chromosomes = get_chr_pedmap_files(study, extension = 'haps')
	if not chromosomes:
		raise Exception('Could not find any files named chr<1-22>.haps in %s' % study)

	positions = [position for position in chr_pos_generator(chromosomes)]

	worksheet_data = [
		['project'] + [job_id for p in positions],
		['knownHapsG'] + [os.path.join(study, 'chr%s.haps' % p[0]) for p in positions],
		['m'] + [os.path.join(defaults['cwd'], defaults['genetic_map'].replace('@CHR@', p[0])) for p in positions],
		['h'] + [os.path.join(reference_dir, defaults[reference + '_hapsgz'].replace('@CHR@', p[0])) for p in positions],
		['l'] + [os.path.join(reference_dir, defaults[reference + '_legendgz'].replace('@CHR@', p[0])) for p in positions],
		['vcf'] + [os.path.join(reference_dir, defaults[reference + '_vcfgz'].replace('@CHR@', p[0])).replace('.vcf.gz', '') for p in positions],
		['additonalImpute2Param'] + ['-k_hap 1500 -Ne 20000' for p in positions],
		['outputFolder'] + [results for p in positions],
		['chr'] + [p[0] for p in positions],
		['fromChrPos'] + [str(p[1]) for p in positions],
		['toChrPos'] + [str(p[2]) for p in positions],
	]

	worksheet_generate_submit(job_id, 'impute', worksheet_data, backend, verbose)

def perform_action(action, reference, study, results, backend, verbose=False, dummy=False):
	"""
	Action dispatcher
	"""

	global defaults

	#Set environment variable
	os.environ['WORKDIR'] = defaults['cwd']

	if action == 'liftover':
		perform_liftover(study, results, backend, verbose=verbose, dummy=dummy)
	elif action == 'phase':
		perform_phase(study, results, backend, verbose=verbose, dummy=dummy)
	elif action == 'impute':
		perform_impute(study, results, reference, backend, verbose=verbose, dummy=dummy)
	else:
		raise Exception('Unknown action: %s' % str(action))

def show_reference_panels():
	"""
	Lists all available reference panels, or available from downloading reference panels
	"""
	global defaults

	print 'Downloaded reference panels:'

	for directory in glob.glob(os.path.join(defaults['reference_dir'], '*')):
		if os.path.isdir(directory):
			print os.path.split(directory)[1]

	print 'Reference panels availabe for download:'
	print ''
	for panel in defaults['reference_panels']:
		print 'name:', panel[0]
		print panel[1]
		print '-' * 20
	
	print 'To download any of these use the option: --dl_reference <name>'

def initialize(verbose):
	"""
	Run start up checks
	"""

	add_custom_reference_panels(verbose)
	

if __name__ == '__main__':

	description = """
		MOLGENIS-compute imputation version 0.7.0
	"""

	parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--dl_tools', help='download all necessary imputation tools', action='store_true')
#	parser.add_argument('--dl_1000gp', help='download the 1000 Genomes Project imputation reference set', choices=['1000GP_20101123_minimac', '1000GP_ALL_1000G_phase1integrated_v3_impute_macGT1', '1000GP_ALL_1000G_phase1integrated_v3_impute'])
	parser.add_argument('--dl_reference', help='download the 1000 Genomes Project imputation reference set', choices=[x[0] for x in defaults['reference_panels']])
	parser.add_argument('--action', help='Action to do: liftover, phase, impute', choices=['liftover', 'phase', 'impute'])
	parser.add_argument('--backend', help='Execution environment. Default: local', choices=['pbs',  'grid', 'local'], default='local')
	parser.add_argument('--study', help='Absolute path of the directory off the study panel')
	parser.add_argument('--output', help='Absolute path of the output directory')
	parser.add_argument('--reference', help='name of reference panel')
	parser.add_argument('--list', help='List of all available reference panels either already downloaded, or available for downloading', action='store_true')
#	parser.add_argument('--silent', help='Print additional output', action='store_true', default=True)
	parser.add_argument('--dummy', help='Show commands, don\'t do anything', action='store_true')
	args = parser.parse_args()

	verbose = True
#	if args.verbose == False:
#		verbose = False

	initialize(verbose)

	dummy = False
	if args.dummy:
		dummy=True

	if args.list:
		show_reference_panels()

	if args.dl_tools:
		dl_tools(verbose=verbose, dummy=dummy)

	if args.dl_reference:
		dl_reference(args.reference, verbose=verbose)

	if args.action:
		if not args.study:
			raise Exception('You need to define a directory where the study panel is, in order to perform this action (parameter --study)')

		if not args.output:
			raise Exception('You need to define a directory where the output results will be stored (parameter --output')

		perform_action(action=args.action, study=args.study, results=args.output, reference=args.reference, backend=args.backend, verbose=verbose, dummy=dummy)


