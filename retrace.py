#!/usr/bin/env python3
# we need to fix the above line so that the virtualenv
# is used instead of the system-wide python3

# retrace.py: retraces our steps for us

# the idea here is to look at the scripts which do

# 1) raw data files -> L0
# 2) L0 -> L1
# 3) etc

# and see if the data in the relevant data tables
# is older than the script that created it. This
# would indicate that the script would need to be
# re-run. Sort of like a make system for data,
# except that it will work across git and postres

import psycopg2
import git
import sys
import datetime

# first get a repository object. The script should
# be run in the directory where the .git directory
# is located.

repo = git.Repo()

# it's not empty, and we've been diligent in tracking
# everything. Also, everything that is tracked is 
# committed to the repository.
assert not repo.bare
assert len(repo.untracked_files) == 0
assert not repo.is_dirty()

head = repo.head
master = head.reference
log = master.log()


# we need to figure out how to add a timezone to this:
# gitpython works in seconds west of UTC.
# the following is pseudocode:
tz = timezone.fromsecondswestofUTC(log[-1][3][1])

lastcommit = datetime.fromtimestamp(log[-1][3][0],tz=tz)
