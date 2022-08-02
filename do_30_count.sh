#rm ./data/tabname.maker.tsv

cd src

if [ $1 == "--mixed" ]; then

rm ./data/tabname.maker.tsv

./count_gpt_output.py gpt2 --screen 

./count_gpt_output.py gpt2-medium --screen

./count_gpt_output.py gpt2-large --screen

./count_gpt_output.py gpt2-xl --screen

./count_gpt_output.py gptj-pipeline --screen

./count_gpt_output.py gpt3-curie --screen

./count_gpt_output.py gpt3 --screen

./total_count_overall.py --screen

fi

if [ $1 == "--safe" ]; then


echo EleutherAI/gpt-neo-125M 
./count_gpt_output.py EleutherAI/gpt-neo-125M --screen --tabname safe 

## 1.3B
echo EleutherAI/gpt-neo-1.3B
./count_gpt_output.py EleutherAI/gpt-neo-1.3B --screen --tabname safe

## 2.7B
echo EleutherAI/gpt-neo-2.7B
./count_gpt_output.py EleutherAI/gpt-neo-2.7B --screen --online --tabname safe

./total_count_overall.py --screen --model_list EleutherAI/gpt-neo-125M,EleutherAI/gpt-neo-1.3B,EleutherAI/gpt-neo-2.7B --tabname safe

fi

if [ $1 == "--check" ]; then

./count_gpt_output.py EleutherAI/gpt-neo-1.3B --screen  --tabname check

./total_count_overall.py --screen --model_list EleutherAI/gpt-neo-1.3B --tabname check

fi


