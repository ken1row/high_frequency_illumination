# Tools for high frequency illumination
Includes pattern generator and post process scripts.

## Dependencies
These scripts depend on python, numpy, and opencv.
For Ubuntu 14.04, these packages can be installed as:
```
sudo apt-get install libopencv-dev python python-numpy python-opencv
```

## generate_checer_board.py
Generates projection patterns.
Image size, pattern size, shift amount, and color are adjustable. See usage using ```-h``` option.

## separate_direct_global.py
Separates into direct and global components.

# Technical paper
This program implements the paper
S. Nayar et al. "Fast Separation of Direct and Global Components of a Scene using High Frequency Illumination", SIGGRAPH 2006.

# For Japanese
[こちらのページ](http://www.am.sanken.osaka-u.ac.jp/~tanaka/project/phfi-jp.html)で簡単な解説がご覧になれます．
