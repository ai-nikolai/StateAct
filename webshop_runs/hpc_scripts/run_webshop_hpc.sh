# This script allows to navigate to the right directory inside the Singularity Container

cd /app

echo "Running Socket"

echo $1

./run_prod_docker.sh $1