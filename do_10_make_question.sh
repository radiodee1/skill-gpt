cd ./src/ 

if [ $1 == "--mixed" ]; then

./convert_dialog_tab.py ../raw/movie_lines.txt --do_format 

fi

if [ $1 == "--safe" ]; then

./convert_dialog_tab.py ../raw/movie_lines.txt --do_format --tabname safe 

fi


if [ $1 == "--test" ]; then

./convert_dialog_tab.py ../raw/movie_lines.txt --do_format --tabname test 

fi
