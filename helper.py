import io
import os
import random
import tarfile

import numpy as np
from PIL import Image


def read_flowers(sample_rate=1.0):
    with tarfile.open(os.path.join(os.environ['TEST_WORKDIR'], '17flowers.tgz')) as fp:
        for m in fp.getmembers():
            if m.name.endswith('.jpg') and random.random() <= sample_rate:
                yield fp.extractfile(m).read()


def bytes2ndarray(i, max_size=48):
    img = Image.open(io.BytesIO(i))
    img.thumbnail((max_size, max_size))
    return np.asarray(img)
