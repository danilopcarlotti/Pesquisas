#!/bin/bash
for filename in *.txt; do cat $filename > ${filename::-4}.csv; rm $filename; done
