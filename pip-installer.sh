#!/usr/bin/env bash
FREZE_TMPFILE_ORIG=/tmp/freeze-orig.txt
FREZE_TMPFILE=/tmp/freeze.txt

set -x

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

pip freeze > $FREZE_TMPFILE_ORIG
pip install $1
pip freeze > $FREZE_TMPFILE

diff $FREZE_TMPFILE_ORIG $FREZE_TMPFILE

