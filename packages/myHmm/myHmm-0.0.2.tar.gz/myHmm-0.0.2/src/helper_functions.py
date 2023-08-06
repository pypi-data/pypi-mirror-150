import numpy as np
import json
from collections import defaultdict
import os
import itertools
import difflib


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Make test data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def Maketestdata(data_set_length):
    '''Create test data set of size data_set_length'''
    np.random.seed(42)

    window_size = 1000
    mutation_rate_window = 1000000

    # Initialization parameters (prob of staring in states)
    state_values = [0,1]
    state_names, transitions, emissions, starting_probabilities = get_default_HMM_parameters()

    mutation_matrix = {
        'A': [0, 0.16, 0.68, 0.16],
        'C': [0.16, 0,0.16, 0.68],
        'G': [0.68, 0.16, 0, 0.16],
        'T': [0.16, 0.68, 0.16, 0],
    }

    bases = ['A','C','G','T']

    # Make obs file
    with open('obs.txt','w') as obs:

        print('chrom', 'pos', 'ancestral_base', 'genotype', sep = '\t', file = obs)

        for chrom in ['chr1', 'chr2']:
            for index in range(data_set_length):
                if index == 0:
                    current_state = np.random.choice(state_values, p=starting_probabilities)
                else:
                    current_state = np.random.choice(state_values, p=transitions[prevstate] )

                n_mutations = np.random.poisson(lam=emissions[current_state]) 
                for mutation in [int(x) for x in np.random.uniform(low=index*window_size, high=index*window_size + window_size, size=n_mutations)]: 
                    ancestral_base = np.random.choice(bases, p=[0.31, 0.19, 0.19, 0.31])
                    derived_base = np.random.choice(bases, p=mutation_matrix[ancestral_base])
                    print(chrom, mutation, ancestral_base, ancestral_base + derived_base, sep = '\t', file = obs)          

                prevstate = current_state


    # Make mutation file
    with open('mutrates.bed','w') as mutrates:
        for chrom in ['chr1', 'chr2']:
            for start in range(int(data_set_length * window_size / mutation_rate_window)):
                print(chrom, start * mutation_rate_window, (start + 1) * mutation_rate_window, 1, sep = '\t', file = mutrates)



    # Make weights file
    with open('weights.bed','w') as weights:
        for chrom in ['chr1', 'chr2']:
            print(chrom, 1, data_set_length * window_size, sep = '\t', file = weights)



    # Make initial guesses
    state_names = np.array(['Human', 'Archaic'])
    starting_probabilities = np.array([0.5, 0.5])
    transitions = np.array([[0.99,0.01],[0.02,0.98]])
    emissions = np.array([0.03, 0.3])

    Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions, 'Initialguesses.json')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions for handling HMM parameters
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_default_HMM_parameters():
    state_names = np.array(['Human', 'Archaic'])
    starting_probabilities = np.array([0.98, 0.02])
    transitions = np.array([[0.9999,0.0001],[0.02,0.98]])
    emissions = np.array([0.04, 0.4])

    return state_names, transitions, emissions, starting_probabilities



def Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions, outfile):
    '''Saves parameters to a file'''
    json_string = json.dumps({
                'state_names' : state_names.tolist(),
                'starting_probabilities' : starting_probabilities.tolist(),
                'transitions' : transitions.tolist(),
                'emissions' : emissions.tolist(),
             }, indent = 2)

    Make_folder_if_not_exists(outfile)
    with open(outfile, 'w') as out:
        out.write(json_string)


