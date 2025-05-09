# Prepositions
Breakdown of scripts and how to use them by section of Beekhuizen et al. 2015 paper:

* Method
	- create_dev_test_split.py
		- usage: python create_dev_test_split.py
		- description: Splits exemplars in data/full_set.csv into a dev_set and test_set of equal sizes and writes them to data/dev_set.tsv and data/test_set.csv.
		
* Are all semantic functions equally important?
	- function_frequency.r
		- run in an R environment to get the data for Table 2. Run for dev_set and test_set.
		- frequency table: Spanish para vs por for each english translation.
	   	- frequency table: What amount of the 'por' uses were coded with each semantic function?
   		- frequency table: What amount of the 'para' uses were coded with each semantic function?
		- Shannon-entropy figures

* Are the functions at the right level of granularity?
	- analyze_clustering.py
		- usage: python analyze_clustering.py dataset.csv
		- dependencies: data.py
		- description: Prints a clustering summary for a given set of options (see description of options in the class docstring for the data class in data.py). Each summary consists of the Adjusted Rand Score with the assigned semantic functions gold labels followed by a confusion matrix between semantic functions and clusters found by the clustering algorithm.

I haven't done this one yet!
~~* The perspective of a similarity space
	- create_oc_files.py
		- usage: python create_oc_files.py data/test_set.tsv data/stemming_dictionary.csv
		- description: restructures data as input for oc.r, and writes them to files oc_SPLIT_labels.csv, oc_SPLIT_gold.csv, and oc_SPLIT.csv. For plotting the development data, replace 'data/test_set.tsv' with 'data/dev_set.tsv'. 
	- oc.r
		- usage: Rscript oc.r
		- description: Generates OC-MDS plots based on info in oc_SPLIT_test_labels.csv, oc_SPLIT_test_gold.csv and oc_test_SPLIT.csv. For plotting People instead of Things with the oc.r script, replace 'thing' on line 17 with 'body'.~~
	
