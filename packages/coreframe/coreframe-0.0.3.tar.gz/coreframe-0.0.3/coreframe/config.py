import multiprocessing as mp

config = {
    "parallel": False,
    "n_workers": mp.cpu_count()
}

def set_config(**kwargs):
    global config
    config.update(kwargs)