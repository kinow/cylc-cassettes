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


def get_query_suite_tasks_state_variables(workflow_id):
    return {
        "wIds": [
            workflow_id
        ],
        "minDepth": 0,
        "maxDepth": 4
    }


"""
{
  "wIds": ["%s"],
  "minDepth": 0,
  "maxDepth": 4 
}

"""

QUERY_SUITE_TASKS_STATE = """fragment treeNest on FamilyProxy {
  name
  cyclePoint
  state
  depth
  childTasks(ids: $nIds, states: $nStates, mindepth: $minDepth, maxdepth: $maxDepth) {
    id
    state
    latestMessage
    depth
    jobs {
      id
      host
      batchSysName
      batchSysJobId
      submittedTime
      startedTime
      finishedTime
      submitNum
    }
  }
}

query tree($wIds: [ID], $nIds: [ID], $nStates: [String], $minDepth: Int, $maxDepth: Int) {
  workflows(ids: $wIds) {
    id
    name
    status
    stateTotals {
      runahead
      waiting
      held
      queued
      expired
      ready
      submitFailed
      submitRetrying
      submitted
      retrying
      running
      failed
      succeeded
    }
    treeDepth
  }
  familyProxies(workflows: $wIds, ids: ["root"]) {
    ...treeNest
    childFamilies(mindepth: $minDepth, maxdepth: $maxDepth) {
      ...treeNest
      childFamilies(mindepth: $minDepth, maxdepth: $maxDepth) {
        ...treeNest
        childFamilies(mindepth: $minDepth, maxdepth: $maxDepth) {
          ...treeNest
          childFamilies(mindepth: $minDepth, maxdepth: $maxDepth) {
            ...treeNest
          }
        }
      }
    }
  }
}"""
