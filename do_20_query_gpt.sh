cd ./src/ 

#echo $@

if [ $1 == "--test" ]; then

#touch ../data/test.tsv

./query_gpt_model.py EleutherAI/gpt-neo-2.7B --screen --online  --tabname test 

echo test 

fi


if [ $1 == "--mixed" ]; then

./query_gpt_model.py gpt2 --screen 

./query_gpt_model.py gpt2-medium --screen

./query_gpt_model.py gpt2-large --screen

./query_gpt_model.py gpt2-xl --screen

echo "The gptj-pipeline gpt test takes approximately one hour."

./query_gpt_model.py gptj-pipeline --screen

echo "The gpt3 test takes longer than the gpt2 tests, possibly 40 minutes."

./query_gpt_model.py gpt3 --screen

echo "This script only runs some of the gpt tests."

fi

if [ $1 == "--safe" ]; then

echo EleutherAI/gpt-neo-125M 
./query_gpt_model.py EleutherAI/gpt-neo-125M --screen --tabname safe 

## 1.3B
echo EleutherAI/gpt-neo-1.3B
./query_gpt_model.py EleutherAI/gpt-neo-1.3B --screen --tabname safe

## 2.7B
echo EleutherAI/gpt-neo-2.7B
./query_gpt_model.py EleutherAI/gpt-neo-2.7B --screen --online --tabname safe


fi
