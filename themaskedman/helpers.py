from .mask import Mask
import json
from typing import List

def write_masks_to_file(masks: List[Mask]):

    data = {}
    data['masks'] = []
    for m in masks:
        data['masks'].append(m.to_json())

    with open('data.txt','w') as outfile:
        json.dump(data,outfile)