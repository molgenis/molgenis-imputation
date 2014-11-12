
"""
molgenis-impute v.0.9.1
Alexandros Kanterakis, alexandros.kanterakis@gmail.com

Please read:
 * LICENSE 
 * documentation in README.md 

"""

__version__ = '0.9.1'

import os
import sys
import platform

# Check python version
if sys.version_info[0] == 2 and sys.version_info[1] >= 7:
	#Version is ok
	pass
else:
	raise Exception('Incompatible python version. (v. 2.7 needed)')

from imputation import Imputation
import argparse

#Check OS version
import platform
if platform.system() != 'Linux':
	raise Exception('Some of the tools needed for imputation are available only for Linux environment. Please run in a Linux computer.')

#Check if this is a x64 system
import struct
if 8 * struct.calcsize("P") != 64:
	raise Exception('Please run in a 64bit system. ')

#Check if outgoing ports for 80 (http) and 443 (https) are open
import socket
for port in [('http', 80), ('https', 443)]:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('www.github.com', port[1]))
	if result != 0:
		raise Exception('Port %i is not open. Therefore a %s connection cannot be established (tested on www.github.com)' % (port[1], port[0]))
	sock.close()

def check_for_absolute_path(argument, path):
	if not path:
		return 

	if not os.path.isabs(path):
		exception_text = '''
In argument: %s
The path: %s
Is not an absolute path
		''' % (argument, path)
		raise Exception(exception_text)


if __name__ == '__main__':

	description = """
		MOLGENIS-compute imputation version: %s
	""" % (__version__)

	parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--installation_dir', help='Installation directory for imputation tools and resources. Default: <currrent working dir>/molgenis_imputation')
	parser.add_argument('--reference_dir', help='Installation directory for the imputation reference panels. Default: <installation_dir>/resources/imputationReference')
	parser.add_argument('--list', help='List of all available reference panels either already downloaded, or available for downloading', action='store_true')
	parser.add_argument('--dl_tools', help='download all necessary imputation tools', action='store_true')
	parser.add_argument('--dl_reference', help='download and install an imputation reference panel')
	parser.add_argument('--study', help='Absolute path of the directory off the study panel')
	parser.add_argument('--output', help='Absolute path of the output (results) directory')
	parser.add_argument('--results', help='Same as --output')
	parser.add_argument('--chromosomes', help='comma separated values of chromosomes (If not set, imputation for all chromosomes will be performed')
	parser.add_argument('--additional_shapeit_parameters', help='Extra command line arguments to pass to SHAPEIT tool', default=' ')
	parser.add_argument('--additional_impute2_parameters', help='Extra command line arguments to pass to impute2 tool', default=' ')
	parser.add_argument('--position_batch_size', help='Size of the chromosomal size of each imputation batch', default=5000000, type=int)
	parser.add_argument('--sample_batch_size', help='Minimum number of samples in imputation batches', default=500, type=int)
	parser.add_argument('--reference', help='name of the imputation reference panel')
	parser.add_argument('--action', help='Action to do: liftover, phase, impute', choices=['liftover', 'phase', 'impute', 'phase_impute', 'liftover_phase_impute'])
	parser.add_argument('--add_reference', help='Add a new reference panel', action='store_true')
	parser.add_argument('--backend', help='Execution environment. Default: local', choices=['pbs',  'grid', 'local'], default='local')
	parser.add_argument('--chain_file', help='Genomic assembly for the liftover step', default='hg18ToHg19')
	parser.add_argument('--nosubmit', help='Create scripts but don\'t submit them for execution', action='store_true')
	parser.add_argument('--java_executable', help='java executable. Default: java .This is useful when java is not in the PATH', default='java')
	
	args = parser.parse_args()

	imp = Imputation(installation_dir=args.installation_dir, reference_dir=args.reference_dir)

	#Check for absolute paths:
	check_for_absolute_path('--study', args.study)
	check_for_absolute_path('--output', args.output)
	check_for_absolute_path('--installation_dir', args.installation_dir)
	check_for_absolute_path('--reference_dir', args.reference_dir)

	if args.results:
		if args.output:
			if args.results != args.output:
				raise Exception('--results and --output are the same parameters. They have different values')
		else:
			args.output = args.results

	if args.dl_tools:
		imp.install_imputation_tools()

	elif args.list:
		imp.list_reference_panels()

	elif args.dl_reference:
		imp.install_reference_panel(args.dl_reference)

	elif args.add_reference:
		imp.add_custom_reference_panels()

	elif args.action:
		if not args.study:
			raise Exception('You need to define a directory where the study panel is, in order to perform this action (parameter --study)')

		if not args.output:
			raise Exception('You need to define a directory where the output results will be stored (parameter --output')

		if args.action == 'liftover':
			imp.perform_liftover(args.study, args.output, assembly=args.chain_file, backend=args.backend, submit=not args.nosubmit)

		elif args.action == 'phase':
			imp.perform_phase(args.study, args.output, additional_shapeit_parameters=args.additional_shapeit_parameters, backend=args.backend, submit=not args.nosubmit)

		elif args.action == 'impute' or args.action == 'phase_impute' or args.action == 'liftover_phase_impute':
			if not args.reference:
				raise Exception('You need to define a reference panel. Use the --reference parameter. For a list for all available reference panels, use --list')

			imp.perform_impute(args.study, args.output, args.reference, 
					additional_impute2_parameters=args.additional_impute2_parameters, 
					additional_shapeit_parameters=args.additional_impute2_parameters,
					perform_liftover_argument=args.action == 'liftover_phase_impute',
					assembly=args.assembly,
					perform_phase_argument=args.action == 'phase_impute',
					custom_chromosomes=args.chromosomes,
					sample_batch_size=args.sample_batch_size,
					position_batch_size=args.position_batch_size,
					java_executable=args.java_executable,
					backend=args.backend,
					submit=not args.nosubmit)


	else:
		print description
		print 'For a full set of options run:'
		print 'python molgenis-impute.py --help'
		print 'For documentation check: https://github.com/molgenis/molgenis-imputation'


