#!/bin/sh

flake1=$(python3 -m flake8 tilewe example_*.py --count --select=E9,F63,F7,F82 --show-source --statistics)
flake2=$(python3 -m flake8 tilewe example_*.py --count --exit-zero --max-complexity=25 --max-line-length=127 --ignore=W291,W293,W504,E128,E201,E202,E252,E302,E305 --statistics)
if [ "$flake1" = "0" ] && [ "$flake2" = "0" ]; then
    echo "passed all flake tests"
else
    if [ "$flake1" != "0" ]; then
        echo "$flake1"
    fi
    if [ "$flake2" != "0" ]; then
        echo "$flake2"
    fi
    echo "failed some flake tests"
    exit 1
fi