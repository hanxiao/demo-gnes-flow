# GNES Flow Demo 

Since `v0.0.46` GNES Flow has become the main interface of GNES. GNES Flow provides a **pythonic** and **intuitive** way to implement a pipeline, enabling users to run or debug GNES on a local machine. By default, GNES Flow orchestrates all microservices using multi-thread or multi-process backend, it can be also exported to a Docker Swarm/Kubernetes YAML config, allowing one to deliver GNES to the cloud.

In this demo, our goal is to build a toy image search engine using GNES Flow API. 

## Files

For first-time users, simply open `flower.ipynb` and follow the steps there.

- `flower.ipynb`: a self-contained Jupyter notebook with a step-by-step explanation 
- `index.py`: the indexing part of `flower.ipynb`, for indexing all images.
- `query.py`: the querying part of `flower.ipynb`, for querying sampled images and plotting top-10 results

## Requirements

```text
gnes>=0.0.46
image
tensorflow==1.12
```

You can install them via `pip install .`. However, you may want to do that in a virtual env though as it will replace your local Tensorflow with `tensorflow==1.12`. Feel free to [contribute and waive this particular requirement](https://github.com/gnes-ai/demo-gnes-flow/pulls).

## Troubleshooting

#### Can not load indexer when indexing twice

I didn't implement features like "incremental indexing" in this simple demo. So please make sure you clean up the existing index before doing `python index.py`. 
```bash
rm $TEST_WORKDIR/*.bin
```

#### `OSError: [Errno 24] Too many open files`

This often happens when `replicas`/`num_parallel` is set to a big number. Solution to that is to increase this (session-wise) allowance via:

```bash
ulimit -n 4096
```

#### `objc[15934]: +[__NSPlaceholderDictionary initialize] may have been in progress in another thread when fork() was called.`

Probably MacOS only. 
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

#### Why `tensorflow==1.12`, why not 2.0?

In this demo, I simply use the inceptionV4 model from `tf.contrib.slim`. There are some major changes in TF2.0, and the model can not be directly used. Fortunately, contribute/port an external model to GNES is extremely simple. Feel free to [follow the instruction in GNES Hub](https://github.com/gnes-ai/hub) and make a contribution to this demo.

#### It stuck/crash in Jupyter Notebook

Please try running `python index.py` or `python query.py` outside the Jupyter Notebook. As far as I know, Jupyter Notebook is employing ZeroMQ in the backend and this can sometimes mess up with GNES sockets (or the other way around). If you find the demo still crash/stuck when running as independent Python script, then please report an [issue to this repository](https://github.com/gnes-ai/demo-gnes-flow/issues) or the [GNES main repository](https://github.com/gnes-ai/gnes/issues).  
 