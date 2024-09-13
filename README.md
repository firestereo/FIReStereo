<p align="center">

  <h1 align="center">FIReStereo: Forest InfraRed Stereo Dataset for UAS Depth Perception in Visually Degraded Environments</h1>
  <p align="center">
  Devansh Dhrafani*, Yifei Liu*, Andrew Jong, Ukcheol Shin, Yao He, Tyler Harp, Yaoyu Hu, Jean Oh, Sebastian Scherer</p>
  <h3 align="center"><a href="http://arxiv.org/abs/2409.07715">Paper</a> | <a href="https://firestereo.github.io/">Project Page</a></h3>

</p>

### Download data
1. Obtain access keys by filling out a simple [survey](https://forms.gle/Vor6LEKXtk6FCaxj9).
2. Paste the keys into `download_data.py`.
```bash
pip install minio tqdm
python download_data.py [--outdir] [--unzip] [--data]
```
- `--data`: select `depth` for our stereo thermal & depth collection, or `thermal` for the collection featuring prescribed fire and smoke

### Stay tuned for visualization tool, dataloader, training scripts, and models.