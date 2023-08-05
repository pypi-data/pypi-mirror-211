import numpy as np
import warnings
from .parallelize import parallelize
import inspect


class CoreFrame(np.ndarray):
    '''
    CoreFrame is a subclass of numpy ndarray that adds time-based indexing and some operations.

    Parameters:
        input_array (array_like): Array-like input data.
        dtimes (array_like): Datetime values for the time-axis.

    Attributes:
        dtimes (ndarray): Datetime values for the time-axis.

    Methods:
    --------
    iter_by_time(self, interval):
        Returns an iterator that yields data points at specified time interval.
        
    between(self, start_time, end_time):
        Returns a new TimeSeries object that contains only data points between start_time and end_time.
        
    meanby(self, interval):
        Returns a new TimeSeries object with mean values computed over specified time intervals.
        
    apply_by_generator(self, generator_func):
        Returns a new TimeSeries object with data points computed by the given generator function.
        
    split(self, num_parts):
        Splits the time series into the specified number of parts and returns a list of TimeSeries objects.
    '''

    def __new__(cls, input_array, dtimes):
        '''
        Returns a new CoreFrame object.

        Parameters:
            input_array (array-like): Input data.
            dtimes (array-like): Array of datetime values.

        Returns:
            obj (CoreFrame): A new CoreFrame object.
        '''
        # TODO: create own indexing for columns
        obj = np.asarray(input_array).view(cls)

        # dtimes must be ndarray to use .astype()
        # converting to ndarray later leads to duplication of dtimes
        obj.dtimes = np.asarray(dtimes) 

        # obj.Y = np.linspace(Y[0], Y[1], num = obj.shape[yaxis]) if Y is not None else None
        # obj.yaxis = yaxis

        # obj.X = np.linspace(X[0], X[1], num = obj.shape[xaxis]) if X is not None else None
        # obj.xaxis = xaxis

        # obj.Z = np.linspace(Z[0], Z[1], num = obj.shape[zaxis]) if Z is not None else None
        # obj.zaxis = zaxis

        # handle obj.dtimes.shape = ()
        if obj.dtimes.shape == (): obj.dtimes = np.expand_dims(obj.dtimes, 0)

        # length of dtimes must correspond to the length along the 0 axis
        assert obj.shape[0] == obj.dtimes.shape[0], f"obj.shape={obj.shape}, but {obj.shape[0]} != {obj.dtimes.shape[0]}"

        return obj


    def _handle_one_dim_getitem(self, key):
        '''
        Handles one-dimensional indexing and slicing for CoreFrame object.

        Parameters:
            key (int, slice): Index or slice.

        Returns:
            result (CoreFrame or ndarray): Result of indexing or slicing.
        '''
        result = super().__getitem__(key)

        if isinstance(result, CoreFrame):
            # select correct dtime
            result.dtimes = result.dtimes[key]
                
        return result
    
    def _handle_multi_dim_getitem(self, key):
        '''
        Handles multi-dimensional indexing and slicing for CoreFrame object.

        Parameters:
            key (tuple): Index or slice.

        Returns:
            result (CoreFrame or ndarray): Result of indexing or slicing.
        '''
        result = super().__getitem__(key)
        
        # select correct dtime
        if isinstance(result, CoreFrame):
            result.dtimes = result.dtimes[key[0]]

        return result
    
    def _handle_time_based_getitem(self, key):
        key = np.datetime64(key)
        # Find the index of the corresponding datetime object
        index = int(np.where(self.dtimes == key)[0][0])
        tup = tuple([slice(None, None, None) if i != 0 else index for i in range(self.ndim)])
        return self[tup]

    def __getitem__(self, key):
        '''
        Returns selected elements from CoreFrame object.

        Parameters:
            key (int, slice, tuple): Index or slice.

        Returns:
            result (CoreFrame or ndarray): Result of indexing or slicing.
        '''
        
        # handling one-dimensional indexing and slicing
        if isinstance(key, int) or isinstance(key, slice):
            return self._handle_one_dim_getitem(key)

        # handling multi-dimensional slicing
        if isinstance(key, tuple) and (isinstance(key[0], slice) or isinstance(key[0], int)):
            return self._handle_multi_dim_getitem(key)
        
        # handling time-based indexing
        if isinstance(key, str):
            return self._handle_time_based_getitem(key)

            
        raise IndexError(f"Inappropriate index: {key}")
    
    # def get_at_XYZ(self,  X=None,  Y=None,Z=None):
    #     def _get_slice(self, letter, coord):
    #         letter_to_self_coord = {
    #             "X": self.X,
    #             "Y": self.Y,
    #             "Z": self.Z
    #         }

    #         if isinstance(coord, tuple):
    #             coord_slice = slice(np.argmin(np.abs(letter_to_self_coord[letter] - coord[0])), np.argmin(np.abs(letter_to_self_coord[letter] - coord[1])), None)
    #         elif isinstance(coord, int):
    #             coord_slice = np.argmin(np.abs(letter_to_self_coord[letter] - coord))
    #         elif coord is None:
    #             coord_slice = slice(None, None, None)

    #         return coord_slice
        
    #     X_slice = _get_slice(self, "X", X)
    #     Y_slice = _get_slice(self, "Y", Y)
    #     Z_slice = _get_slice(self, "Z", Z)

    #     axis_to_slice = {
    #         self.xaxis: X_slice,
    #         self.yaxis: Y_slice,
    #         self.zaxis: Z_slice
    #     }

    #     slicing = [axis_to_slice[i] if i in axis_to_slice else slice(None, None, None) for i in range(self.ndim)]
    #     slicing = tuple(slicing)
    #     print(slicing)

    #     return self[slicing]

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):

        '''
        Applies a universal function to the CoreFrame object.

        Parameters:
            ufunc (callable): The universal function to apply.
            method (str): The method to apply.
            inputs (tuple): Input arguments for the function.
            kwargs (dict): Additional keyword arguments.

        Returns:
            result (CoreFrame or ndarray): Result of the ufunc application.
        '''
        # saving col_names and dtimes that will be used in reduced CoreFrame
        dtimes = None
        # creating an array of ndarrrays of inputs
        new_inputs = []
        for input in inputs:
            if isinstance(input, CoreFrame):
                new_inputs.append(input.__array__())
                dtimes = input.dtimes
            else:
                new_inputs.append(input)

        # if the "out" argument is given, then convert it to ndarray
        if isinstance(kwargs.get('out'), tuple):
            if len(kwargs['out']) > 1: raise Exception
            if isinstance(kwargs['out'][0], CoreFrame):
                kwargs['out'] = kwargs['out'][0].__array__()

        result = super().__array_ufunc__(ufunc, method, *new_inputs, **kwargs)
        result = result.view(CoreFrame)
        if isinstance(result, CoreFrame):
            result.dtimes = dtimes

        if method == 'reduce' and isinstance(result, CoreFrame):
            # TODO: should check which axis of application

            # if the method reduces the dimensions, then dtimes will be an average
            st_date = inputs[0].dtimes[0]
            nd_date  = inputs[0].dtimes[-1]
            result.dtimes = st_date + (nd_date-st_date)//2

        return result

    def __array_finalize__(self, obj):
        '''
        Finalizes the CoreFrame object after slicing.

        Parameters:
            obj (object): The original object.

        Returns:
            None
        '''
        # obj is the original object and self is the slice
        if obj is None: return
        
        self.dtimes = getattr(obj, 'dtimes', None)

    def __array_function__(self, func, types, args, kwargs):
        # custom implementation of concatenate
        if func is np.concatenate:

            dtimes =  None

            # convert all CoreFrames to ndarrays for concatenation
            new_input = []
            for input in args[0]:
                if isinstance(input, CoreFrame):
                    new_input.append(input.__array__())

                    # handle dtimes
                    if (dtimes is None):
                        dtimes = input.dtimes
                    else:
                        dtimes = np.concatenate((np.atleast_1d(dtimes), np.atleast_1d(input.dtimes)))
                else:
                    new_input.append(input)

            result = np.concatenate(new_input, *args[1:], **kwargs)
            result = result.view(CoreFrame)

            if isinstance(result, CoreFrame):
                result.dtimes = dtimes
            return result

        return super().__array_function__(func, types, args, kwargs)

    def iter_by_time(self, itert):
        '''
        Returns an iterator that iterates through CoreFrame object by time intervals.

        Parameters:
            itert (str): Time interval to iterate by (e.g. '3D' for 3 days).

        Yields:
            element (CoreFrame or ndarray): Selected element from CoreFrame object.
        '''
        num, t_type = int(itert[0:-1]), itert[-1]
        delta = np.timedelta64(num, t_type)
        dtimes = self.dtimes.astype(f"datetime64[{t_type}]")

        current_date = dtimes[0]
        yield self[0]
        for i in range(1, len(self.dtimes)):
            if dtimes[i] - current_date >= delta:
                # yield by each itert
                current_date = dtimes[i]
                yield self[i]

    def __repr__(self):
        '''
        Returns a string representation of the CoreFrame object.

        Returns:
            str: A string representation of the CoreFrame object.
        '''
        return f"\
<coreframe.CoreFrame>\n\
shape:      {self.shape}\n\
dtimes:     {self.dtimes} \n\
data:\n{np.ndarray.__str__(self)}"

    def __str__(self):
        '''
        Returns a string representation of the CoreFrame object.

        Returns:
            str: A string representation of the CoreFrame object.
        '''
        return self.__repr__()

    def between(self, sdtime, edtime):
        '''
        Returns a subset of CoreFrame between 2 datetime constraints.

            Parameters:
                sdtime (datetime): Start date
                edtime (datetime): End date

            Returns:
                sub_cf (CoreFrame): A CoreFrame between start and end times
        '''
        sdtime = np.datetime64(sdtime)
        edtime = np.datetime64(edtime)

        start, end = np.searchsorted(self.dtimes, [sdtime, edtime])
        sub_cf = self[start:end]
        return sub_cf


    def meanby(self, itert):
        '''
        Returns a CoreFrame with the time-series average of the original.

            Parameters:
                itert (char): one of 'Y', 'M', 'W', 'D', 'h', 'm', 's', 'ms'

            Returns:
                CoreFrame with the time-series average of the original.
        '''
        num, t_type = int(itert[0:-1]), itert[-1]
        delta = np.timedelta64(num, t_type)
        dtimes = self.dtimes.astype(f"datetime64[{t_type}]")

        indices = []
        curr = dtimes[0]
        new_dtimes = [dtimes[0]]
        for i, val in enumerate(dtimes):
            if val - curr >= delta:
                curr = val
                indices.append(i)
                new_dtimes.append(curr)
        to_compute = np.split(np.array(self), indices)
        
        for i, _ in enumerate(to_compute):
            to_compute[i] = np.mean(to_compute[i], axis=0)

        return CoreFrame(np.array(to_compute), new_dtimes)

    @parallelize()
    def apply_window():
        return

    @parallelize()
    def apply_by(self, itert, fun, out=None, out_chunk_start = None, out_dtimes_list = None, out_dtimes_idx = None, *args, **kwargs):
        num, t_type = int(itert[0:-1]), itert[-1]

        delta = np.timedelta64(num, t_type)
        dtimes = self.dtimes.astype(f"datetime64[{t_type}]")

        list_of_results = []
        current_date = dtimes[0]
        st_group_index = 0

        if "keepdims" in inspect.signature(fun).parameters:
            kwargs["keepdims"] = True

        for i in range(1, len(dtimes)):
            if dtimes[i] - current_date >= delta:
                # apply function to slice of CoreFrame corresponding to itert
                list_of_results.append(fun(self[st_group_index:i], *args, **kwargs))
                current_date = dtimes[i]
                st_group_index = i
        list_of_results.append(fun(self[st_group_index:], *args, **kwargs))

        if out is None:
            return np.concatenate(list_of_results)

        mini_chunk_size = list_of_results[0].__array__().flatten().shape[0]

        dtimes_list = []
        for i, result in enumerate(list_of_results):
            out[out_chunk_start+ i*mini_chunk_size : out_chunk_start+ (i+1)*mini_chunk_size] =  result.__array__().flatten()
            if isinstance(result.dtimes, list):
                # TODO: test this
                dtimes_list.extend(result.dtimes)
            else:
                dtimes_list.append(result.dtimes)


        out_dtimes_list[out_dtimes_idx] = dtimes_list

        # TODO: should users be aple to su "out" parameter?
        # If yes, what "out" should actually mean? 
        # - it MUST NOT be just one coreframe, because it doesn't make sense
        # - it MIGHT be N results that we want to save to separate numpy arrays
        # DECISION: do both, but first try without it

        # TODO: should be able to handle uniquify if num = 0 is supported
        # TODO: theoretically I can handle fill_values (regularize) if I get the shape of the output


    def apply_by_generator(self, itert, fun, *args, **kwargs):
        '''
        Apply a function to slices of a CoreFrame corresponding to a time interval.

        Args:
            itert (str): A string specifying the time interval, with the form '{number}{unit}', 
                where 'number' is an integer and 'unit' is one of 'Y' (years), 'M' (months), 
                'W' (weeks), 'D' (days), 'h' (hours), 'm' (minutes), or 's' (seconds).
            fun (function): The function to apply to each slice of the CoreFrame.
            *args: Any positional arguments to pass to `fun`.
            **kwargs: Any keyword arguments to pass to `fun`.

        Yields:
            The result of applying `fun` to each slice of the CoreFrame corresponding to the 
            specified time interval.

        '''
        num, t_type = int(itert[0:-1]), itert[-1]

        delta = np.timedelta64(num, t_type)
        dtimes = self.dtimes.astype(f"datetime64[{t_type}]")

        current_date = dtimes[0]
        st_group_index = 0
        for i in range(1, len(dtimes)):
            if dtimes[i] - current_date >= delta:
                # apply function to slice of CoreFrame corresponding to itert
                yield fun(self[st_group_index:i], *args, **kwargs)
                current_date = dtimes[i]
                st_group_index = i
        yield fun(self[st_group_index:], *args, **kwargs)
        

    def split(self, itert ):
        '''
        Split a CoreFrame into slices corresponding to a time interval.

        Args:
            itert (str): A string specifying the time interval, with the form '{number}{unit}', 
                where 'number' is an integer and 'unit' is one of 'Y' (years), 'M' (months), 
                'W' (weeks), 'D' (days), 'h' (hours), 'm' (minutes), or 's' (seconds).

        Returns:
            A list of CoreFrame slices, where each slice corresponds to the specified time interval.

        '''
        return list( self.apply_by_generator(itert, lambda x: x ))

        

