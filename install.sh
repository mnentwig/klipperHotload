#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
INSTALL_PATH="${HOME}/klipperHotload"

set -eu # strict
export LC_ALL=C

for file in "${INSTALL_PATH}"/klipper/extras/*.py; do ln -sfn "${file}" "${KLIPPER_PATH}/klippy/extras/"; done
echo "File linked."
echo "Now add [klipperHotload] to a configuration file and restart klipper."
echo "The 'U' G-code will be available (see README.md)"
