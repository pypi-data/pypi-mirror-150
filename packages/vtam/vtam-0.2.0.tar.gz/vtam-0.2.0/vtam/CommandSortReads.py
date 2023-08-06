import multiprocessing
import os
import sys

import pandas
import pathlib
import shlex
import subprocess
import gzip 
import bz2
from functools import partial
import shlex

# Compatible with both pre- and post Biopython 1.78:
try:
    from Bio.Alphabet import generic_dna
except ImportError:
    generic_dna = None

from Bio.Seq import Seq
from vtam.utils.Logger import Logger
from vtam.utils.FileParams import FileParams
from vtam.utils.PathManager import PathManager
from vtam.utils.FileSampleInformation import FileSampleInformation
from vtam.utils.FilesInputCutadapt import FilesInputCutadapt

class CommandSortReads(object):
    """Class for the Merge command"""

    @staticmethod
    def main(fastainfo, fastadir, sorteddir, params=None, num_threads=multiprocessing.cpu_count(), 
        no_reverse=False, tag_to_end=False, primer_to_end=False):
        
        Logger.instance().info(f"OPTIONS:\n no_reverse: {not no_reverse} \n tag_to_end {not tag_to_end} \n primer_to_end {not primer_to_end}")

        if sys.platform.startswith('win'):
            num_threads = 1

        ############################################################################################
        #
        # params.yml parameters
        #
        ############################################################################################

        params_dic = FileParams(params).get_params_dic()

        cutadapt_error_rate = params_dic['cutadapt_error_rate']
        cutadapt_minimum_length = params_dic['cutadapt_minimum_length']
        cutadapt_maximum_length = params_dic['cutadapt_maximum_length']

        ############################################################################################
        #
        # Loop over tag and primer pairs to demultiplex and trim reads
        #
        ############################################################################################

        merged_fastainfo_df = FileSampleInformation(fastainfo).read_tsv_into_df()
        
        pathlib.Path(sorteddir).mkdir(parents=True, exist_ok=True)
        tempdir = PathManager.instance().get_tempdir()

        merged_fasta_list = []
        results_list = []
        sample_info = {}

        # make sure every file is analysed once.
        for i in range(merged_fastainfo_df.shape[0]):
            if merged_fastainfo_df.iloc[i].mergedfasta not in merged_fasta_list:
                merged_fasta_list.append(merged_fastainfo_df.iloc[i].mergedfasta)
            
        for mergedfasta in merged_fasta_list:

            inputFiles = FilesInputCutadapt(fastainfo, mergedfasta, no_reverse, tag_to_end)
            
            tagFile_path = inputFiles.tags_file()
            info = inputFiles.get_df_info()

            for key in info.keys():
                if key in sample_info.keys():
                    sample_info[key] = sample_info[key] + info[key]
                else:
                    sample_info[key] = info[key]

            Logger.instance().debug("Analysing FASTA file: {}".format(mergedfasta))

            in_raw_fasta_path = os.path.join(fastadir, mergedfasta)

            ########################################################################################
            #
            #   cutadapt --cores=0 -e 0 --no-indels --trimmed-only -g tagFile:$tagfile 
            #   --overlap length -o "tagtrimmed.{name}.fasta" in_raw_fasta_path
            #
            ########################################################################################

            base = os.path.basename(in_raw_fasta_path)
            base, base_suffix = base.split('.', 1)
            
            out_fasta_path = os.path.join(tempdir, "sorted") 

            cmd_cutadapt_tag_dic = {
                'in_fasta_path': in_raw_fasta_path,
                'out_fasta': out_fasta_path,
                'num_threads': num_threads,
                'tagFile': tagFile_path,
                'base_suffix': base_suffix,
            }

            cmd_cutadapt_tag_str = 'cutadapt --cores={num_threads} --no-indels --error-rate 0 --trimmed-only ' \
                '-g file:{tagFile} --output {out_fasta}_{{name}}.{base_suffix} {in_fasta_path}' \
                .format(**cmd_cutadapt_tag_dic)

            Logger.instance().debug("Running: {}".format(cmd_cutadapt_tag_str))

            if sys.platform.startswith("win"):
                args = cmd_cutadapt_tag_str
            else:
                args = shlex.split(cmd_cutadapt_tag_str)
            run_result = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            Logger.instance().info(run_result.stdout.decode())

            inputFiles.remove_tags_file()

            ########################################################################################
            #
            # Trim primers from output
            # cutadapt --quiet --cores=0 -e trim_error --no-indels --trimmed-only 
            # --minimum-length minimum_length --maximum-length maximum_length 
            # --output input_path + {name} + suffix outputfile
            #
            ########################################################################################
            
            primers = inputFiles.primers()
            try:
                tags_samples = inputFiles.get_sample_names()
            except Exception as e:
                Logger.instance().error(e)
                return 
            
            for primer in primers:
                
                marker, primerfwd, primerrev, lenprimerfwd, lenprimerrev = primer

                for tag_sample in tags_samples:

                    name, run, marker2, sample, replicate, _, _ = tag_sample
                    
                    if marker not in marker2:
                        continue

                    in_fasta_path = out_fasta_path + "_" + name + "." + base_suffix

                    baseMerge =  mergedfasta.split(".")[0]
                                        
                    outname = run + "_" + marker + "_" + sample + "_" + replicate + "_" + baseMerge + "_trimmed"
                    if name.endswith("_reversed"):
                        outname = outname + "_reversed"
                    out_fasta_path_new = os.path.join(tempdir, outname + "." + base_suffix)

                    results_list.append(out_fasta_path_new)
                    
                    if not "_reversed" in name:
                        if generic_dna:  # Biopython <1.78
                            primerRev = str(Seq(primerrev, generic_dna).reverse_complement())
                        else:  # Biopython =>1.78
                            primerRev = str(Seq(primerrev).reverse_complement())
                        primerFwd = primerfwd
                        lenPrimerFwd = lenprimerfwd
                        lenPrimerRev = lenprimerrev
                    else:
                        if generic_dna:  # Biopython <1.78
                            primerRev = str(Seq(primerfwd, generic_dna).reverse_complement())
                        else:  # Biopython =>1.78
                            primerRev = str(Seq(primerfwd).reverse_complement())
                        primerFwd = primerrev
                        lenPrimerFwd = lenprimerrev
                        lenPrimerRev = lenprimerfwd


                    cmd_cutadapt_primer_dic = {
                        'in_fasta_path': in_fasta_path,
                        'out_fasta': out_fasta_path_new,
                        'error_rate': cutadapt_error_rate,
                        'num_threads': num_threads,
                        'primerFwd': primerFwd,
                        'primerRev': primerRev,
                        'lenPrimerFwd': lenPrimerFwd,
                        'lenPrimerRev': lenPrimerRev,
                        'read_min_length': cutadapt_minimum_length,
                        'read_max_length': cutadapt_maximum_length,
                    }

                    if not primer_to_end: #works if the command is selected
                        cmd_cutadapt_primer_str = 'cutadapt --cores={num_threads} --no-indels --error-rate {error_rate} ' \
                            '--minimum-length {read_min_length} --maximum-length {read_max_length} ' \
                            '--trimmed-only -g "^{primerFwd}...{primerRev}$" --output {out_fasta} {in_fasta_path}'\
                            .format(**cmd_cutadapt_primer_dic)
                    else:
                        cmd_cutadapt_primer_str = 'cutadapt --cores={num_threads} --no-indels --error-rate {error_rate} ' \
                            '--minimum-length {read_min_length} --maximum-length {read_max_length} ' \
                            '--trimmed-only -g "{primerFwd};min_overlap={lenPrimerFwd}...{primerRev};min_overlap={lenPrimerRev}" '\
                            '--output {out_fasta} {in_fasta_path}'\
                            .format(**cmd_cutadapt_primer_dic)

                    Logger.instance().debug("Running: {}".format(cmd_cutadapt_primer_str))

                    if sys.platform.startswith("win"):
                        args = cmd_cutadapt_primer_str
                    else:
                        args = shlex.split(cmd_cutadapt_primer_str)

                    run_result = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    Logger.instance().info(run_result.stdout.decode())

        ###################################################################
        #
        # Reverse complement back rc fasta and pool
        #
        ###################################################################   
     
        for file in results_list:
            if "_trimmed" in file:

                out_final_fasta_path = os.path.join(sorteddir, os.path.split(file)[-1])
                in_fasta_path = os.path.join(tempdir, file)

                if out_final_fasta_path.endswith(".gz"):      
                    _open = partial(gzip.open) 
                elif out_final_fasta_path.endswith(".bz2"):
                    _open = partial(bz2.open)
                else:
                    _open = open

                if in_fasta_path.endswith(".gz"):
                    _open2 = partial(gzip.open) 
                elif in_fasta_path.endswith(".bz2"):
                    _open2 = partial(bz2.open) 
                else: 
                    _open2 = open

                if "_reversed" in file:
                    Logger.instance().debug("Pooling fwd and rc reads...")

                    out_final_fasta_path = out_final_fasta_path.replace("_reversed", "")

                    with _open(out_final_fasta_path, 'at') as fout:
                        with _open2(in_fasta_path, 'rt') as fin:
                            for line in fin.readlines():
                                if not line.startswith('>'):
                                    if generic_dna:  # Biopython <1.78
                                        fout.write("%s\n" % str(
                                            Seq(line.strip(), generic_dna).reverse_complement()))
                                    else:  # Biopython =>1.78
                                        fout.write("%s\n" % str(
                                            Seq(line.strip()).reverse_complement()))

                                else:
                                    fout.write(line)
                else:
                    with _open(out_final_fasta_path, 'at') as fout:
                        with _open2(in_fasta_path, 'rt') as fin:
                            for line in fin.readlines():
                                fout.write(line)
        
        results_list = [os.path.split(result)[-1] for result in results_list if "_reversed" not in result]

        del sample_info['mergedfasta']
        del sample_info['primerrev']
        del sample_info['primerfwd']
        del sample_info['tagrev']
        del sample_info['tagfwd']

        sample_info['sortedfasta'] = results_list

        sample_info_df = pandas.DataFrame(sample_info)

        fasta_trimmed_info_tsv = os.path.join(sorteddir, 'sortedinfo.tsv')
        sample_info_df.to_csv(fasta_trimmed_info_tsv, sep="\t", header=True, index=False)
