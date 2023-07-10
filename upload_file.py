"""
API main reference https://pydataverse.readthedocs.io/en/latest/user/advanced-usage.html#upload-data-via-api
"""

from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
from credentials import *
import os
import pandas as pd
import time

# testing api connection
api = NativeApi(BASE_URL, API_TOKEN)
resp = api.get_info_version()
assert resp.status_code == 200, 'Unable to connect to the server'

# get a specific dataset with its persistentId
# http://13.212.78.188:8080/dataset.xhtml?persistentId=XXX&version=DRAFT
# XXX would be the persistentId, a DOI assigned by dataverser
dv = api.get_dataset(DATASET)

# load metadata TODO: this can be replace (or extent) with other metadata files
df_metadata = pd.read_csv('data/simplemaps.csv')

# main data folder and files
folder = DATA_PATH
ls_files = os.listdir(folder)


# loop over files located
start_time = time.time()
for single_file in ls_files:
    df = Datafile()
    df_filename = os.path.splitext(single_file)[0]

    # filter metadata
    df_filtered = df_metadata[df_metadata['uuid'] == df_filename]

    df.set({
        'pid': DATASET,
        'filename': df_filename,
        'description':
            df_filtered['source'].values[0] +
            ',' +
            df_filtered['city'].values[0] +
            ',' +
            df_filtered['country'].values[0]
    })

    resp = api.upload_datafile(DATASET, 'data/images/' +
                               df_filename + '.jpeg', df.json())
print(f"Seconds: {time.time() - start_time}")
print(resp.json())
