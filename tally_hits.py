from utils import *

def count_property_range_hits(prop, min_val, max_val, node_dict, hits, overall_max):
	""" picks which values to use in tuples based on property
		counts vals having min_val <= val < max_val
	 	unless max_val == overall_max, where min_val <= val <= max_val 
	 	is used instead
	"""
	res = (0, 0, 0)
	# sets tuple position to use in dict value
	switcher = {
        "length": 0,
        "steps": 1,
        "cov": 2
    }
	if prop not in switcher:
		return res
	tup_pos = switcher[prop]
	node_cnt = 0
	pos_cnt = 0
	for node in node_dict.keys():
		val = node_dict[node][tup_pos]
		if max_val < overall_max:
			range_test_val = (min_val <= val < max_val)
		else:
			range_test_val = (min_val <= val <= max_val)
		# print "range bool is", range_test_val
		if range_test_val:
			node_cnt += 1
			if node in hits: pos_cnt += 1
	if node_cnt > 0:
		res = (pos_cnt, node_cnt, round(float(pos_cnt)/node_cnt,2))
	return res


# inputs: paths_w_cov.txt file, 
# RNODE_280_length_11187_cov_22.02284
# ('NODE_3309_length_5848_cov_19.2717', 'NODE_3684_length_331_cov_25.5688', "NODE_704_length_464_cov_21.1614'", 'NODE_3719_length_1431_cov_23.867', "NODE_2031_length_74_cov_35.1579'", "NODE_3754_length_3314_cov_24.4557'")
# [19.2717, 25.5688, 21.1614, 23.867, 2.5215272727272762, 24.4557]
# [3309, 3684, 704, 3719, 2031, 3754]
paths_file = '/home/nasheran/rozovr/recycle_paper_data/ref_400/before_rr.cycs.paths_w_cov.txt'

# create dict of RNODES as keys, values
# as tuples of (total_length, num_steps, coverage)
f = open(paths_file, 'r')
lines = f.readlines()
rnode_dict = {}
for ind in range(len(lines)/4):
	name = lines[ind*4].rstrip()
	path = lines[ind*4 + 1].rstrip()
	cov = get_cov_from_spades_name(name)
	length = get_length_from_spades_name(name)
	num_steps = len(path.split(','))
	# print name, num_steps, path
	rnode_dict[name] = (length, num_steps, cov)

# issue - single node path RNODEs are not in path_w_cov files
# read in cycs.fasta file, add back single node paths 
cycs_file = '/home/nasheran/rozovr/recycle_paper_data/ref_400/before_rr.cycs.fasta'
f = open(cycs_file)
lines = f.readlines()
for ind in range(len(lines)/2):
	name = lines[ind*2][1:].rstrip()
	if name in rnode_dict: continue
	else:
		cov = get_cov_from_spades_name(name)
		length = get_length_from_spades_name(name)
		# print name, 1
		rnode_dict[name] = (length, 1, cov)


# nucmer.delta file parsed to RNODES having 100/80 hits with 
#/home/gaga/rozovr/MUMmer3.23/show-coords -r -c -l /home/nasheran/rozovr/recycle_paper_data/ref_800/before_rr.nucmer.delta | awk '$10==100.00 && $15>=80.00' | cut -d'|' --complement -f 1-6 | cut -f2 > /home/nasheran/rozovr/recycle_paper_data/rnode_hits.txt
# need to read names in and get set
hits_file = '/home/nasheran/rozovr/recycle_paper_data/rnode_hits.txt'
f = open(hits_file)
hits = set([])
lines = f.readlines()
for line in lines:
	hits.add(line.rstrip())



print count_property_range_hits("length", 1000, 20000, rnode_dict, hits, 20000)
print count_property_range_hits("length", 0, 999, rnode_dict, hits, 20000)
# print count_property_range_hits("length", 5000, 9999, rnode_dict, 20000)




