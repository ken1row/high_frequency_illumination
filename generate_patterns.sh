#!/bin/bash

d='illumination'

rm -rf $d
mkdir $d
cd $d
python ../generate_checker_board.py

