To perform the groupAggregate analysis, run the script groupAggregate. This script is not entirely self-contained, since the steps to acquiring the datasets in the initial stages are not in this script. They are in other scripts.

To get the Fisher's test data for all the individual ligand datasets except for ATP, run ligands bash script. For instance, to get 1%, 2.5%, 5%, and 10% for both the all and topsix metal ions for the ADP ligand, you should run ligands. You would also get the datasets for all the other ligands, e.g. GDP and FAD.

To get the Fisher's test data for the aggregate ligand datasets (includes ATP), run aggregate bash script.

The bash script groupAnalysis performs the grouping analysis. The Python script group.py is the first command executed for each ligand.

fisher.py performs the Fisher's test on the given metal or crystal contact dataset. The result is a p-value obtained using a 2x2 contingency table. Along one side of the table is outlier vs. non-outlier, and along the other side is close (i.e. within 3.5 angstroms) vs. non-close (i.e. beyond 3.5).

getBoth.py gets the both dataset for the given metal and crystal contact datasets. Note that the input is two datasets: metal dataset, and crystal dataset, each one having the same definition of outlier (e.g. both are 1%).

To get the Fisher results, just run fisher.py on each of the datasets. Note that you'll need to first run getBoth.py to get the both datasets, which you then pass in to fisher.py to get the Fisher results for those datasets.

To just do the Fisher's test on the given dataset that has the Fisher's table printed on the first line, run quickFisher.py on that dataset.

To execute the Fisher's test within the context of the group analysis, run groupFisher.py.
