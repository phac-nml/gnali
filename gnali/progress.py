"""
Copyright Government of Canada 2020

Written by: Xia Liu, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import time

from progress.spinner import Spinner
from multiprocessing import Pool


def show_progress_spinner(function, display_msg, fargs=()):
    spinner = Spinner(display_msg)
    pool = Pool(processes=1)
    async_result = pool.apply_async(function, fargs)
    while not async_result.ready() or not async_result.successful():
        spinner.next()
        time.sleep(0.2)
    print("\nDone")
    return async_result.get()
