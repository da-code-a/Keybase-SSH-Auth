#!/bin/bash

keybase oneshot -u $KEYBASE_USERNAME --paperkey $KEYBASE_PAPERKEY
python3 /main.py