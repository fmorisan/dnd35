#!/bin/sh

cat ../skills/* | grep ability | grep -v Hablar | sort | uniq | cut -d\" -f4 | sed "s/^/\"/g" | sed "s/\$/\"/g" | jq -s > ../attributes.json
