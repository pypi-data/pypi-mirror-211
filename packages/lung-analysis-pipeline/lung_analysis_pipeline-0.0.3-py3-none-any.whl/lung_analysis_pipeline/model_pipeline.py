from lung_analysis_pipeline.Normalization_Pipeline.codes.models import create_model as create_normalization_model
from lung_analysis_pipeline.NoduleSeg_MedicalNet.build_unet_model import create_seg_model 
from lung_analysis_pipeline.Feature_Extractor.HSCNN.model import create_feat_extractor 
from lung_analysis_pipeline.Feature_Extractor.radiomics.feature_extractor import radiomic_feature_extractor 
from lung_analysis_pipeline.NoduleDetect_SANet import create_detect_model 
from lung_analysis_pipeline.utils import util
import numpy as np 
import os 
import torch


class ModelPipeline: 
    def __init__(self, opt):
        # self.models = models 
        self.opt = opt 
        self.check_order(opt)
        order = self.opt['order']
        if 'normalization' in order: 
            self.norm_model = create_normalization_model(opt)
        if 'detection' in order: 
            self.detect_model = create_detect_model(opt)
        if 'segmentation' in order: 
            self.seg_model = create_seg_model(opt)
        if 'feature_extraction' in order:
            self.feature_extractions = {}
            if 'deep_feature' in opt['feature_extraction']:
                self.feature_extractions['deep_feature'] = create_feat_extractor(opt)
            if 'radiomics' in opt['feature_extraction']:
                self.feature_extractions['radiomics'] = radiomic_feature_extractor(opt)
    def test(self, input_data): 
        
        if hasattr(self, 'norm_model'):
            input_data = self.norm_model.run_test(input_data)

            # save norm output 
            if self.opt['normalization']['output_path']:
                # print('saving norm')
                norm_results_dir = self.opt['normalization']['output_path']
                util.mkdir(norm_results_dir)

                sr_vol = util.tensor2img(input_data['volume'], out_type=np.uint16)
                util.save_vol(self.opt, [], norm_results_dir, input_data['uid'][0], sr_vol, dtype=self.opt['normalization']['output_dtype'])
        else: 
            input_data['volume'] = input_data['LR']
        
        if hasattr(self, 'detect_model'):
            detect_output = self.detect_model.run_test(input_data)
            # print(detect_output['detection_bboxes'])
            if self.opt['detection']['output_path']:
                util.save_detect_bbox(self.opt, detect_output)

        if hasattr(self, 'seg_model'): 
            if self.opt['segmentation']['use_decetion_bbox']: 
                seg_output = self.seg_model.run_test(detect_output) 
            else: 
                seg_output = self.seg_model.run_test(input_data) 
            if self.opt['segmentation']['output_path']:
                # seg_ressult_dir = os.path.join(results_dir, 'segmentation')
                seg_ressult_dir = self.opt['segmentation']['output_path']
                seg_result_dtype = self.opt['segmentation']['output_dtype']
                util.mkdir(seg_ressult_dir)

                seg_mask = util.tensor2mask(seg_output['seg_mask'][0][0], out_type=np.uint16)
                util.save_mask(self.opt, seg_output['input_info'], seg_ressult_dir, seg_result_dtype, seg_output['uid'][0], seg_mask)
        if hasattr(self, 'feature_extractions'): 
            for key, extractor in self.feature_extractions.items(): 
                # extract feature 
                feat_output = extractor.run_test(input_data, roi=self.opt['feature_extraction']['roi_source'], threshold_size=0)
                
                # only save results if output location is provided 
                if self.opt['feature_extraction'][key]['output_path']:
                    # save features 
                    
                    # util.save_feature_csv(feat_file, feat_dtype, feat_output['uid'][0], feat_output[key].cpu().numpy())
                    util.save_features(key, self.opt, feat_output)
        if self.opt['gpu_ids']: 
            torch.cuda.synchronize()

    """
    Check if specified operations are allowed. 
    """
    def check_order(self, opt): 
        order = opt['order']
        for i, ops in enumerate(order): 
            if not opt[ops]:
                raise ValueError('Please specify {} operation.'.format(ops))
            if ops == 'normalization': 
                if i != 0: 
                    raise ValueError('Normalization operation order not supported!')
            elif ops == 'segmentation': 
                # there has to exist detection before seg or use detection is set to false 
                if opt['segmentation']['use_decetion_bbox'] and not 'detection' in order[:i]: 
                    raise ValueError('Segmentation operation order not supported!')
                # check if the specified model is supported 
                if opt['segmentation']['model'] != 'unet': 
                    raise NotImplementedError('Model [{:s}] not implemented.'.format(opt['segmentation']['model']))
            elif ops == 'feature_extraction': 
                if not opt['feature_extraction']['roi_source']:
                    raise ValueError('Segmentation operation order not supported! Need to specify source of ROI.')
                if opt['feature_extraction']['roi_source'] == 'segmentation' and not 'segmentation' in order[:i]: 
                    raise ValueError('Feature extraction order not supported. Need to specify a segmentation method.')
                if opt['feature_extraction']['roi_source'] == 'detection' and not 'detection' in order[:i]: 
                    raise ValueError('Feature extraction order not supported. Need to specify a detection method.')
                if opt['feature_extraction']['roi_source'] == 'user' and not opt['dataset']['feature_roi_centroid']: 
                    raise ValueError('Feature extraction order not supported. Need to specify a ROI location.')
                if opt['feature_extraction']['roi_source'] == 'user' and not opt['dataset']['feature_mask']: 
                    raise ValueError('Feature extraction order not supported. Need to specify a mask location.')