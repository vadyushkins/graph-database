if [ ! -f benchmarks/benchmark_cfpq/myDataForCFPQ.tar.xz ]; then
  cd benchmarks/benchmark_cfpq/
  gdown https://drive.google.com/uc?id=1UDw3OTJG25GM8z_R84D8WiiTkuLxCfLM
  cd ../../
fi

declare -a graphs=("MemoryAliases" "FullGraph" "WorstCase" "SparseGraph")

for graph in "${graphs[@]}"; do
  echo "Started benchmark $graph"
  python3 -m pytest -v -s benchmarks/benchmark_cfpq/test_benchmark_cfpq.py -m "$graph"
  echo "Ended benchmark $graph"
done
