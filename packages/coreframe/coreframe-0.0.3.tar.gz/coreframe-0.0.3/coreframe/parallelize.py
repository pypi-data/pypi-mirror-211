import numpy as np
import multiprocessing as mp
from .config import config
from math import ceil

def create_shared_array(shape, dtype=np.float64):
    size = int(np.prod(shape))
    ctype = np.ctypeslib.as_ctypes_type(dtype)
    shared_array = mp.Array(ctype, size)
    np_array = np.frombuffer(shared_array.get_obj(), dtype=ctype).reshape(shape)
    return shared_array, np_array


def find_input_chunk_starts(cf, dtimes, itert_delta, updated_n_workers):

    start_date = dtimes[0]
    length = cf.shape[0]

    # TODO this algorithm doesn't work if the edge of the chunk is not divisible by itert_delta
    # find indices of chunks attributed to each process
    n_workers_indices = [0]
    for i in range(1, updated_n_workers):
        index = i * length // updated_n_workers
        delta = dtimes[index] - start_date 
        coeff = delta % itert_delta / itert_delta
        if ( coeff == 0):
            n_workers_indices.append(index)
        elif (coeff >= 0.5):
            while coeff != 0:
                index += 1
                delta = dtimes[index] - start_date
                coeff = delta % itert_delta / itert_delta
            n_workers_indices.append(index)
        else:
            while coeff != 0:
                index -= 1
                delta = dtimes[index] - start_date
                coeff = delta % itert_delta / itert_delta
            n_workers_indices.append(index)

    return n_workers_indices


# TODO: implement modes like "itert", "window"
def parallelize(rows_per_itert = 1):
    '''
    rows_per_itert = integer
    '''
    
    def extract_attributes(kwargs):
        options = kwargs.get("options") 
        if options is not None:
            del kwargs["options"]

            updated_rows_per_itert = options.get("rows_per_itert") or rows_per_itert
        
            return updated_rows_per_itert
        
        return rows_per_itert

    def decorator(func):

        # need because of pickling in multiprocessing
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        def wrapper(*args, **kwargs):

            if config["parallel"] is not True:
                return func(*args, **kwargs)
            
            n_workers = config['n_workers']
            
            # get the values needed for parallelization and remove them from kwargs
            rows_per_itert= extract_attributes(kwargs)

            # get itert from kwargs and args
            itert = kwargs.get("itert") 
            if itert is None: itert = args[func.__code__.co_varnames.index("itert")]
            
            # get the original CoreFrame
            cf = args[0]
            args = args[1:]

            num, t_type = int(itert[0:-1]), itert[-1]
            itert_delta = np.timedelta64(num, t_type)
            dtimes = cf.dtimes.astype(f"datetime64[{t_type}]")

            # find the n_workers_indices
            input_chunk_starts = find_input_chunk_starts(cf, dtimes, itert_delta, n_workers)

            # calculate output indices
            output_chunk_starts = [ 0 for _ in input_chunk_starts]

            shape = list(cf.shape)
            shape[0] = ceil( rows_per_itert*(dtimes[-1] - dtimes[0] +  np.timedelta64(1, t_type))/itert_delta)
            shape = tuple(shape)
            for i, _ in enumerate(output_chunk_starts):
                output_chunk_starts[i] = rows_per_itert * input_chunk_starts[i] * int(np.prod(shape) / shape[0] / num )
                
            # create shared memory array
            shared_array, np_array = create_shared_array(shape)

            # make a CoreFrame view of np array
            cf_array = np_array.view(cf.__class__)

            with mp.Manager() as manager:
                dtimes_list = manager.list([None] * n_workers)
                cf_array.dtimes = cf.dtimes

                # TODO: in the future when new attributes will appear make a list of attribute names and make a function that just applies them because they are unchanged

                # assign tasks
                processes = []
                for i in range(n_workers):
                    chunk_end = input_chunk_starts[i+1] if i != (n_workers-1) else None
                    fun_args = (cf[input_chunk_starts[i]: chunk_end], *args, shared_array, output_chunk_starts[i], dtimes_list, i)
                    p = mp.Process(target=call_func, args = fun_args, kwargs=kwargs)
                    p.start()
                    processes.append(p)

                # collect tasks
                for p in processes:
                    p.join()

                dtimes_list = list(dtimes_list)
                res_dtimes_list = []
                for val in dtimes_list:
                    res_dtimes_list.extend(val)
                
                # TODO: modify dtimes_list with the rows_per_itert
            cf_array.dtimes = res_dtimes_list
            
            return cf_array
        return wrapper
    
    return decorator