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

import shutil
import os
from contextlib import closing
import urllib.request as request
from gnali.exceptions import ReferenceDownloadError


def download_file(url, dest_path, max_time):
    """Download a file from a url.

    Args:
        url: url for a file
        dest_path: where to save file
        max_time: maximum time to wait for
                  download. An exception is
                  raised if download doesn't
                  complete in this time.
    """
    file_type = url.split(":")[0]
    try:
        if file_type == 'ftp':
            with closing(request.urlopen(url)) as resp:
                with open(dest_path, 'wb') as fh:
                    shutil.copyfileobj(resp.raw, fh)
        else:
            with request.urlopen(url) as resp:
                with open(dest_path, 'wb') as fh:
                    shutil.copyfileobj(resp, fh)

    except Exception:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise ReferenceDownloadError("Error downloading {}".format(url))