def Load_HMM_parameters(markov_param):
    '''Loads parameters to a file'''
    if markov_param is None:
        state_names, transitions, emissions, starting_probabilities = get_default_HMM_parameters()
    else:
        with open(markov_param) as json_file:
            data = json.load(json_file)

        state_names, starting_probabilities, transitions, emissions = data['state_names'], data['starting_probabilities'], data['transitions'], data['emissions']


    # convert into numpy arrays
    transitions, starting_probabilities, emissions, state_names = np.array(transitions), np.array(starting_probabilities), np.array(emissions), np.array(state_names)

    return state_names, transitions, emissions, starting_probabilities


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions for handling observertions/bed files
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_callability_from_bed(bedfile, obs_counter, window_size):
    callability = defaultdict(lambda: defaultdict(float))
    with open(bedfile) as data:
        for line in data:

            if not line.startswith('chrom'):

                if len(line.strip().split('\t')) == 3:
                    chrom, start, end = line.strip().split('\t')
                    value = 1
                elif  len(line.strip().split('\t')) > 3:
                    chrom, start, end, value = line.strip().split('\t')[0:4]
                    value = float(value)

                start = int(start)
                end = int(end)


                firstwindow = start - start % window_size
                firstwindow_fill = window_size - start % window_size

                lastwindow = end - end % window_size
                lastwindow_fill = end %window_size

                # not spanning windows
                if firstwindow == lastwindow:
                    callability[chrom][firstwindow] += (end-start+1) * value

                else:

                    callability[chrom][firstwindow] += firstwindow_fill * value
                    callability[chrom][lastwindow] += (lastwindow_fill+1) * value

                    for window_tofil in range(firstwindow + window_size, lastwindow, window_size):
                        callability[chrom][window_tofil] += window_size * value

    final_list = []

    if obs_counter is not None:
        for chrom in sorted(obs_counter, key=sortby):
            lastwindow = max(obs_counter[chrom]) + window_size

            for window in range(0, lastwindow, window_size):
                final_list.append(callability[chrom][window] / float(window_size))

    else:
        for chrom in sorted(callability, key=sortby):
            lastwindow = max(callability[chrom]) + window_size

            for window in range(0, lastwindow, window_size):
                final_list.append(callability[chrom][window] / float(window_size))


    return np.array(final_list)

def Load_observations_weights_mutrates(obs_file, mutrates_file, weights_file, window_size):

    obs_counter = defaultdict(lambda: defaultdict(int))
    with open(obs_file) as data:
        for line in data:
            if not line.startswith('chrom'):
                chrom, pos = line.strip().split()[0:2]
                rounded_pos = int(pos) - int(pos) % window_size
                obs_counter[chrom][rounded_pos] += 1

    temp_obs = []
    chromosome_order = sorted(obs_counter, key=sortby)
    for chrom in chromosome_order:
        lastwindow = max(obs_counter[chrom]) + window_size

        for window in range(0, lastwindow, window_size):
            temp_obs.append(obs_counter[chrom][window])


    if weights_file is None:
        weights = np.ones(len(temp_obs)) 
    else:  
        weights = make_callability_from_bed(weights_file, obs_counter, window_size)

    if mutrates_file is None:
        mutrates = np.ones(len(temp_obs)) 
    else:  
        mutrates = make_callability_from_bed(mutrates_file, obs_counter, window_size)

    # Make sure there are no places with obs > 0 and 0 in mutation rate or weight
    obs = np.zeros(len(temp_obs))
    for index, (observation, w, m) in enumerate(zip(temp_obs, weights, mutrates)):
        if w*m == 0 and observation != 0:
            obs[index] = 0
            print('warning, you had observations but no called bases/no mutation rate')
            print(index, observation, w, m)
        else:
            obs[index] = int(observation)

    return obs.astype(int), mutrates, weights



