import csv
import re
import numpy as np
from scipy.sparse import csr_matrix
from collections import Counter
import networkx as nx
from scipy.stats import fisher_exact
'''
Options: (original calls these parameters, but it's also calling something completely different parameters)
direct_trans: only use words that are directly translated
no_ambig: exclude words that are marked ambiguous
exclude_stock_phrases: remove annotations POR FAVOR, POR DIOS
exclude_syntax: remove annotations ADV, INF
'''

class data:
        def __init__(self, options):
                self.options = options
                self.read_data()

        def read_data(self):
                self.token_index = []
                self.annotation = []
                self.utterance = []
                #self.oix_raw = []
                self.all_legal = []
		
                with open('dataset.csv', encoding='utf-8') as f:
                        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
                        data_raw = list(reader)[1:]
                self.data = []
                for di,d in enumerate(data_raw):
                        if d[7] != 'x': continue;
                        if d[4] == 'ERROR': continue
                        if d[3] == '?' and d[4] == '?': continue
                        annotation = d[4].strip()
                        #oix = di
                        try: utt = int(d[0])
                        except ValueError:
                                print("integer ValueError",d)
                        sentence = d[5].strip()
                        preposition = d[1].strip()
                        english_trans = d[3].strip()
                        try:
                                if d[3] == '?': english_trans = 'ERR'
                                elif annotation[-1] == '?': annotation = 'AMBIG'
                        except IndexError:
                                print("d=",d,"annotation=",annotation)
                        try: inx = sentence.lower().split(' ').index(preposition)
                        except ValueError:
                                print("sentence.lower().split(' ').index(preposition) failed: ",preposition, sentence)
                                continue
                        #yes I could combine these nested if statements into one-layer statements--I'm too sleepy to debug
                                #when I inevitably write it wrong
                        if 'no_ambig' in self.options and annotation == 'AMBIG': continue
                        if 'direct_trans' in self.options:
                                if english_trans == 'ERR' or english_trans == 'DISTRANS': continue
                        if 'exclude_stock_phrases' in self.options:
                                if annotation == 'POR FAVOR' or annotation == 'POR DIOS': continue
                        if 'exclude_syntax' in self.options:
                                if annotation == 'ADV' or annotation == 'INF': continue;
                        self.token_index.append((utt,inx))
			#self.ontological.append(onto)
                        self.annotation.append(annotation)
                        self.utterance.append(d[5])
                        #self.oix_raw.append(oix)
                        self.data.append([])
                        self.data[-1].append([d[1].strip()])
                        self.data[-1].append([english_trans.strip()])
                        self.all_legal.append((0,preposition,annotation))
                        if english_trans != '?':
                                self.all_legal.append((1,english_trans))
		# convert attributes to np arrays
		#self.ontological = np.array(self.ontological)
                self.annotation = np.array(self.annotation)
                self.oix_raw = list(range(len(self.annotation)))
                self.data = np.array(self.data)
                self.token_index = np.array(self.token_index)
                return

        def get_tf_associations(self, test):
		# test = {not dissociated,associated}
                tf_set = set()
		# this is the set in which all Term - Function pairs will be contained
		# that cannot be dissociated (i.e, for which we do not know for sure that
		# they are not associated) - done with Fisher Exact tests
                d = self.data
                for li in range(2):
                        terms = set([w for dd in d for w in dd[li]])
                        for term in terms:
                                for annot in set(self.annotation):
                                        valid = False
                                        if annot == 'AMBIG': continue;
                                        d_annot = self.data[(self.annotation == annot)]
                                        aa = len([t for t in d_annot if term in t[li]]) # + term + function
                                        ab = len(d_annot) - aa # - term + function
                                        ba = len([t for t in d if term in t[li]]) - aa # + term - function
                                        bb = len(d) - (aa + ab + ba) # - term - function
                                        if test == 'not dissociated' and fisher_exact([[aa,ab],[ba,bb]],'less')[1] > .05:
                                                valid = True
                                                tf_set.add((li,term,annot))
                                        if test == 'associated' and fisher_exact([[aa,ab],[ba,bb]],'greater')[1] < .05:
                                                valid = True
                                                tf_set.add((li,term,annot))
						# if aa > 0: print('%s,%d,%s,%s,%r,%d,%d,%d' % (onto,li,term,annot,valid,aa,ba,ab))

                return tf_set

        def get_all_associations(self):
                return set(self.all_legal)

if __name__ == "__main__":
	import sys
	d = data(["direct_trans"])
	#d.get_tf_associations


