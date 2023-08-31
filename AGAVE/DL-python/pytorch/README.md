pytorch examples
================

The tutorial pages provided by `pytorch` are used for this section.

* [Data Loading Example tutorial][0]
* [Data Loading Example ipynb download][1]
* [Transfer Learning tutorial][2]
* [RNN tutorial][3]
* [Nice RNN link from tutorial][4]

Setup
-----

Tested on node `cg20-10` (8 Tesla V100s)

Run the following `conda` command to install the `pytorch` enviroment
built for this exercise

    interactive -t 60 -p gpu -q wildfire --gres=gpu:V100:1
    module load anaconda/py3
    conda env create -f environment.yml
    source activate pytorch


<img src="../../assets/ASURC_logo.png" width="240">


[0]: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
[1]: https://pytorch.org/tutorials/_downloads/21adbaecd47a412f8143afb1c48f05a6/data_loading_tutorial.ipynb
[2]: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
[3]: https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html
[4]: https://karpathy.github.io/2015/05/21/rnn-effectiveness/
