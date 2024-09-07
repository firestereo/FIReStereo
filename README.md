<p align="center">

  <h1 align="center">FIReStereo: Forest InfraRed Stereo Dataset for UAS Depth Perception in Visually Degraded Environments</h1>
</p>

### Download data
```bash
pip install minio
python download_data.py [--outdir] [--unzip] [--data]
```
- `--data`: select `depth` for our stereo thermal & depth collection, `thermal` for thermal only collection in prescribed fire and smoke