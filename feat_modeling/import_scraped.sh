#!/bin/sh

for f in $(ls ../feats)
do
    echo "Ingesting $f"
    ./manage.py ingest_feat ../feats/$f
done