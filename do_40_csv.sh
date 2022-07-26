cd ./src/ 

if [ $1 == "--mixed" ]; then

./make_csv.py

fi

if [ $1 == "--safe" ]; then

./make_csv.py --tabname safe

fi

if [ $1 == "--test" ]; then

./make_csv.py --tabname test

fi
