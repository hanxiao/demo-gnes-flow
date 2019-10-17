import os

from gnes.flow import Flow

from helper import read_flowers, bytes2ndarray

os.environ['TEST_WORKDIR'] = '/tmp/gnes-flow-demo'

flow = (Flow(check_version=False)
        .add_preprocessor(name='prep', yaml_path='yaml/prep.yml')
        .add_encoder(yaml_path='yaml/incep.yml')
        .add_indexer(name='vec_idx', yaml_path='yaml/vec.yml')
        .add_router(name='scorer', yaml_path='yaml/score.yml')
        .add_indexer(name='doc_idx', yaml_path='yaml/doc.yml'))

# checkout how the flow looks like
print(flow.build(backend=None).to_url())

num_q = 20
topk = 10
sample_rate = 0.05

# do the query
results = []
with flow.build(backend='process') as fl:
    for q, r in fl.query(bytes_gen=read_flowers(sample_rate)):
        q_img = q.search.query.raw_bytes
        r_imgs = [k.doc.raw_bytes for k in r.search.topk_results]
        r_scores = [k.score.value for k in r.search.topk_results]
        results.append((q_img, r_imgs, r_scores))
        if len(results) > num_q:
            break

# converts raw_bytes to 64x64 thumbnails for visualization
results_v = [(bytes2ndarray(q_img), [bytes2ndarray(r) for r in r_imgs], r_scores) for q_img, r_imgs, r_scores in
             results]

# plotting
import matplotlib.pyplot as plt

plt.close()
# first row: query. empty space for separation, 3rd to last: topk-results
f, ax = plt.subplots(topk + 2, num_q, figsize=(12, 8))

for q in range(num_q):
    ax[0][q].imshow(results_v[q][0])
    for r in range(topk):
        ax[r + 2][q].imshow(results_v[q][1][r])

# do some layout things
[aa.axis('off') for a in ax for aa in a]
plt.tight_layout()
plt.show()
