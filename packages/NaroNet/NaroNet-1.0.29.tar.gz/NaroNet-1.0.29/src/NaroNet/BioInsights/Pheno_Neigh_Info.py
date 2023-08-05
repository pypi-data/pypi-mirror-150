import numpy as np
import os.path as osp
import copy
import os
import matplotlib.pyplot as plt
import cv2
from skimage.morphology import opening, disk
from skimage.measure import perimeter
from matplotlib import cm
from scipy import stats
import seaborn as sns
from torch import clamp_min
from NaroNet.utils.parallel_process import parallel_process
from tifffile.tifffile import imwrite
import pandas as pd
import gc
import itertools
from skimage import filters
import time 
from openTSNE import TSNE
from sklearn.preprocessing import StandardScaler
from torch_geometric.data.makedirs import makedirs


def visualize_tsne_phenotypes(dataset, IndexAndClass,clusters):

    def load_embeddings(patch_dir):
        
        # Initialize features    
        features = []
        features_idx = []

        # Extract patches and save it into a graph
        for subject in IndexAndClass:                                    
            
            # Load image 
            subject_feats = np.load(patch_dir + subject[0] + '.npy')

            # Store feats
            features.append(subject_feats)
            
            # Store subject idx
            features_idx.append([subject[1]]*subject_feats.shape[0])

        # Store in one file all features
        features = np.concatenate(features,axis=0)
        features_idx = np.concatenate(features_idx,axis=0)    
        return features, features_idx
    
    def tsne_with_pheno_thrshold(dataset,features_idx,features,pheno_assignmnents):
        
        # Select number of patches
        num_val =min(10000000,features_idx.shape[0])     
        features_idx = features_idx[::int(features_idx.shape[0]/num_val)]
        features = features[::int(features.shape[0]/num_val),:]
        pheno_assignmnents = pheno_assignmnents[::int(features.shape[0]/num_val),:]
        
        # Reorder samples
        sel_vals = np.random.randint(0,high=features.shape[0],size=features.shape[0])
        features = features[sel_vals,:]
        features_idx = features_idx[sel_vals]
        pheno_assignmnents = pheno_assignmnents[sel_vals,:]
        
        # Normalize features
        scaled_features = StandardScaler().fit_transform(features[:,2:])

        # Create UMAP
        embedding = TSNE(n_jobs=8,random_state=3, verbose=True).fit(scaled_features)

        # Show each phenotype
        for ph in range(pheno_assignmnents.shape[1]):

            # Create and save scatter plot figure
            plt.close('all')
            fig, ax = plt.subplots()   
            scatter = ax.scatter(embedding[:, 0],embedding[:, 1],s=0.5,c=pheno_assignmnents[:,ph],vmin=0,vmax=1,cmap='jet',edgecolors='none')        
            plt.title('TSNE of the dataset Phenoptype - '+str(ph+1), fontsize=24)    
            plt.colorbar(scatter)
            plt.savefig(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/'+'Ph_'+str(ph+1)+'.png',dpi=600)

        pheno_assignmnents_75 = np.zeros(pheno_assignmnents.shape[0])
        for ph in range(pheno_assignmnents.shape[1]):
            thr = np.percentile(pheno_assignmnents[pheno_assignmnents.argmax(1)==ph,ph],90)
            pheno_assignmnents_75[np.logical_and(pheno_assignmnents.argmax(1)==ph,pheno_assignmnents[:,ph]>=thr)] = ph+1
        plt.close('all')
        fig, ax = plt.subplots()   
        scatter = ax.scatter(embedding[:, 0],embedding[:, 1],s=0.5,c=pheno_assignmnents_75,cmap='jet',edgecolors='none')        
        plt.title('TSNE of the dataset ALL_Phenotypes D1', fontsize=24)    
        plt.colorbar(scatter)
        plt.savefig(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/'+'ALL_Phenotypes_D1.png',dpi=600)        


    pat_num = int(len(IndexAndClass)*dataset.args['TSNE_Perc_Pat'])
    IndexAndClass = IndexAndClass[:pat_num]

    # Directory to load
    patch_dir = dataset.root+'Patch_Contrastive_Learning/Image_Patch_Representation/'       

    # Load data
    features, features_idx = load_embeddings(patch_dir)

    # Load pheno assignments
    pheno_assignmnents = []
    for subject_idx, subject_info in enumerate(IndexAndClass):              
        _, cell_type_assignment = load_cell_types_assignments(dataset, 0, subject_info, 0, clusters[0], [])
        pheno_assignmnents.append(cell_type_assignment[:(features_idx==subject_info[1]).sum(),:])
    pheno_assignmnents = np.concatenate(pheno_assignmnents,axis=0)   
        
    # Create Tsne 
    makedirs(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/')
    embedding = tsne_with_pheno_thrshold(dataset,features_idx,features,pheno_assignmnents)


def load_cell_types_assignments(dataset, cell_type_idx, subject_info,subgraph_idx,n_cell_types, prev_cell_type_assignment):
    """
    Obtain matrix that assigns patches to cell types (phenotypes and neighborhoods)
    dataset: (object)
    cell_type_idx: (int) cell_type_idx==0 is phenotype, cell_type_idx==1 is neihborhood, cell_type_idx==2 is neihborhood interaction
    subject_info: (list of str and int)
    subgraph_idx: (int) specifying the index of the subgraph.
    n_cell_types: (int) number of cell types (phenotypes or neighborhoods)
    prev_cell_type_assignment: (array of int) specifying assignments
    """

    # If phenotype or neighborhood load matrix assignment.
    if cell_type_idx<2:
        cell_type_assignment = np.load(osp.join(dataset.processed_dir_cell_types,
                    'cluster_assignmentPerPatch_Index_{}_{}_ClustLvl_{}.npy'.format(subject_info[1], subgraph_idx, n_cell_types)))                        

    # if neighborhood interaction the matrix assigns neighbors to neighborhood interactions.
    else:        
        # Load neighborhood interactions
        secondorder_assignment = np.load(osp.join(dataset.processed_dir_cell_types,
                                'cluster_assignment_Index_{}_ClustLvl_{}.npy'.format(subject_info[1], n_cell_types)))                    
        
        # Obtain assignment of patches to neighborhood interactions
        cell_type_assignment = np.matmul(prev_cell_type_assignment,secondorder_assignment)
    prev_cell_type_assignment = copy.deepcopy(cell_type_assignment)
    
    return prev_cell_type_assignment, cell_type_assignment

def load_patch_image(dataset,imList):
    '''
    Load patch image
    # Create label map. 
    labels = []
    last_patch = 0
    for im_i in imList:
        num_patches = int(im_i.shape[0]/dataset.patch_size)*int(im_i.shape[1]/dataset.patch_size)
        labels.append(np.reshape(np.array(range(last_patch,last_patch+num_patches)),(int(im_i.shape[0]/dataset.patch_size),int(im_i.shape[1]/dataset.patch_size))))
        last_patch = last_patch+num_patches
    labels = np.concatenate(labels,1)
    '''             

    labels = []
    last_patch = 0
    for im_i in imList:
        num_patches = int(im_i.shape[0]/dataset.patch_size)*int(im_i.shape[1]/dataset.patch_size)
        labels.append(np.reshape(np.array(range(last_patch,last_patch+num_patches)),(int(im_i.shape[0]/dataset.patch_size),int(im_i.shape[1]/dataset.patch_size))))
        last_patch = last_patch+num_patches

    return np.concatenate(labels,1), labels

def select_patches_from_cohort_(clusters,dataset,subject_info,count):

    # Crops,Confidence,and Phenotype Vector.
    CropConfPheno = []
    CropConfTissueComm = []
    TissueArea_Conf = []
    for c in range(clusters[0]):
        CropConfPheno.append([])
            
    for c in range(clusters[1]):
        CropConfTissueComm.append([])  
    
    for c in range(clusters[2]):
        TissueArea_Conf.append([]) 

    # Crops,Confidence,and Phenotype Vector.    
    prev_cell_type_assignment=[]
        
    # Apply mask to patch
    for subgraph_idx in range(dataset.findLastIndex(subject_info[1])+1):                
        
        # Open Raw Image.        
        im, imList = dataset.open_Raw_Image(subject_info,1)                

        for cell_type_idx, n_cell_types in enumerate(clusters):    
            # load cell_types_assignments
            prev_cell_type_assignment, cell_type_assignment = load_cell_types_assignments(
                                                                    dataset,cell_type_idx,subject_info,subgraph_idx,
                                                                    n_cell_types,prev_cell_type_assignment)                               
            # Open Single-Cell Contrastive Learning Information
            PCL_reprsntions = np.load(dataset.raw_dir+'/{}.npy'.format(subject_info[0]))                     

            # Phenotypes and neighborhoods, or areas
            if cell_type_idx<2:             
                # Select patches with most confidence
                CropConfPheno,CropConfTissueComm = topk_confident_patches(dataset,n_cell_types,
                                                                            cell_type_assignment,cell_type_idx,CropConfPheno,
                                                                            CropConfTissueComm,im,imList,PCL_reprsntions,count)  
            else:
                # Save subject index and max cell type
                for c_type in range(n_cell_types):
                    TissueArea_Conf[c_type].append(cell_type_assignment[:,c_type])

    del im, imList, PCL_reprsntions
    gc.collect(0)
    gc.collect(1)
    gc.collect(2)
    time.sleep(3)

    return CropConfPheno,CropConfTissueComm,TissueArea_Conf


def select_patches_from_cohort(dataset,IndexAndClass,clusters):
    '''
    '''
     
    # Prepare parallel process
    dict_subjects = []
    for count, subject_info in enumerate(IndexAndClass):
        if subject_info[2][0]!='None':
            dict_subjects.append({'clusters':clusters,'dataset':dataset,'subject_info':subject_info,'count':count})
    
    # select_patches_from_cohort
    result_images = parallel_process(dict_subjects,select_patches_from_cohort_,use_kwargs=True,front_num=1,desc='BioInsights: Get relevant examples of cell types') 

    # Crops,Confidence,and Phenotype Vector.
    CropConfPheno = []
    CropConfTissueComm = []
    TissueArea_Conf = []
    for c in range(clusters[0]):
        CropConfPheno.append([])
            
    for c in range(clusters[1]):
        CropConfTissueComm.append([])  
    
    for c in range(clusters[2]):
        TissueArea_Conf.append([])  

    # Get lists of patches
    for cluster_level in result_images:  
        for clust_idx, cluster in enumerate(cluster_level[0]):
            for patch in cluster:  
                CropConfPheno[clust_idx].append(patch)
        for clust_idx, cluster in enumerate(cluster_level[1]):
            for patch in cluster:  
                CropConfTissueComm[clust_idx].append(patch)
        for r_i, r in enumerate(cluster_level[2]):
            TissueArea_Conf[r_i].append(r)
            
    return CropConfPheno,CropConfTissueComm, TissueArea_Conf

def topk_confident_patches(dataset,n_cell_types,
                            cell_type_assignment,cell_type_idx,CropConfPheno,
                            CropConfTissueComm,im,imList,PCL_reprsntions,count):
    '''
    '''
    K = 25

    # Create label map. 
    labels,labels_list = load_patch_image(dataset,imList)
    # for ll in range(len(labels_list)):
    #     labels_list[ll] = np.transpose(labels_list[ll])
    # labels = np.concatenate(labels_list,axis=1)

            
    for c in range(n_cell_types):
                                                                        
        # Obtain patch info of the K with most certainty
        highest_ent_patches = cell_type_assignment[:PCL_reprsntions.shape[0],c].argsort()[-K:]
        for patch_idx in highest_ent_patches:                  
                    
            # Select the patch from the patch_image            
            mask = labels==patch_idx

            if cell_type_idx==0:
                mx_val = mask.argmax(0).max()*dataset.patch_size
                mxx_val = mask.argmax(1).max()*dataset.patch_size
                CropConfPheno[c].append([im[mx_val:mx_val+dataset.patch_size,mxx_val:mxx_val+dataset.patch_size].copy(), # The original Image
                                            cell_type_assignment[patch_idx,c], # The cell type certainty
                                            [], # The parameters obtained from contrastive learning
                                            [100000*count+patch_idx]]) # Number of the image, and patch identificator
            elif cell_type_idx==1:
                mx_val = mask.argmax(0).max()*dataset.patch_size
                mxx_val = mask.argmax(1).max()*dataset.patch_size
                minIdx = mx_val-dataset.patch_size*2
                maxIdx = mx_val+dataset.patch_size*3
                minIdy = mxx_val-dataset.patch_size*2
                maxIdy = mxx_val+dataset.patch_size*3
                if maxIdx>im.shape[0] or maxIdy>im.shape[1] or minIdx<0 or minIdy<0:
                    continue
                CropConfTissueComm[c].append([im[minIdx:maxIdx,minIdy:maxIdy].copy(), # The original Image
                                            cell_type_assignment[patch_idx,c], # The cell type certainty
                                            [100000*count+patch_idx]]) # Patch identificator 
    
    return CropConfPheno,CropConfTissueComm

def save_2Dmatrix_in_excel_with_names(filename,matrix,Names):
    dict_ = {}
    for n, name in enumerate(Names):
        dict_[name] = matrix[:,n]
    dict_ = pd.DataFrame.from_dict(dict_)      
    dict_.to_excel(filename) 

def save_heatmap_with_names(filename,matrix,Names):   
    import sys
    sys.setrecursionlimit(1000000) 
    if matrix.shape[0]>2:
        plt.close('all')
        plt.figure()
        sns.set(font_scale=1.1)
        scaler = StandardScaler()
        scaler.fit(matrix)        
        h_E_Fig = sns.clustermap(scaler.transform(matrix)*25+128, row_cluster=True, xticklabels=Names, linewidths=0,vmin=-2, vmax=2, cmap="bwr")                
        h_E_Fig.savefig(filename,dpi=600) 

def calculate_pearson_correlation(matrix_0,matrix_1):
    cor_val = stats.spearmanr(matrix_0.flatten(),matrix_1.flatten()).correlation
    cor_val = 0 if np.isnan(cor_val) else cor_val
    return cor_val

def calculate_IoU_usingOtsu(matrix_0,matrix_1):
    # Check if all values are equal and return an IoU of zeros
    if matrix_0.max()==matrix_0.min() or matrix_1.max()==matrix_1.min():
        return 0

    matrix_0 = matrix_0>filters.threshold_otsu(matrix_0)
    matrix_1 = matrix_1>filters.threshold_otsu(matrix_1)        
    intersection = np.logical_and(matrix_0, matrix_1)
    union = np.logical_or(matrix_0, matrix_1)
    return np.sum(intersection) / np.sum(union)    

def calculate_marker_colocalization(matrix,MarkerNames):
    # matrix: contains (number of patches, x_dimension, y_dimension, number of markers)
    Marker_Colocalization =  np.ones((len(MarkerNames),len(MarkerNames)))
    for n_comb, pair_of_markers in enumerate(itertools.combinations(MarkerNames,2)):
        id_0 = MarkerNames.index(pair_of_markers[0])
        id_1 = MarkerNames.index(pair_of_markers[1])
        matrix_0 = matrix[:,:,:,[id_0]]
        matrix_1 = matrix[:,:,:,[id_1]]
        for n_patch in range(matrix.shape[0]):            
            Marker_Colocalization[id_0,id_1] += calculate_pearson_correlation(matrix_0[n_patch,:,:],matrix_1[n_patch,:,:])
        Marker_Colocalization[id_1,id_0] = Marker_Colocalization[id_0,id_1]
    return Marker_Colocalization/matrix.shape[0]

def calculate_Cell_Size_circularity(filename, matrix):
    # matrix: contains (number of patches, x_dimension, y_dimension)         
    # selem = disk(2)
    Size = np.zeros((matrix.shape[3]))
    Eccentricity = np.zeros((matrix.shape[3]))
    for mk in range(matrix.shape[3]):

        # Calculate global threshold
        thr = filters.threshold_otsu(matrix[:,:,:,mk])

        # Initialize count
        count = 0 

        for patch in range(matrix.shape[0]):
            
            if matrix[patch,:,:].sum()>0 and (matrix[patch,:,:].max()-matrix[patch,:,:].min())>0:
                logical = matrix[patch,:,:]>thr
                Size_eccentricity[0] += logical.sum() # Area
                Size_eccentricity[1] += min((4*3.14159*logical.sum())/(perimeter(logical,neighbourhood=4)**2),1) # Eccentricity

                count += 1
        
        Size[mk] /= count
        Eccentricity[mk] /= count

                # if patch<4:
                #     cv2.imwrite(filename+"Patch_"+str(patch)+"_Size_"+str(logical.sum())+"_Ecc_"+str((4*3.14159*logical.sum())/(perimeter(logical,neighbourhood=4)**2))+"_Raw.png", matrix[patch,:,:]/(matrix[patch,:,:].max())*255)
                #     cv2.imwrite(filename+"Patch_"+str(patch)+"_Size_"+str(logical.sum())+"_Ecc_"+str((4*3.14159*logical.sum())/(perimeter(logical,neighbourhood=4)**2))+"_Logical.png", logical*255)
    return Size_eccentricity/matrix.shape[0]

def extract_topk_patches_from_cohort(dataset, CropConf, Marker_Names,cell_type,Thresholds):
    '''
    docstring
    '''

    thisfolder = dataset.bioInsights_dir_cell_types + cell_type+'/'

    if cell_type=='Phenotypes':
        mult_1 = 1 
        mult_2 = 2
    else:
        mult_1 = 5 
        mult_2 = 4

    ## Iterate through Phenotypes to extract topk patches
    k=100
    topkPatches=[]
    # Create a heatmap marker using topk patches
    heatmapMarkerExpression = np.zeros((7,len(CropConf),len(Marker_Names))) # Number of TMEs x number of markers
    heatmap_Colocalization = np.zeros((len(CropConf),len(Marker_Names),len(Marker_Names))) # Number of TMEs x Number of Markers x Number of Markers
    heatmap_CellSize_circularity = np.zeros((len(CropConf),2)) # size and circularity of markers

    # Use CropCOnf, that saves a lot of patches...
    for n_cell_type ,CropConf_i in enumerate(CropConf):
        
        if len(CropConf_i)==0: # Let te heatmap be zero in case no cells were assigned to this TME.
            continue
        
        # Choose patches with most confidence
        topkPheno = np.array([CCP[1] for CCP in CropConf_i]).argsort()[-k:]               
        
        heatmap_Colocalization[n_cell_type,:,:] = calculate_marker_colocalization(np.array([CropConf_i[t][0] for t in topkPheno]),Marker_Names)    
        heatmap_CellSize_circularity[n_cell_type,:] = calculate_Cell_Size_circularity(thisfolder,np.array([CropConf_i[t][0] for t in topkPheno]))

        # Save topkPheno to heatMarkerMap. Mean
        MarkerExpression = np.array([CropConf_i[t][0].mean((0,1)) for t in topkPheno])
        
        # # Save marker expression of patches individually
        # if cell_type=='Phenotypes':        
        #     save_heatmap_with_names(thisfolder+'TME_{}_patchExpression.png'.format(n_cell_type+1),MarkerExpression.mean((1,2)),Marker_Names)            
        # else:
        #     expr = MarkerExpression[:,::int(dataset.patch_size/10),::int(dataset.patch_size/10),:]            
        #     save_heatmap_with_names(thisfolder+'TME_{}_patchExpression.png'.format(n_cell_type+1),np.array([expr[:,:,:,i].flatten() for i in range(expr.shape[3])]).T,Marker_Names)

        # MarkerExpression = np.reshape(MarkerExpression,(MarkerExpression.shape[0]*MarkerExpression.shape[1]*MarkerExpression.shape[2],MarkerExpression.shape[3]))
        heatmapMarkerExpression[0,n_cell_type,:] = np.mean(MarkerExpression,axis=0)                    
        # for n_i, i in enumerate(Thresholds[1:]):
        #     heatmapMarkerExpression[n_i+1,n_cell_type,:] = np.percentile(MarkerExpression,i,axis=0)                    

        # Save Image in RGB
        ImwithKPatches = np.zeros((dataset.patch_size*mult_1*int(np.sqrt(k))+mult_2*int(np.sqrt(k)),dataset.patch_size*mult_1*int(np.sqrt(k))+mult_2*int(np.sqrt(k)),CropConf_i[0][0].shape[2]))
        for t_n, t in enumerate(topkPheno):
            row = np.floor(t_n/int(k**0.5))
            col = np.mod(t_n,int(k**0.5))
       
            # Assign patch to Image
            ImwithKPatches[int(row*mult_1*dataset.patch_size+row*mult_2):int((row+1)*mult_1*dataset.patch_size+row*mult_2),int(col*mult_1*dataset.patch_size+col*mult_2):int((col+1)*mult_1*dataset.patch_size+col*mult_2),:] = CropConf_i[t][0]
        
        if len(Marker_Names)<10:
            # Fill unassigned patches with zeroes.
            for t_n in range(len(topkPheno),k):
                row = np.floor(t_n/int(k**0.5))
                col = np.mod(t_n,int(k**0.5))
                # Assign patch to Image
                ImwithKPatches[int(row*mult_1*dataset.patch_size+row*mult_2):int((row+1)*mult_1*dataset.patch_size+row*mult_2),int(col*mult_1*dataset.patch_size+col*mult_2):int((col+1)*mult_1*dataset.patch_size+col*mult_2),:] = 0.0
                            
            # RGBImwithKPatches = dataset.nPlex2RGB(ImwithKPatches)
            imwrite(thisfolder+'Cell_type_{}_Raw.tiff'.format(n_cell_type+1),np.moveaxis(ImwithKPatches,2,0), photometric='minisblack')
            
            # Save Certainty of this Phenotype
            plt.close('all')
            plt.figure()
            n, bins, patches = plt.hist(np.array([i[1] for i in CropConf_i]), 100, color=cm.jet_r(int(n_cell_type*(255/int(len(CropConf))))), alpha=1)            
            plt.ylabel('Number of Patches',fontsize=16)            
            plt.xlabel('Level of TME certainty',fontsize=16)
            plt.title('Histogram of TME ' + str(n_cell_type+1) + ' certainty',fontsize=16)
            plt.savefig(thisfolder+'ConfidenceHistogram_{}.png'.format(n_cell_type+1), format="PNG",dpi=600)                                         

        # Assign topkPheno Patches
        topkPatches+=[CropConf_i[t] for t in topkPheno]     

    return heatmapMarkerExpression, heatmap_Colocalization, heatmap_CellSize_circularity

def save_heatmap_raw_and_normalized(filename, heatmap, TME_names,Colormap,Marker_Names):    
    y_ticklabels = TME_names[heatmap.sum(1)!=0]
    c_map = Colormap[:heatmap.shape[0]][heatmap.sum(1)!=0]
    # Figure Heatmap Raw Values
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    cluster=True if (heatmap.sum(1)!=0).sum()>1 else False
    h_E_Fig = sns.clustermap(heatmap[heatmap.sum(1)!=0,:],col_cluster=cluster, row_cluster=cluster, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(filename+'_Raw.png',dpi=600) 

    # Figure Heatmap Min is 0 and max is 1 Values    
    h_E_COL_MinMax = heatmap[heatmap.sum(1)!=0,:] - heatmap[heatmap.sum(1)!=0,:].min(0,keepdims=True)
    h_E_COL_MinMax = h_E_COL_MinMax/h_E_COL_MinMax.max(0,keepdims=True)
    h_E_COL_MinMax[np.isnan(h_E_COL_MinMax)] = 0 
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    if (h_E_COL_MinMax.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_MinMax[h_E_COL_MinMax.sum(1)!=0,:],col_cluster=False, 
            row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_MinMax.png',dpi=600) 
    elif (h_E_COL_MinMax.sum(1)!=0).sum()>1: # Normal heatmap.    
        h_E_Fig = sns.clustermap(h_E_COL_MinMax[h_E_COL_MinMax.sum(1)!=0,:],col_cluster=True, 
            row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_MinMax.png',dpi=600)  
    
    # Figure Heatmap z-scored values
    h_E_COL_Norm = stats.zscore(heatmap[heatmap.sum(1)!=0,:],axis=0)  
    h_E_COL_Norm[np.isnan(h_E_COL_Norm)] = 0              
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)    
    if (h_E_COL_Norm.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=False, vmin=-2, vmax=2, row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm.png',dpi=600) 
    elif (h_E_COL_Norm.sum(1)!=0).sum()>1: # Normal heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=True, vmin=-2, vmax=2, row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm.png',dpi=600) 

    # Figure Heatmap z-scored values
    h_E_COL_Norm = stats.zscore(h_E_COL_Norm[heatmap.sum(1)!=0,:],axis=1)  
    h_E_COL_Norm[np.isnan(h_E_COL_Norm)] = 0              
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)    
    if (h_E_COL_Norm.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=False, vmin=-2, vmax=2, row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm_rows.png',dpi=600) 
    elif (h_E_COL_Norm.sum(1)!=0).sum()>1: # Normal heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=True, vmin=-2, vmax=2, row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm_rows.png',dpi=600) 

def save_heatMapMarker_and_barplot(dataset, heatmapMarkerExpression, heatmapMarkerColocalization, heatmap_CellSize_circularity, CropConf,Marker_Names,cell_type,Thresholds):
    '''
    '''
    if cell_type=='Phenotypes':
        abrev = 'P'
    else:
        abrev = 'N'

    Colormap=cm.jet(range(0,255,int(255/heatmapMarkerExpression.shape[1])))[:,:3]

    # Save heatmapmarker to disk
    for n_j, j in enumerate(Thresholds):
        save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/heatmap_MarkerExpression_'+str(j), 
                                        heatmapMarkerExpression[n_j,:,:], np.array([abrev+str(i+1) for i in range(len(CropConf))]),
                                        Colormap,Marker_Names)
        # save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/heatmap_MarkerExpression_Colocalization_'+str(j), 
        #                                 np.concatenate((heatmapMarkerExpression[n_j,:,:],heatmapMarkerColocalization),axis=1), np.array([abrev+str(i+1) for i in range(len(CropConf))]),
        #                                 Colormap,Marker_Names+['_'.join(i) for i in itertools.combinations(Marker_Names,2)])
        

    # try:
    #     save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types + cell_type + '/heatmap_Size_Circularity', heatmap_CellSize_circularity, np.array([abrev+str(i+1) for i in range(len(CropConf))]),Colormap,['Nucleus Size', 'Nucleus circularity'])
    # except:
    #     print('')
    # save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types + cell_type + '/heatmap_Colocalization', heatmapMarkerColocalization, np.array([abrev+str(i+1) for i in range(len(CropConf))]),Colormap,['_'.join(i) for i in itertools.combinations(Marker_Names,2)])

    # Calculate Phenotype abundance across all patients
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.0)
    BarPlotPresenceOfPhenotypes = sns.barplot(x=[abrev+str(i+1) for i in range(len(CropConf))] ,y=np.array([len(i) for i in CropConf]),palette=Colormap)      
    BarPlotPresenceOfPhenotypes.set(xlabel=cell_type, ylabel = 'Number of patches',title='Histogram of abundance across the patient cohort')                
    BarPlotPresenceOfPhenotypes.set_xticklabels([abrev+str(i+1) for i in range(len(CropConf))], size=7)
    plt.savefig(dataset.bioInsights_dir_cell_types + cell_type +'/Barplot_cell_types.png',dpi=600)

def neigh_comp(TC,phenoInd):
    InteractivityVect = np.zeros(len(phenoInd))
    for n_Phen, PH in enumerate(phenoInd):
        PH = [p[0] for p in PH]
        if len(PH)>0:
            for t in TC:
                if t[2] in PH:
                    InteractivityVect[n_Phen]+=1     
    return InteractivityVect

def obtain_neighborhood_composition(dataset,CropConfPheno,CropConfTissueComm):
    '''
    '''

    # Find indices of phenotypes
    phenoInd = []
    for c in CropConfPheno:
        # Find all indices
        phenoInd.append([c_n[3] for c_n in c])        

    # Generate Interactivity matrix
    dict_neigh = []
    for n_Neighbor, TC in enumerate(CropConfTissueComm):
        dict_neigh.append({'TC':TC,'phenoInd':phenoInd})
    result = parallel_process(dict_neigh,neigh_comp,use_kwargs=True,front_num=1,desc='BioInsights: Calculate phenotype abundance whithin neighborhoods') 
    InteractivityMatrix = np.stack(result)

    # Input
    Colormap_Pheno=cm.jet_r(range(0,255,int(255/len(CropConfPheno))))[:,:3]
    Colormap_Neigh=cm.jet_r(range(0,255,int(255/len(CropConfTissueComm))))[:,:3]

    # Save interactivity matrix
    sns.set(font_scale=1.5)
    plt.close('all')
    heatmapInteractivityMatrix_Fig = sns.clustermap(InteractivityMatrix,col_cluster=False, row_cluster=False, row_colors=Colormap_Neigh, col_colors=Colormap_Pheno,xticklabels=['P'+str(i+1) for i in range(len(CropConfPheno))],yticklabels=['N'+str(i+1) for i in range(len(CropConfTissueComm))], linewidths=0.5, cmap="bwr")            
    plt.xlabel("Phenotypes")
    plt.ylabel("Neighborhoods")
    heatmapInteractivityMatrix_Fig.savefig(dataset.bioInsights_dir_cell_types+'Neighborhoods/heatmap_InteractivityMat_Raw.png',dpi=600) 
    plt.close('all')
    InteractivityMatrix[InteractivityMatrix==0]=1e-3
    heatmapInteractivityMatrix_Fig = sns.clustermap(stats.zscore(InteractivityMatrix,axis=1),col_cluster=False, row_cluster=False, row_colors=Colormap_Neigh, col_colors=Colormap_Pheno,xticklabels=['P'+str(i+1) for i in range(len(CropConfPheno))],yticklabels=['N'+str(i+1) for i in range(len(CropConfTissueComm))], linewidths=0.5, cmap="bwr")            
    plt.xlabel("Phenotypes")
    plt.ylabel("Neighborhoods")
    heatmapInteractivityMatrix_Fig.savefig(dataset.bioInsights_dir_cell_types+'Neighborhoods/heatmap_InteractivityMat_Norm.png',dpi=600) 

def Area_to_Neighborhood_to_Phenotype(dataset,clusters,IndexAndClass, ClusteringThreshold):
    
    # Initialize variables
    neigh_to_area = []
    patch_to_pheno = []
    patch_to_neigh = []

    # Obtain clusters per Slide
    for count, idxclster in enumerate(IndexAndClass):           
        try:

            # Load assignment
            neigh_to_area_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignment_Index_{}_ClustLvl_{}.npy'.format(idxclster[1], clusters[-1])))                
            patch_to_neigh_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignmentPerPatch_Index_{}_0_ClustLvl_{}.npy'.format(idxclster[1], clusters[-2])))        
            patch_to_pheno_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignmentPerPatch_Index_{}_0_ClustLvl_{}.npy'.format(idxclster[1], clusters[-3])))                             
            data = dataset.get(idxclster[1],0)

            # Save assignments
            neigh_to_area.append(neigh_to_area_assignment)
            patch_to_neigh.append(patch_to_neigh_assignment[:data.num_nodes,:])            
            patch_to_pheno.append(patch_to_pheno_assignment[:data.num_nodes,:])                        
        except:
            continue

    # Calculate Neighborhoods to areas
    neigh_to_area = np.stack(neigh_to_area) # pat x neigh x areas
    PercTHrsl_area = np.percentile(neigh_to_area,axis=(0,1),q=ClusteringThreshold)
    Area_to_Neigh = np.zeros((clusters[-1],clusters[-2])) 
    for area in range(clusters[-1]):
        Area_to_Neigh[area,:] = np.sum(neigh_to_area[:,:,area]*np.array(neigh_to_area[:,:,area]>PercTHrsl_area[area]),0)

    # Save Neighborhoods to areas heatmap
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    row_colors_Area=cm.jet_r(range(0,255,int(255/clusters[2])))[:,:3]
    yticklabels_Area = ['A'+str(i+1) for i in range(clusters[2])]
    col_colors_Neigh=cm.jet_r(range(0,255,int(255/clusters[1])))[:,:3]
    xticklabels_Neigh = ['N'+str(i+1) for i in range(clusters[1])]
    Area_to_Neigh = Area_to_Neigh/Area_to_Neigh.sum(1,keepdims=True)*100    
    Area_to_Neigh[np.isnan(Area_to_Neigh)] = 0
    h_E_Fig = sns.clustermap(Area_to_Neigh.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Area,
                                row_colors=col_colors_Neigh,yticklabels=xticklabels_Neigh,xticklabels=yticklabels_Area, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Perc_'+str(ClusteringThreshold)+'.png',dpi=600) 
    plt.close('all')
    plt.figure()
    h_E_Fig = sns.clustermap(Area_to_Neigh.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Area, z_score=1,
                                row_colors=col_colors_Neigh,yticklabels=xticklabels_Neigh,xticklabels=yticklabels_Area, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Zscore_'+str(ClusteringThreshold)+'.png',dpi=600) 
    df = pd.DataFrame(Area_to_Neigh.transpose(), columns = yticklabels_Area)
    df.index = xticklabels_Neigh
    df.to_excel(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Zscore_'+str(ClusteringThreshold)+'.xlsx')  

    # Phenotypes to neighborhoods
    patch_to_neigh = np.concatenate(patch_to_neigh,0) # patches x neigh
    patch_to_pheno = np.concatenate(patch_to_pheno,0) # patches x pheno    
    PercTHrsl_neigh = np.percentile(patch_to_neigh_assignment,axis=0,q=ClusteringThreshold)
    PercTHrsl_pheno = np.percentile(patch_to_pheno,axis=0,q=ClusteringThreshold)        
    for i in range(patch_to_neigh.shape[1]):
        patch_to_neigh[:,i][PercTHrsl_neigh[i]>=patch_to_neigh[:,i]] = 0 
    for i in range(patch_to_pheno.shape[1]):
        patch_to_pheno[:,i][PercTHrsl_pheno[i]>=patch_to_pheno[:,i]] = 0        
    Neigh_to_Pheno = np.matmul(np.transpose(patch_to_neigh),patch_to_pheno)

    # Save heatmap Neigh_to_Pheno
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    row_colors_Neigh=cm.jet_r(range(0,255,int(255/clusters[1])))[:,:3]
    yticklabels_Neigh = ['N'+str(i+1) for i in range(clusters[1])]
    col_colors_Pheno=cm.jet_r(range(0,255,int(255/clusters[0])))[:,:3]
    xticklabels_Pheno = ['P'+str(i+1) for i in range(clusters[0])]
    Neigh_to_Pheno = Neigh_to_Pheno/Neigh_to_Pheno.sum(1,keepdims=True)*100
    Neigh_to_Pheno[np.isnan(Neigh_to_Pheno)] = 0
    h_E_Fig = sns.clustermap(Neigh_to_Pheno.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Neigh,
                                row_colors=col_colors_Pheno,yticklabels=xticklabels_Pheno,xticklabels=yticklabels_Neigh, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Perc_Thrs{}.png'.format(str(ClusteringThreshold)),dpi=600) 
    plt.close('all')
    plt.figure()
    Neigh_to_Pheno[Neigh_to_Pheno==0] = 1e-16
    h_E_Fig = sns.clustermap(Neigh_to_Pheno.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Neigh, z_score=1,
                                row_colors=col_colors_Pheno,yticklabels=xticklabels_Pheno,xticklabels=yticklabels_Neigh, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Zscore_Thrs{}.png'.format(str(ClusteringThreshold)),dpi=600) 
    df = pd.DataFrame(Neigh_to_Pheno.transpose(), columns = yticklabels_Neigh)
    df.index = xticklabels_Pheno
    df.to_excel(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Perc_Thrs{}.xlsx'.format(str(ClusteringThreshold)))  


    
