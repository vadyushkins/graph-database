conda activate test-environment || activate test-environment
rm -rf .benchmarks
python3 -m pytest -v -s tests/benchmark_rpq/test_benchmark_rpq.py -m --benchmark-autosave --benchmark-save-data
pytest-benchmark compare --name=short --csv=RPQ
cat RPQ.csv