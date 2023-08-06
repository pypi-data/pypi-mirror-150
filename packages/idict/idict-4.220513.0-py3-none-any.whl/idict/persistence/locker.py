#  Copyright (c) 2022. Davi Pereira dos Santos
#  This file is part of the i-dict project.
#  Please respect the license - more about this in the section (*) below.
#
#  i-dict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  i-dict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with i-dict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#

import shelve
from contextlib import contextmanager
from datetime import datetime, timedelta

from temporenc import packb, unpackb


def locker(iterable, dict_shelf=None, timeout=3600, logstep=1):
    """
    Generator that skips items from 'iterable' already processed before or still being processed

    Item processing is restarted if 'timeout' expires.
    'dict_shelf' is a dict-like or a shelve-like object to store each item status
        when 'None', 'shelve.open("/tmp/locker.db")' will be used
    'logstep' is the frequency of printed messages, 'None' means 'no logs'.

    >>> from time import sleep
    >>> names = ["a","b","c","d","e"]
    >>> storage = {}
    >>> for name in locker(names, dict_shelf=storage, timeout=10):
    ...    print(f"Processing {name}")
    ...    sleep(1)
    ...    print(f"{name} processed!")
    'a' is new, started
    Processing a
    a processed!
    'b' is new, started
    Processing b
    b processed!
    'c' is new, started
    Processing c
    c processed!
    'd' is new, started
    Processing d
    d processed!
    'e' is new, started
    Processing e
    e processed!
    """
    if dict_shelf is None:
        contextm = shelve.open("/tmp/locker.db")
    elif hasattr(dict_shelf, "__contains__"):
        @contextmanager
        def ctx():
            yield dict_shelf

        contextm = ctx()
    else:
        contextm = dict_shelf

    with contextm as dic:
        for c, item in enumerate(iterable):
            if item in dic:
                val = dic[item]
                if val == b'd':
                    status, action = 'already done', "skipping"
                elif datetime.now() > unpackb(val).datetime() + timedelta(seconds=timeout):
                    status, action = "expired", "restarted"
                else:
                    status, action = 'already started', "skipping"
            else:
                status, action = "is new", "started"
            if logstep is not None and c % logstep == 0:
                print(f"'{item}' {status}, {action}")
            if action != "skipping":
                dic[item] = packb(datetime.now())
                yield item
                dic[item] = b'd'
