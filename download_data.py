from minio import Minio
import argparse
import os

def download_from_airlab_server(source_name, target_name):
    """
    Downloads a file using Minio.

    Args:

    Returns:
    """
    access_key = "UmeJIrIMssnBrrkwtjeB"
    secret_key = "CsE5zykgqc2zpS5EiMaBbZ6lfzq7riUXNWGnYQBW"
    endpoint_url = "airlab-share-01.andrew.cmu.edu:9000"

    client = Minio(endpoint_url,access_key=access_key,secret_key=secret_key,secure=True)
    bucket_name = "firestereo"
    
    print(f"Downloading {source_name} from {bucket_name}...")
    client.fget_object(bucket_name, source_name, target_name)
    print(f"Successfully downloaded {source_name} to {target_name}!")

    return True, target_name

def unzip(zip_file, out_dir):
    """
    Unzips a file.

    Args:

    Returns:
    """
    print('Unzipping', zip_file, 'to', out_dir)
    os.system(f"unzip -q -o {zip_file} -d {out_dir}")

def filter_data_type(type, files):
    if type:
        filtered = [f for f in files if type in f]
        return filtered
    else:
        return files
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Download data from the Airlab server.")
    parser.add_argument('--out_dir', default='./firestereo', help="Root directory to save the downloaded data.")
    parser.add_argument('--unzip', action='store_true', help="Unzip the downloaded files.")
    parser.add_argument('--data', nargs='+', help="Type of data to download: all (default), depth, thermal")
    args = parser.parse_args()
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    files = [f.rstrip() for f in open('download.txt', 'r')]
    files = filter_data_type(args.data, files)
    for file in files:
        res, saved_file = download_from_airlab_server(file, os.path.join(args.out_dir, file))
        if args.unzip:
            subdir = file.split('/')[0]
            unzip(saved_file, os.path.join(args.out_dir, subdir))