def Get_genome_coordinates(obs_file, window_size):
    

    obs_counter = defaultdict(lambda: defaultdict(list))
    with open(obs_file) as data:
        for line in data:
            if not line.startswith('chrom'):
                chrom, pos = line.strip().split()[0:2]
                rounded_pos = int(pos) - int(pos) % window_size
                obs_counter[chrom][rounded_pos].append(pos)

    chroms, starts, variants = [], [], []
    chromosome_order = sorted(obs_counter, key=sortby)
    for chrom in chromosome_order:
        lastwindow = max(obs_counter[chrom]) + window_size

        for window in range(0, lastwindow, window_size):
            chroms.append(chrom)   
            starts.append(window)
            variants.append(','.join(obs_counter[chrom][window]))


    return chroms, starts, variants


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# For decoding/training
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def find_runs(inarray):
        """ run length encoding. Partial credit to R rle function. 
            Multi datatype arrays catered for including non Numpy
            returns: tuple (runlengths, startpositions, values) """
        ia = np.asarray(inarray)                # force numpy
        n = len(ia)
        if n == 0: 
            return (None, None, None)
        else:
            y = ia[1:] != ia[:-1]               # pairwise unequal (string safe)
            i = np.append(np.where(y), n - 1)   # must include last element posi
            z = np.diff(np.append(-1, i))       # run lengths
            p = np.cumsum(np.append(0, z))[:-1] # positions
            #return (ia[i], p, z)

            for (a, b, c) in zip(ia[i], p, z):
                yield (a, b, c)


def logoutput(emissions, loglikelihood, transitions, starting_probabilities, iteration):

    if iteration == 0:    
        print_emissions = '\t'.join(['emis{0}'.format(x + 1) for x in range(len(emissions))])
        print_starting_probabilities = '\t'.join(['start{0}'.format(x + 1) for x in range(len(emissions))])
        print_transitions = '\t'.join(['trans{0}_{0}'.format(x + 1) for x in range(len(emissions))])
        print('iteration', 'loglikelihood', print_starting_probabilities, print_emissions, print_transitions, sep = '\t')

    
    print_emissions = '\t'.join([str(x) for x in np.matrix.round(emissions, 4)])
    print_starting_probabilities = '\t'.join([str(x) for x in np.matrix.round(starting_probabilities, 3)])
    print_transitions = '\t'.join([str(x) for x in np.matrix.round(transitions, 4).diagonal()])
    print(iteration, round(loglikelihood, 4), print_starting_probabilities, print_emissions, print_transitions, sep = '\t')


def get_ancestral_from_fasta(ancestral):
    # Get ancestral information
    ancestral_allele = ''
    with open(ancestral) as data:
        for line in data:
            if line.startswith('>'):
                pass
                #seqname = line.strip().replace('>','')
            else:
                ancestral_allele += line.strip().upper()

    return ancestral_allele


def get_ingroup_outgroup(outgroup_ingroupfile):
    # Load outgroup and ingroup individuals
    with open(outgroup_ingroupfile) as json_file:
        data = json.load(json_file)
    outgroup_individuals = data['outgroup']
    ingroup_individuals = data['ingroup']

    return ingroup_individuals, outgroup_individuals






def make_mutation_rate(freqfile, outfile, callablefile, window_size):

    print('-' * 40)
    print('Selected parameters')
    print(f'> Outgroupfile is:\n{freqfile}\n')
    print(f'> Outputfile is:\n{outfile}\n')
    print(f'> Callability file is:\n{callablefile}\n')
    print(f'> Window size is:\n{window_size}\n')
    print('-' * 40)

    snps_counts_window = defaultdict(lambda: defaultdict(int))

    with open(freqfile) as data:
        for line in data:
            if not line.startswith('chrom'):
                chrom, pos, ref_allele_info, alt_allele_info, ancestral_base = line.strip().split()
                _, ref_count = ref_allele_info.split(':')
                _, alt_count = alt_allele_info.split(':')
                pos, ref_count, alt_count = int(pos),  int(ref_count), int(alt_count)
                window = pos - pos%window_size
                snps_counts_window[chrom][window] += 1


    mutations = []
    genome_positions = []
    for chrom in sorted(snps_counts_window, key=sortby):
        lastwindow = max(snps_counts_window[chrom]) + window_size

        for window in range(0, lastwindow, window_size):
            mutations.append(snps_counts_window[chrom][window])
            genome_positions.append([chrom, window, window + window_size])

    mutations = np.array(mutations)

    if callablefile is not None:
        callable_region = make_callability_from_bed(callablefile, snps_counts_window, window_size)
    else:
        callable_region = np.ones(len(mutations)) * window_size

    genome_mean = np.sum(mutations) / np.sum(callable_region)

    Make_folder_if_not_exists(outfile)
    with open(outfile,'w') as out:
        print('chrom', 'start', 'end', 'mutationrate', sep = '\t', file = out)
        for genome_pos, mut, call in zip(genome_positions, mutations, callable_region):
            chrom, start, end = genome_pos
            if mut * call == 0:
                ratio = 0
            else:
                ratio = round(mut/call/genome_mean, 2)

            print(chrom, start, end, ratio, sep = '\t', file = out)
        

