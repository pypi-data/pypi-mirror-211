#!/usr/bin/python
#
#  Copyright 2002-2022 Barcelona Supercomputing Center (www.bsc.es)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import os
import pycompss_cli.cli.pycompss as pycompss


def main():
    # Force to use the dislib image by default
    os.environ['DEFAULT_DISLIB_DOCKER_IMAGE'] = 'bscwdc/dislib:latest'
    pycompss.main()

if __name__ == "__main__":
    main()
