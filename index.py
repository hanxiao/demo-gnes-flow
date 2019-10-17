import os

from gnes.flow import Flow

from helper import read_flowers

os.environ['TEST_WORKDIR'] = '/tmp/gnes-flow-demo'

# I didn't implement "incremental indexing" in this simple demo.
# So make sure you clean the existing index before doing `python index.py`
# $ rm $TEST_WORKDIR/*.bin

flow = (Flow(check_version=False, ctrl_with_ipc=True)
        .add_preprocessor(name='prep', yaml_path='yaml/prep.yml', replicas=5)
        .add_encoder(yaml_path='yaml/incep.yml', replicas=6)
        .add_indexer(name='vec_idx', yaml_path='yaml/vec.yml')
        .add_indexer(name='doc_idx', yaml_path='yaml/doc.yml', recv_from='prep')
        .add_router(name='sync', yaml_path='BaseReduceRouter', num_part=2, recv_from=['vec_idx', 'doc_idx']))

# checkout how the flow looks like (...and post it on Twitter, but hey what do I know about promoting OSS)
print(flow.build(backend=None).to_url())

with flow(backend='process') as fl:
    fl.index(bytes_gen=read_flowers(), batch_size=64)