if __name__ == '__main__':

    n = 60
    nd_data = np.random.rand(n, 3, 4)
    base = np.datetime64("2019-02-03", 'M')
    dtimes = np.asarray([base + np.timedelta64(x, 'M') for x in range(n)])

    cf = CoreFrame(nd_data, dtimes)
    # print(cf.shape, len(cf.dtimes))
    # min_list = list(cf.apply_by_generator("2M", np.min, axis=0))    

    # res = np.max(cf, axis=1)
    # print(res)

    # TODO: add a parallelization dictionary or list

    from .config import set_config, config
    set_config(parallel=True)
    set_config(n_workers=4)


    options = {"rows_per_itert": 1}
    
    res = cf.apply_by("2M", np.min, options = options, axis=0)

    # set_config(parallel=False)
    res1 = cf.apply_by("2M", np.min, axis=0)

    print("dtimes: ", len(res.dtimes) )
    print("shape", res.shape)
    
    print(res.__array__() == res1.__array__())

    # print(res.dtimes)
    # print(res1.dtimes)
    

    # import requests

    # url = 'https://drive.google.com/uc?id=1fnXw6cgIPyeACIrPCaSUNe4kpuWVw73j'
    # r = requests.get(url)

    # with open('dataset.nc', 'wb') as f:
    #     f.write(r.content)


    # from from_nc import from_nc

    # cf = from_nc("dataset.nc", "Tair", "time")
    # # print(cf)

    # new_cf = CoreFrame(cf.__array__(), cf.dtimes, X=(0, 720), Y=(0, 360))
    # print(new_cf.get_at_XYZ( (30, 50), (30, 50)))


    # print(cf1.shape, len(cf1.dtimes))
    # print(cf2.shape, len(cf2.dtimes))

    # cf3 = np.concatenate((cf2, cf2))
    
    # print(cf3)
    # print(cf3.shape, len(cf3.dtimes))
    # print(cf3.dtimes)


    # cf1 = CoreFrame(nd_data, dtimes)

    # sdtime = np.datetime64("2022-04-02")
    # edtime = np.datetime64("2023-07-02")


    

    # min_list = list(cf.apply_by_generator("2M", np.min, axis=0))
    # max_list = list(cf.apply_by_generator("2M", np.max, axis=0, keepdims=True))
    # # mean_list = list(cf.apply_by_generator("2M", np.mean, axis=0, keepdims=True))
    
    # for i, el in enumerate(min_list):
        # print((mean_list[i] == (max_list[i] + min_list[i])/2))

    #     # print(cf.shape)
    #     # # print(type(cf))
    #     # print(cf.dtimes)


    # # print(cf[:5])

