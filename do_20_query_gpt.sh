cd ./src/ 

./query_gpt_model.py gpt2 --screen 

./query_gpt_model.py gpt2-medium --screen

./query_gpt_model.py gpt2-large --screen

./query_gpt_model.py gpt2-xl --screen

echo "The gptj-pipeline gpt test takes approximately one hour."

./query_gpt_model.py gptj-pipeline --screen

echo "The gpt3 test takes longer than the gpt2 tests, possibly 40 minutes."

./query_gpt_model.py gpt3 --screen

echo "This script only runs some of the gpt tests."
