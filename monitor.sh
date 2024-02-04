#!/bin/bash

TARGET=$1
TARGET=${TARGET%.py}
EVENTS="modify"

switch=1

inotifywait -m -r -e "$EVENTS" "${TARGET}.py" | while read -r _ action _; do
    if [ $switch = 1 ]; then
        echo "[I] Detected $action on target $TARGET - $(date +"%T")"
        if [[ -e "./args/$TARGET" ]]; then
            echo "[I] Generating from template args..."
            python "${TARGET}.py" < "./args/${TARGET}" > "result/${TARGET}.aff"
        else
            echo "[E] Argument template not exist" >&2
        fi
        switch=0
    else
        switch=1
    fi
done
