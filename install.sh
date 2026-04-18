#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
INSTALL_PATH="${HOME}/klipperHotload"

set -eu # strict
export LC_ALL=C

# link all python files, all directories
for file in "${INSTALL_PATH}"/klipper/extras/*.py "${INSTALL_PATH}"/klipper/extras/*/; do ln -sfn "${file}" "${KLIPPER_PATH}/klippy/extras/"; done
echo "File linked."
echo "Now add [klipperHotload] to a configuration file and restart klipper."
echo "The 'U' G-code will be available (see README.md)"
