# todo: clean up

from data import data
import sys
import numpy as np
import re
#
from sklearn.cluster import AffinityPropagation
from scipy.cluster import hierarchy
from sklearn.cluster import KMeans
#
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import confusion_matrix
#
from collections import defaultdict as dd

def get_k(clustering, depth = 10):
	"""
	(ndarray, int) -> int
	clustering: ndarray -- linkage matrix representing hierarchical clustering
	depth: int -- the maximum depth to traverse clustering
	
	Returns the number of clusters to extract from the hierarchical clustering
	using the elbow method.
	"""
	last = clustering[-depth: , 2]
	acceleration = np.diff(last, 2)
	acceleration_rev = acceleration[::-1]
	k = acceleration_rev.argmax() + 2
	return k

def get_cluster_assignments(sim_matrix, parameters):
	"""
	(np.array, list of int) -> list of int
	sim_matrix: list of list of float -- similarity matrix between exemplars
	parameters: list of parameters in the format ["method:method_name", 
			"algo:algo_name", "k:num_clusters", "damping:damping"]
			where order doesn't matter
			(k and damping only relevant for certain clustering methods)
			the possible values for each parameter are listed in the
			function below.
	
	Returns a list of integers. The integer at each index of the list corresponds
	to the cluster number of the exemplar at the same index in sim_matrix.
	"""

	algorithm = next((re.split(':',f)[1] for f in parameters if f[:4] == 'algo'), 'ap')
	# from { 'hierarchical', 'kmeans', 'ap', 'ward' }
	method = next((re.split(':',f)[1] for f in parameters if f[:6] == 'method'), 'single')
	# from {'single', 'complete', 'average'} (only relevant for hierarchical clustering)
	kMk = next((int(re.split(':',f)[1]) for f in parameters if f[:1] == 'k'), 8)
	# any integer <= the data length
	damping = next((re.split(':',f)[1] for f in parameters if f[:4] == 'damping'), 0.5)
	# only relevant for AP -- in [0.5,1]
	#
	if algorithm == 'hierarchical':
		clustering = hierarchy.linkage(sim_matrix, method)
		k = get_k(clustering, 20)
		cluster_assignments = hierarchy.fcluster(clustering, k, criterion = 'maxclust')-1
	elif algorithm == 'kmeans':
		cluster_assignments = KMeans(n_clusters = kMk).fit_predict(sim_matrix)
	elif algorithm == 'ap':
		cluster_assignments = AffinityPropagation().fit_predict(sim_matrix)
	elif algorithm == 'ward':
		clustering = hierarchy.ward(sim_matrix)
		k = get_k(clustering, 20)
		cluster_assignments = hierarchy.fcluster(clustering, k, criterion = 'maxclust')-1
	return cluster_assignments

def print_confusion_matrix(cluster_assignments, gold):
	"""
	(list of int, list of str) -> None
	cluster_assignments: list of int -- cluster numbers for each exemplar
	gold: list of str -- Haspelmath codes for each exemplar

	Prints out the confusion matrix between cluster_assignments and gold.
	"""
	m = dd(lambda : [0 for i in range(len(set(cluster_assignments)))])
	for c,g in zip(cluster_assignments,gold):
		m[g][c] += 1
	for k,v in m.items():
		print('%s\t%s' % (k[:7], ' '.join([('%d        ' % w)[:8] for w in v])))


def write_cluster_assignments(cluster_assignments, parameters):
        """
        (list of int, list of str) -> None
        cluster_assignments: list of int -- cluster numbers for each exemplar
        parameters: list of str -- list of parameters
        
        Writes the cluster assignments to a file named based on the contents
        of parameters.
        """
        with open('clustering_%s.csv' % '_'.join(sorted(parameters)),'w') as fh:
                fh.write('assignment\n%s' % '\n'.join([str(s) for s in cluster_assignments])) 

def sim(d1,d2):
	"""
	(list of str, list of str, list of str) -> float
	d1: list of str -- list of terms for each language used in a situation
	d2: list of str -- list of terms for each language used in a situation

	Returns the similarity score between d1 and d2.
	"""
	comparisons = [(e1==e2)
		for e1,e2 in zip(d1,d2) 
		if ((len(e1) > 0 and len(e2) > 0))]
	return (sum(comparisons)/len(comparisons)) if len(comparisons) > 0 else 0

def get_similarity_matrix(d, oix, association = 'None'):
        if association == 'None':
                legal_term_set = d.get_all_associations()
        else:
                legal_term_set = set([(li,t) for li,t,f in d.get_tf_associations(test = association)])
	#
        filtered_data = np.array([[[t for t in tt]
                for li,tt in enumerate(sit)] for sit in d.data])
        data_sub = filtered_data[oix]
        similarity_matrix = np.ones((data_sub.shape[0],data_sub.shape[0]))
        for i,di in enumerate(data_sub):
                for j,dj in enumerate(data_sub):
                        if j >= i: continue
                        similarity_matrix[i,j] = similarity_matrix[j,i] = sim(di, dj)
        return similarity_matrix

def single_exp(parameters):
	"""
	Runs a single clustering experiment based on a list of arguments.
	"""

	#data_path = sys.argv[1]    # path to data set
	#stem_dict_path = sys.argv[2]	# path to stemming dictionary
	#parameters = sys.argv[3:]	# list of parameters in format ["method:method_name", 
	parameters = parameters		#"algo:algo_name", "k:num_clusters", "damping:damping"]
					# see get_cluster_assignments for more details
	d = data(parameters)
	oix = sorted(set(d.oix_raw))
	print(len(oix))
	return
	#
	similarity_matrix = get_similarity_matrix(d, parameters, oix)
	cluster_assignments = get_cluster_assignments(similarity_matrix, parameters)
	print(adjusted_rand_score(d.annotation[oix], cluster_assignments))
	print_confusion_matrix(cluster_assignments, d.annotation[oix])

def comparative_exp():
        """
        Runs a series of clustering experiments for different parameter settings.
        """
        options = ['no_ambig','direct_trans', 'exclude_syntax', 'exclude_stock_phrases']
        d = data(options)
        oix = sorted(set(d.oix_raw))
        similarity_matrix = get_similarity_matrix(d, oix, association = 'associated')
        clustering_algos = [(a,m,k) for a in ['hierarchical', 'ward','kmeans']
			    for m in [None,'complete','average','single']
			    for k in [None,2,3,4,5,6,7,8,9,10]
			    if (m != None and k == None and a == 'hierarchical') or
			    (m == None and k != None and a == 'kmeans') or
			    (m == None and k == None and a in ['ward'])]
        for a,m,k in clustering_algos:
                parameters_j = options + ['algo:%s' % a]
                if m != None: parameters_j.append('method:%s' % m)
                if k != None: parameters_j.append('k:%r' % k)
                print(parameters_j)
                cluster_assignments = get_cluster_assignments(similarity_matrix, parameters_j)
                print(set(cluster_assignments))
                print(adjusted_rand_score(d.annotation[oix], cluster_assignments))
                print_confusion_matrix(cluster_assignments, d.annotation[oix])
	
if __name__ == "__main__":
	comparative_exp()
