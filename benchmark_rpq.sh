bash install.sh
cd tests/benchmark_rpq/ ; gdown https://drive.google.com/uc?id=1ZZ8FI6MxQ2rWIRxBQjZOVw64zHdbxcmm ; cd ../../
rm -rf .benchmarks
pwd
python3 -m pytest -v -s tests/benchmark_rpq/test_benchmark_rpq.py --benchmark-autosave --benchmark-save-data
pytest-benchmark compare --name=short --csv=RPQ
cat RPQ.csv