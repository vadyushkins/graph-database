if [ ! -f benchmarks/benchmark_rpq/myDataForRPQ.zip ]; then
  cd benchmarks/benchmark_rpq/
  gdown https://drive.google.com/uc?id=19L7RUCJlkgWQpQRnp6hMb7MLXibB4jTp
  cd ../../
fi

declare -a graphs=("LUBM300" "LUBM500" "LUBM1M" "LUBM1.5M" "LUBM1.9M" "geospecies" "proteomes" "mappingbased_properties_en" "uniprotkb_archea_asgard_group_1935183_0")

for graph in "${graphs[@]}"; do
  echo "Started benchmark $graph"
  python3 -m pytest -v -s benchmarks/benchmark_rpq/test_benchmark_rpq.py -m "$graph"
  echo "Ended benchmark $graph"
done