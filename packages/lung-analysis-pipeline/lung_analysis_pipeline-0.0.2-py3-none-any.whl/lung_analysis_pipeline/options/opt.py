import os
import os.path as osp
import logging
from collections import OrderedDict
import json
import lung_analysis_pipeline.utils.util as util

def parse(opt_path, is_train=False):
    # remove comments starting with '//'
    json_str = ''
    with open(opt_path, 'r') as f:
        for line in f:
            line = line.split('//')[0] + '\n'
            json_str += line
    opt = json.loads(json_str, object_pairs_hook=OrderedDict)

    # results_root = opt['output']['output_location']
    # opt['output']['log'] = results_root
    # util.mkdir(results_root) 

    # For feature extraction, redirect to another file if the output path already exists 
    # for operation in ['feature_extraction', 'detection']:
    if 'feature_extraction' in opt: 
        for extractor in ['deep_feature', 'radiomics']:
            if extractor in opt['feature_extraction']:  
                opt['feature_extraction'][extractor]['output_path'] and os.path.exists(opt['feature_extraction'][extractor]['output_path'])
                filename = os.path.basename(opt['feature_extraction'][extractor]['output_path'])

                # Extract the file name without extension and append timestamp 
                file_name_without_ext = os.path.splitext(filename)[0]
                new_file_name = file_name_without_ext + util.get_timestamp() + os.path.splitext(filename)[1]

                # Get the directory of the path and new path 
                directory = os.path.dirname(opt['feature_extraction'][extractor]['output_path'])
                opt['feature_extraction'][extractor]['output_path'] = os.path.join(directory, new_file_name)
                
                logger = logging.getLogger('base')
                logger.info('File already exists. Rename it to [{:s}]'.format(opt['feature_extraction'][extractor]['output_path']))
   
    if 'detection' in opt and 'output_path' in opt['detection'] and os.path.exists(opt['detection']['output_path']): 
        filename = os.path.basename(opt['detection']['output_path'])

        # Extract the file name without extension and append timestamp 
        file_name_without_ext = os.path.splitext(filename)[0]
        new_file_name = file_name_without_ext + util.get_timestamp() + os.path.splitext(filename)[1]

        # Get the directory of the path and new path 
        directory = os.path.dirname(opt['detection']['output_path'])
        opt['detection']['output_path'] = os.path.join(directory, new_file_name)
        
        logger = logging.getLogger('base')
        logger.info('File already exists. Rename it to [{:s}]'.format(opt['detection']['output_path']))
    
    gpu_list = ','.join(str(x) for x in opt['gpu_ids']) if opt['gpu_ids'] else ""
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
    # print('export CUDA_VISIBLE_DEVICES=' + gpu_list)

    return opt

