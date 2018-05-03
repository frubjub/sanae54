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


