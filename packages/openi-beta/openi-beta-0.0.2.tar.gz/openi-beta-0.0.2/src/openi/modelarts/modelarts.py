import emoji

def env_check():
    try:
        import moxing as mox
    except:
        print(f'{emoji.emojize(":cross_mark:")} enviornment check failed: 请在启智平台NPU集群上运行该代码')

def openi_dataset_to_Env(data_url, data_dir):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} pass Modelarts check')
        from .helper import openi_dataset_to_Env
        openi_dataset_to_Env(data_url, data_dir)

def openi_multidataset_to_env(multi_data_url, data_dir):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        openi_multidataset_to_env(multi_data_url, data_dir)

def pretrain_to_env(pretrain_url, pretrain_dir):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        pretrain_to_env(pretrain_url, pretrain_dir)

def env_to_openi(train_dir, train_url):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        env_to_openi(train_dir, train_url)

def obs_copy_file(obs_file_url, file_url):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        obs_copy_file(obs_file_url, file_url)
    
def obs_copy_folder(folder_dir, obs_folder_url):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        obs_copy_folder(folder_dir, obs_folder_url)

def c2net_multidataset_to_env(multi_data_url, data_dir):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        c2net_multidataset_to_env(multi_data_url, data_dir)

def EnvToOpenIEpochEnd(train_dir, obs_train_url):
    if env_check():
        print(f'{emoji.emojize(":circle_mark:")} Modelarts check')
        from .helper import openi_dataset_to_Env
        EnvToOpenIEpochEnd(train_dir, obs_train_url)