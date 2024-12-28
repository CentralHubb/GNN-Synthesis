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
new_pt = bucket.list_blobs(prefix=directory2)
new_pt_list = [pt.name for pt in new_pt]
pattern = r"^[a-zA-Z0-9_]+_syn\d+_step\d+\.pt$"

count = 0 
max_count = 1
pt_list = []
for pt in pt_files:
    if count < max_count: 
        #if pt.name.endswith(".pt"):
        if re.match(pattern, os.path.basename(pt.name)):
            new_name = "OPENABC2_DATASET/new_pg_processed/" + os.path.basename(pt.name)
            #print(f"New name: {new_name}")
            #print(new_pt_list[0])
            if new_name not in new_pt_list:
                #print(pt.name)
                old_file = "./old_pt/" + os.path.basename(pt.name)
                print(f"Downloading {pt.name} to {old_file}.")
                pt.download_to_filename(old_file)
                try: 
                    dataset = torch.load(old_file)
                    #print(dataset)
                    print(f"Converting old file to dict")
                    data_dict = {}
                    for key in dataset.keys:
                        data_dict[key] = dataset[key]
                    data_file = "../data/" + os.path.basename(pt.name)
                    print(f"Saving {os.path.basename(pt.name)} data to {data_file}.")
                    torch.save(data_dict, data_file)
                    #delete old file from old_pt
                    print(f"Deleteing old_file at {old_file}")
                    os.remove(old_file)
                except ModuleNotFoundError:
                    print("Incorrect PyG version")
                #count += 1
            else:
                pass
                #print(f"File {pt.name} has already been updated")
        else:
            print(f"File {pt.name} is not a .pt file that represents  ip-recipe-step information.")
    else:
        break



