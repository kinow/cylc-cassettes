#!/usr/bin/env python

# Copyright 2019 Bruno P. Kinoshita
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

QUERY_SUITE_STATE = """{
    workflows {
        id
        name
        owner
        host
        port
    }
}
"""

QUERY_SUITE_TASKS_STATE = """{
    workflows {
        id
        owner
        name
        host
        port
        tasks {
            id
            name
            meta {
                title
                description
                URL
            }
            meanElapsedTime
            namespace
            proxies {
                id
            }
        }
    }
}
"""
