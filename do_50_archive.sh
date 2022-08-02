#!/bin/bash

#mixed
#safe
#check

cd ./data/ 

NAME="skill-"

if [ $1 == "--mixed" ]; then

echo $NAME
zip ${NAME}tabname.zip tabname*
mv ${NAME}tabname.zip ..

fi 

if [ $1 == "--safe" ]; then

echo $NAME

zip ${NAME}safe.zip safe*
mv ${NAME}safe.zip ..

fi

if [ $1 == "--check" ]; then

echo $NAME

zip ${NAME}check.zip check*
mv ${NAME}check.zip ..

fi

if [ $1 == "--test" ]; then

echo $NAME

zip ${NAME}test.zip test*
mv ${NAME}test.zip ..

fi
