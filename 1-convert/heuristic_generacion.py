############################################
#######  GENERACION HEURISTIC FILE   #######
#######       PENLab Jan 2026        #######
############################################

import os

grouping = 'all'                   # change it to 'all' if Study Identifier UID error appears

delete_scans = True
delete_events = True

# create files function
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    # paths for the desired output BIDS. Further BIDS paths must follow BIDS
    # specification filenames: https://bids.neuroimaging.io/getting_started/folders_and_files/files.html
    
    t1w=create_key('sub-{subject}/anat/sub-{subject}_run-{item:02d}_T1w')
    
    rest_bold=create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_bold')
    pain_bold=create_key('sub-{subject}/func/sub-{subject}_task-pain_run-{item:02d}_bold')
    multisens_bold=create_key('sub-{subject}/func/sub-{subject}_task-multisens_run-{item:02d}_bold')
    selfvowel_bold=create_key('sub-{subject}/func/sub-{subject}_task-selfvowel_run-{item:02d}_bold')
    nback_bold=create_key('sub-{subject}/func/sub-{subject}_task-nback_run-{item:02d}_bold')

    dwi=create_key('sub-{subject}/dwi/sub-{subject}_dir-AP_run-{item:02d}_dwi')

    dwi_b0_pa=create_key('sub-{subject}/fmap/sub-{subject}_dir-PA_acq-DWI_run-{item:02d}_epi')

    # dictionary: list of DICOMs for each BIDS file
    info =  {
                    t1w:[],
                    rest_bold:[],
                    pain_bold:[],
                    multisens_bold:[],
                    selfvowel_bold:[],
                    nback_bold:[],
                    dwi:[],
                    dwi_b0_pa:[],
             }

    # append DICOMS to dictionary keys --> to change in function of protocol_name,
    # can be found in <bidspath>/.heudiconv/<subject>/ses-<session>/info/dicominfo_ses-<session>.tsv
    # test heudiconv can be done by 'heudiconv --files <dicoms_path>/<subject>/*/*/*/*/*.dcm -o <bids_path>/ -f convertall -s <subject> -c none -g all' on command
    
    for s in seqinfo:
       
        #anat
        if s.protocol_name=='t1_mprage_sag_p3_iso_Munich':
            info[t1w].append(s.series_id)   

        #func
        if s.protocol_name=='resting MULTI a-p ADAPTADO' and s.series_description[-6:] != '_SBRef':
                info[rest_bold].append(s.series_id)
        elif 'DOLOR' in s.protocol_name and s.series_description[-6:] != '_SBRef':            
            info[pain_bold].append(s.series_id)
        elif 'MULTISENSORIAL' in s.protocol_name and s.series_description[-6:] != '_SBRef':            
            info[multisens_bold].append(s.series_id)
        elif 'AUTOJUICIO' in s.protocol_name and s.series_description[-6:] != '_SBRef':            
            info[selfvowel_bold].append(s.series_id)
        elif 'NBACK' in s.protocol_name and s.series_description[-6:] != '_SBRef':            
            info[nback_bold].append(s.series_id)

        #dwi
        if s.protocol_name=='DWI_ FASTnFURIUS AP 2X2X2' and s.series_description[-7:] != '_TRACEW':
            info[dwi].append(s.series_id)

        #fmap
        if s.protocol_name=='2_B0_PA':
            info[dwi_b0_pa].append(s.series_id)     

    return info

# Fill the IntendedFor metadata field for fmap files
POPULATE_INTENDED_FOR_OPTS = {
        'matching_parameters': ['ImagingVolume', 'Shims'],
        'criterion': 'Closest'
}