rm ./data/tabname.maker.tsv

cd src

./count_gpt_output.py gpt2 --screen 

./count_gpt_output.py gpt2-medium --screen

./count_gpt_output.py gpt2-large --screen

./count_gpt_output.py gpt2-xl --screen

./count_gpt_output.py gptj-pipeline --screen

./count_gpt_output.py gpt3-curie --screen

./count_gpt_output.py gpt3 --screen

./total_count_overall.py --screen
