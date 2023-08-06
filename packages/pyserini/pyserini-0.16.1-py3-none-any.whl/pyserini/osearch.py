#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys

# from pyserini.search.faiss import AnceEncoder
# from pyserini.search.faiss import DenseSearchResult, PRFDenseSearchResult, QueryEncoder, \
#     DprQueryEncoder, BprQueryEncoder, DkrrDprQueryEncoder, TctColBertQueryEncoder, AnceQueryEncoder, AutoQueryEncoder
# from pyserini.search.faiss import DenseVectorAveragePrf, DenseVectorRocchioPrf, DenseVectorAncePrf
# from pyserini.search.faiss import FaissSearcher, BinaryDenseSearcher as FaissBinaryDenseSearcher

import pyserini.search.faiss
from pyserini.search.faiss import TctColBertQueryEncoder

__all__ = ['SimpleDenseSearcher', 'BinaryDenseSearcher', 'TctColBertQueryEncoder']


class SimpleDenseSearcher(pyserini.search.faiss.FaissSearcher):
    def __new__(cls, *args, **kwargs):
        print('pyserini.dsearch.SimpleDenseSearcher class has been deprecated, '
              'please use FaissSearcher from pyserini.search.faiss instead')
        return super().__new__(cls)


class BinaryDenseSearcher(pyserini.search.faiss.BinaryDenseSearcher):
    def __new__(cls, *args, **kwargs):
        print('pyserini.dsearch.BinaryDenseSearcher class has been deprecated, '
              'please use BinaryDenseSearcher from pyserini.search.faiss instead')
        return super().__new__(cls)


if __name__ == "__main__":
    print('WARNING: pyserini.dsearch is deprecated, please use pyserini.search.faiss instead!')
    args = " ".join(sys.argv[1:])
    os.system(f'python -m pyserini.search.faiss {args}')
