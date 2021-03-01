# Instagram_Poetry_Processing

This project was written in Python3.

The purpose of the project was to compile a dataset of Instapoems, and use those poems to (1) write an algorithm that could generate representative Instapoetry based on the dataset and (2) extract useful statistical insights from the data.

ocr_new.py takes all images in a folder named "sample" and compiles an output file named "results.csv" of all of the poems that appear to be written in English.

cleanResults.py takes the "results.csv" file and performs various processing operations on it; it eliminates poems that are seemingly low-quality due to their (1) excessively short length, (2) excessive ratio of misspelled words, or (3) excessive number of non-English words.  It compiles an output file named "clean.csv."

genText.py takes the "clean.csv" file and uses Markov chains to generate 20 poems based on the sample.

statsModel.py takes the "clean.csv" file and uses latent Dirichlet allocation to compile several topic models from the poems.

requirements.txt lists all of the Python modules required to run the project - and, just as importantly, the versions of the modules.  If you attempt to run one of the scripts and it appears not to work for reasons that are not immediately clear, use a dependency manager to ensure that your version of the dependencies match the versions in requirements.txt.
