# Webshop Environment

## Running the environment

```bash
docker run --rm -p 3000:3000 ainikolai/webshop:latest "0.0.0.0"
```

```bash
mkdir tmp
docker run --rm -v ./tmp:/tmp ainikolai/webshop:latest "unix:///tmp/webshop.sock"
```

## Running the experiments
```bash
pip3 install -r requirements.txt
```

```bash
python3 Webshop_adapted.py
```