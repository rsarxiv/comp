#!/usr/bin/env bash
#
# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

../../fastText/fasttext supervised -input train.data -output model -dim 100 -lr 0.1 -wordNgrams 3 -minCount 1 -bucket 10000000 -epoch 5 -thread 4

# ../../fastText/fasttext test model.bin valid.data

../../fastText/fasttext predict model.bin test.data > result.txt
