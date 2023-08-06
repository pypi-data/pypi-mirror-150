# uniPort


adata = up.Run(adatas=None, adata_cm=None, mode='h', lambda_s=0.5, labmda_recon=1.0, lambda_kl=0.5, lambda_ot=1.0, reg=0.1, reg_m=1.0, batch_size=256, lr=2e-4, max_iteration=30000, seed=124, gpu=0, Prior=None, label_weight=None, ref_id=None, save_OT=False, use_specific=True, loss_type='BCE', outdir='output/', out='latent', input_id=0, pred_id=1, source_name='source', rep_celltype='cell_type', batch_key='domain_id', enc=None, dec=None, umap=False, verbose=False, assess=False, show=False)

<font color='Dodgerblue'>**Key parameters includes:**</font>

+ **adatas**: List of AnnData matrices for each dataset.
+ **adata_cm**: AnnData matrix containing common genes from different datasets.
+ **mode**: Choose from ['h', 'v', 'd'] If 'mode=h', integrate data with common genes (Horizontal integration). If 'mode=v', integrate data profiled from the same cells (Vertical integration). If 'mode=d', inetrgate data without common genes (Diagonal integration). Default: 'h'.
+ **lambda_s**: balanced parameter for common and specific genes. Default: 0.5
+ **lambda_recon**: balanced parameter for reconstruct term. Default: 1.0
+ **lambda_kl**: balanced parameter for KL divergence. Default: 0.5
+ **lambda_ot**: balanced parameter for OT. Default: 1.0
+ **max_iteration**: max iterations for training. Training one batch_size samples is one iteration. Default: 30000
+ **ref_id**: id of reference dataset. Default: The domain_id of last dataset
+ **save_OT**: if True, output a global OT plan. Need more memory. Default: False
+ **out**: output of uniPort. Choose from ['latent', 'project', 'predict']. If out=='latent', train the network and output cell embeddings. If out=='project', project data into the latent space and output cell embeddings. If out=='predict', project data into the latent space and output cell embeddings through a specified decoder. Default: 'latent'



<font color='Dodgerblue'>**Other parameters include:**</font>

+ **label_weight**: prior-guided weighted vectors. Default: None
+ **reg**: entropy regularization parameter in OT. Default: 0.1
+ **reg_m**: unbalanced OT parameter. Larger values means more balanced OT. Default: 1.0
+ **batch_size**: number of samples per batch to load. Default: 256
+ **lr**: learning rate. Default: 2e-4
+ **enc**: structure of encoder. For example: enc=[['fc', '1024', 1, 'relu'], ['fc', 16, '', '']] means that the encoder contains two layers. The first layer is fully connected with 1024 neurons, a [DSBN](https://openaccess.thecvf.com/content_CVPR_2019/papers/Chang_Domain-Specific_Batch_Normalization_for_Unsupervised_Domain_Adaptation_CVPR_2019_paper.pdf) and activative function `relu`. The second layer is fully connected with 16 neurons without DSBN or activative function.
+ **gpu**: index of GPU to use if GPU is available. Default: 0
+ **Prior**: prior correspondence matrix. Default: None
+ **loss_type**: type of loss function. Choose from ['BCE', 'MSE', 'L1']. Default: 'BCE'
+ **outdir**: output directory. Default: 'output/'
+ **input_id**: only used when mode=='d' and out=='predict' to choose a encoder to project data. Default: 0
+ **pred_id**: only used when out=='predict' to choose a decoder to predict data. Default: 1
+ **seed**: random seed for torch and numpy. Default: 124
+ **batch_key**: name of batch in AnnData. Default: domain_id
+ **source_name**: name of source in AnnData. Default: source
+ **rep_celltype**: names of cell-type annotation in AnnData. Default: 'cell_type'
+ **umap**: if True, perform UMAP for visualization. Default: False
+ **assess**: if True, calculate the entropy_batch_mixing score and silhouette score to evaluate integration results. Default: False
+ **show**: if True, show the UMAP visualization of latent space. Default: False