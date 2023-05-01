# You need miniconda https://docs.conda.io/en/latest/miniconda.html

cd s2orc-doc2json
pip3 install -r requirements.txt
python3 setup.py develop
chmod +x scripts/*.sh
bash scripts/setup_grobid.sh
bash scripts/run_grobid.sh
cd ..