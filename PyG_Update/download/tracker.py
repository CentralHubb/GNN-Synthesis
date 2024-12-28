from google.cloud import storage 
import os 
import torch 
import subprocess 
import re 
from torch_geometric.data import Data 
 
service_account = "../gnn-for-synthesis-f4d9ad3451da.json" 
storage_client = storage.Client.from_service_account_json(service_account) 
 
bucket_name = "synthesis-data-bucket" 
bucket = storage_client.bucket(bucket_name) 
directory = "OPENABC2_DATASET/processed" 
directory2 = "OPENABC2_DATASET/new_pg_processed" 
 
pt_files = bucket.list_blobs(prefix=directory) 
pt_list = [pt.name for pt in pt_files]
new_pt = bucket.list_blobs(prefix=directory2)
new_pt_list = [pt.name for pt in new_pt]

print(f"{len(new_pt_list)}/{len(pt_list)} convertered")


