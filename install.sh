conda --version
if [[ $? -ne 0 ]]; then
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
  bash miniconda.sh -b -p $HOME/miniconda
  source "$HOME/miniconda/etc/profile.d/conda.sh"
  conda init
  source "$HOME/.bashrc"
  hash -r
  conda config --set always_yes yes --set changeps1 yes
  conda update -q conda
  # Useful for debugging any issues with conda
  conda info -a
fi
conda config --add channels conda-forge
conda create -q -n graph-database-environment python=3.8 pygraphblas pytest
conda activate graph-database-environment
conda install pygraphblas
pip install -r requirements.txt