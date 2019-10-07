GPU
===

To have a GPU powered notebook, conduct the following steps:

1. Connect to agave
2. sbatch a jupyter job to a gpu node, i.e.


```
    sbatch -p gpu -q wildfire --gres=gpu:GTX1080:1 -t 60 << EOF
    #!/bin/bash
    module load anaconda/py3
    source activate rapidsWS
    jupyter notebook --port=29292 --no-browser
    EOF
```

3. Note the compute node associated with the gpu job, e.g. cg19-6
4. From your local computer, issue the following in a terminal:

```
   ssh -t -t agave -L 8888:localhost:8888 ssh cg19-6 -L 8888:localhost:29292
```

Note: The port number on the compute node and the head node may need to
change, as well as the compute node specification, e.g.:

```
   ssh -t -t <asurite>@agave.asu.edu -L 8888:localhost:<login_port> ssh <compute_node> -L 8888:localhost:<compute_port>
```
   





   
