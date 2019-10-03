import os
import random

import youtokentome as yttm
from utils_for_testing import (
    BASE_MODEL_FILE,
    RENAME_ID_MODEL_FILE,
    TEST_FILE,
    TRAIN_FILE,
    file_starts_with,
    generate_artifacts,
)


def test_encode_decode():
    generate_artifacts()
    os.remove(BASE_MODEL_FILE)
    yttm.BPE.train(data=TRAIN_FILE, vocab_size=16000, model=BASE_MODEL_FILE)

    bpe = yttm.BPE(BASE_MODEL_FILE)
    text_in = [" ".join("".join([random.choice("abcd ") for _ in range(50)]).split())]
    ids = bpe.encode(text_in, yttm.OutputType.ID)
    assert text_in == bpe.decode(ids)


def test_vocabulary_consistency():
    generate_artifacts()
    os.remove(BASE_MODEL_FILE)
    yttm.BPE.train(data=TRAIN_FILE, vocab_size=16000, model=BASE_MODEL_FILE)

    bpe = yttm.BPE(BASE_MODEL_FILE)
    assert bpe.vocab_size() == len(bpe.vocab())
    assert bpe.vocab_size() == len(set(bpe.vocab()))
    vc = bpe.vocab()
    for i, subword in enumerate(vc):
        assert i == bpe.subword_to_id(subword)
        assert subword == bpe.id_to_subword(i)
