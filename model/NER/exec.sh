#!/bin/sh
../CRF++-0.58/crf_learn -c 4.0 template T.data model
../CRF++-0.58/crf_test -m model V.data >> output.txt

# ../../crf_learn -a MIRA template train.data model
# ../../crf_test -m model test.data

#../../crf_learn -a CRF-L1 template train.data model
#../../crf_test -m model test.data

