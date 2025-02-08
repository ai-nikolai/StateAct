# If you have a PBS (or similarly SLURM) cluster.

## Prepare the image and run:
1. Download image: (e.g. into webshop_run)
```bash
singularity pull --name webshop.simg docker://ainikolai/webshop:latest
```

2. Run singularity: (The below could be the content of the pbs script)

```bash
mkdir -p tmp #create the tmp directory inside webshop_runs

SOCKET="unix:///tmp/webshop.sock"

singularity exec --writable-tmpfs -B $MY_HOME/stateact/webshop_runs/tmp:/tmp $MY_HOME/stateact/webshop_runs/webshop.simg $MY_HOME/stateact/webshop_runs/hpc_scripts/run_webshop_hpc.sh $SOCKET &

sleep 30 #increase this number if necessary

curl --unix-socket ./tmp/webshop.sock localhost/abc
```


## In case of problems
(optional) In case you don't have temp file-system permissions for singularity (i.e. the above did not work, because of `--writable-tmpfs`).

1. First create an overlay:
```bash
singularity overlay create --size 500 webshop_overlay.img #create an overlay size 500MB
```

2. Run Singularity: (The below could be the content of the pbs script)
```bash
mkdir -p tmp #create the tmp directory inside webshop_runs

SOCKET="unix:///tmp/webshop.sock"

singularity exec --userns --overlay $MY_HOME/stateact/webshop_runs/webshop_overlay.img -B $MY_HOME/stateact/webshop_runs/tmp:/tmp $MY_HOME/stateact/webshop_runs/webshop.simg $MY_HOME/stateact/webshop_runs/hpc_scripts/run_webshop_hpc.sh $SOCKET &

sleep 30 #increase this number if necessary

curl --unix-socket ./tmp/webshop.sock localhost/abc
```

---
## To then Run Webshop in the same PBS script:
```bash
python3 WebShop_adapted.py --llm_type LOCAL --socket ./tmp/webshop.sock
```
