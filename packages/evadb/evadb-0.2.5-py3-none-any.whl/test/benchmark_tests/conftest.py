# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from eva.catalog.catalog_manager import CatalogManager
from eva.server.command_handler import execute_query_fetch_all
from eva.udfs.udf_bootstrap_queries import init_builtin_udfs


@pytest.fixture(autouse=False)
def setup_pytorch_tests():
    CatalogManager().reset()
    execute_query_fetch_all("LOAD VIDEO 'data/ua_detrac/ua_detrac.mp4' INTO MyVideo;")
    execute_query_fetch_all("LOAD VIDEO 'data/mnist/mnist.mp4' INTO MNIST;")
    execute_query_fetch_all("LOAD VIDEO 'data/sample_videos/touchdown.mp4' INTO VIDEOS")
    init_builtin_udfs(mode="release")
    yield None