def get_consensus(infiles):
    infiles = [str(x) for x in infiles]

    consensus_strings = defaultdict(int)
    for a, b in itertools.combinations(infiles,2):
        consensus_a = 'START'
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0] != ' ':
                consensus_a += ' '
            else:
                consensus_a += s[-1]
        consensus_a += 'END'


        new_joined = '|'.join(consensus_a.split()).replace('START','').replace('END','')
        consensus_strings[new_joined] += 1

    for value in consensus_strings:

        if len(value.split('|')) == 2:
            prefix, postfix = value.split('|')
            matches = len([x for x in infiles if prefix in x and postfix in x])

            if matches == len(infiles):
                values = [x.replace(prefix, '').replace(postfix,'') for x in infiles]
                return prefix, postfix, set(values)

def sortby(x):
    lower_case_letters = 'abcdefghijklmnopqrstuvwxyz'
    if x.isnumeric():
        return int(x)
    elif type(x) == str and len(x) > 0:
        return 1e6 + lower_case_letters.index(x[0].lower())
    else:
        return 2e6


def Make_folder_if_not_exists(path):
    # Check if path exists - otherwise make it
    path = os.path.dirname(path)
    if path != '':
        if not os.path.exists(path):
            os.makedirs(path)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Download 1000 genomes data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def download_1KG_data_bcf(chrom): 
    print(f'Dowloading bcf for 1000g chromosome {chrom}')
    os.system(f'wget ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/bcf_files/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5.20130502.genotypes.bcf')
    os.rename(f'ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5.20130502.genotypes.bcf', f'chr{chrom}.bcf')

    os.system(f'wget ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/bcf_files/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5.20130502.genotypes.bcf.csi')
    os.rename(f'ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5.20130502.genotypes.bcf.csi', f'chr{chrom}.bcf.csi')

def download_callability():
    print('Download strick callability mask')
    os.system('wget ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/accessible_genome_masks/20141020.strict_mask.whole_genome.bed')
    os.system("""sed 's/^chr\|%$//g' 20141020.strict_mask.whole_genome.bed | awk '{{print $1"\t"$2"\t"$3}}' > strickmask.bed""")
    os.remove('20141020.strict_mask.whole_genome.bed')

def download_ancestral_information():
    print('dowloading ancestral information')
    os.system('wget ftp://ftp.ensembl.org/pub/release-74/fasta/ancestral_alleles/homo_sapiens_ancestor_GRCh37_e71.tar.bz2')
    os.system('tar -xf homo_sapiens_ancestor_GRCh37_e71.tar.bz2')
    os.remove('homo_sapiens_ancestor_GRCh37_e71.tar.bz2')

 
def download_outgroup():
    print('Download outgroup/ingroup information')
    os.system('wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel')
    outgroup_ind = []
    ingroup = ['HG00096', 'HG00097']
    with open('integrated_call_samples_v3.20130502.ALL.panel') as data, open('individuals.json','w') as out:
        for line in data:
            if not line.startswith('sample'):
                sample, pop, super_pop, gender = line.strip().split()
                if pop in ['YRI','MSL','ESN']:
                    outgroup_ind.append(sample)

        '''Saves parameters to a file'''
        json_string = json.dumps({
                    "ingroup" : ingroup,
                    "outgroup" :outgroup_ind
                }, indent = 2)

        out.write(json_string)
    os.remove('integrated_call_samples_v3.20130502.ALL.panel')