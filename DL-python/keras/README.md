keras
=====

The materials hosted [in this nice tutorial repository][0] are used for
reference in this section.

Setup
-----

Tested on node `cg20-10` (8 Tesla V100s)

Run the following `conda` command to install the `tfv100` enviroment
built for this exercise

    interactive -t 60 -p gpu -q wildfire --gres=gpu:V100:1
    module load anaconda/py3
    conda env create -f environment.yml
    source activate tfv100

Run a test on the following file:

    python 1-basic-cnn.py


<img src="../../assets/ASURC_logo.png" width="240">

[0]: https://github.com/buomsoo-kim/Easy-deep-learning-with-Keras
