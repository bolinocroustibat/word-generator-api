#!/bin/sh

mkdir cmd
mkdir lib
mkdir bin
mkdir doc
echo ''

tar -zxf tree-tagger-MacOSX-3.2.3.tar.gz
echo 'TreeTagger version for Mac OS-X installed.'

gzip -cd tagger-scripts.tar.gz | tar -xf -
chmod +x cmd/*
echo 'Tagging scripts installed.'

gzip -cd french.par.gz > lib/french.par
echo 'French parameter file installed.'

for file in cmd/*
do
    awk '$0=="BIN=./bin"{print "BIN=\"'`pwd`'/bin\"";next}\
         $0=="CMD=./cmd"{print "CMD=\"'`pwd`'/cmd\"";next}\
         $0=="LIB=./lib"{print "LIB=\"'`pwd`'/lib\"";next}\
         {print}' $file > $file.tmp;
    mv $file.tmp $file;
done
echo 'Path variables modified in tagging scripts.'

chmod 0755 cmd/*

echo ''
echo 'You might want to add '`pwd`'/cmd and '`pwd`'/bin to the PATH variable so that you do not need to specify the full path to run the tagging scripts.'
echo ''
