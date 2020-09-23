if [ ! -f benchmarks/benchmark_rpq/myDataForRPQ.zip ]; then
  cd benchmarks/benchmark_rpq/
  gdown https://drive.google.com/uc?id=19L7RUCJlkgWQpQRnp6hMb7MLXibB4jTp
  cd ../../
fi
python3 -m pytest -v -s benchmarks/benchmark_rpq/test_benchmark_rpq.py -m "(LUBM300) or (LUBM500)"