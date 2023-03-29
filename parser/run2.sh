# You need miniconda https://docs.conda.io/en/latest/miniconda.html

git clone git@github.com:allenai/s2orc-doc2json.git
cd s2orc-doc2json
pip3 install -r requirements.txt
python3 setup.py develop
bash scripts/setup_grobid.sh
bash scripts/run_grobid.sh
cd ..