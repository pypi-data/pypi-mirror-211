# -*- coding: utf-8 -*-
# A function that modifies tqdm progress bars to estimate the remaining time, by allowing the user to specify how much time a step takes with respect to the others
# adds input weights=[1,2,4,8,16] for a progress bar that takes into account that iteration 2 takes twice as long as iteration 1, and iteration 3 takes 4 times as long as iteration 1, etc.
import time
from tqdm import tqdm
import itertools
import numpy as np
from pathos.helpers import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool

def determine_length_of_iterable(iterable, weights, **kwargs):
    # calulcate the total number of iterations
    if hasattr(iterable, '__len__'):
        total = len(iterable)
    elif 'total' in kwargs:
        total = kwargs['total']
    elif isinstance(weights, (list, tuple, np.ndarray)):
        total = len(weights)
    else:
        raise ValueError('tqdm_factor requires a total number of iterations to be specified, either by using an iterator with __len__, by specifying total directly or by providing a weights list')
    return total

def make_weight_list(iterable, total, weights=None):
    # determine the sum of the weights if weights is specified otherwise assume weights are all 1
    if weights is not None:
        if hasattr(weights, '__iter__'): #isinstance(weights, (list, tuple, np.ndarray)):
            min_weight = min(weights)
            weights = [int(i/min_weight) for i in weights]
            weight_sum = sum(weights)
        else:
            weight_vals = [weights(i) for i in iterable]
            min_weight = min(weight_vals)
            weights = [int(i/min_weight) for i in weight_vals]
            weight_sum = sum(weights)
    else:
        weight_sum = total
        weights = [1]*total
    return weights, weight_sum

def weighted_tqdm(iterable, weights=None, name='', print_val=False, bar_format='{l_bar}{bar}| {elapsed}<{remaining}', max_rate=30, **kwargs):
    total = determine_length_of_iterable(iterable, weights, **kwargs)
    weights_var, weight_sum = make_weight_list(iterable, total, weights)
    # create a new tqdm object, then with every iteration yield the next weight in weight_vals
    pbar = tqdm(total=weight_sum, bar_format=bar_format, **kwargs)
    start_time = time.time()
    min_time = 1/max_rate 
    i = 1
    if len(name):
        name += ': '
    # with every iteration 
    iterator = iter(iterable)
    elem = next(iterator)
    if print_val:
        pbar.set_description(name+str(elem)+' (' +str(i) + '/' + str(total) + ')')
    else:
        pbar.set_description(name+'(' +str(i) + '/' + str(total) + ')')
    yield elem
    for weight in weights_var[:-1]:
        i += 1
        elem = next(iterator)
        new_time = time.time()
        if new_time - start_time > min_time:
            if print_val:
                pbar.set_description(name+str(elem)+' (' +str(i) + '/' + str(total) + ')')
            else:
                pbar.set_description(name+'(' +str(i) + '/' + str(total) + ')')
            start_time = new_time
        pbar.update(weight)
        yield elem
    #pbar.set_description('(Done)')
    pbar.update(weights_var[-1])
    pbar.close()

def qudit_tqdm(iterable, dit=2, exp=3, name='qubits', print_val=False, bar_format='{l_bar}{bar}| {elapsed}<{remaining}', **kwargs):
    #  calculates the increase in compute for qudit calculations (by default for qubits and considereng O(n**3) operations)
    return weighted_tqdm(iterable, weights=lambda i: (dit**i)**exp, name=name, print_val=print_val, bar_format=bar_format, **kwargs)

def _parallel(function, *iterables, **kwargs):
    # Modified version of p_tqdm works with weighted_tqdm generators
    # Extract num_cpus
    num_cpus = kwargs.pop('num_cpus', None)

    # Determine num_cpus
    if num_cpus is None:
        num_cpus = cpu_count()
    elif type(num_cpus) == float:
        num_cpus = int(round(num_cpus * cpu_count()))

    # Determine length of tqdm (equal to length of shortest iterable or total kwarg), if possible
    total = kwargs.pop('total', None)
    lengths = [len(iterable) for iterable in iterables if hasattr(iterable, '__len__')]
    length = total or (min(lengths) if lengths else None)

    # Create parallel generator
    pool = Pool(num_cpus)
    for item in weighted_tqdm(pool.imap(function, *iterables), **kwargs, weights= np.ones(length)/length):
        yield item
    pool.clear()


def weighted_p_tqdm(function, *iterables, **kwargs):
    """Performs a parallel ordered map with a progress bar."""
    generator = _parallel( function, *iterables, **kwargs)
    result = list(generator)
    return result        
# A variant of tqdm, that creates a progress bar generator (via class called progress), 
# which is then used to create progress bars, which can be split between different loops
## for example:
# p = progress()# for i in p.tqdm(range(10)):
# for j in p.tqdm(range(10)):
#     pass
## this will create a progress bar where every iteration of j is counted as 1/10th of an iteration of i
class progress:
    def __init__(self, total=1000, print_val=False, bar_format='{l_bar}{bar}| {elapsed}<{remaining}', max_rate=30, **kwargs):
        self.total = total # separate these steps dynamically
        self.levels = 0
        self.weight_by_level = []
        self.ind_by_level = []
        self.current_count = 0
        self.current_count_float = 0.0
        self.pbar = None
        self.print_val = print_val
        self.bar_format = bar_format
        self.names = []
        self.min_time = 1/max_rate
        self.time = time.time()
        
    def _parallel(self, function, *iterables, num_cpus=None, **kwargs):
        # Modified version of p_tqdm works with weighted_tqdm generators

        # Determine num_cpus
        if num_cpus is None:
            num_cpus = cpu_count()
        elif type(num_cpus) == float:
            num_cpus = int(round(num_cpus * cpu_count()))

        # Create parallel generator
        pool = Pool(num_cpus)
        for item in self.tqdm(pool.imap(function, *iterables), **kwargs):
            yield item
        pool.clear()
        
    def p_tqdm(self, function, *iterables, num_cpus=None, **kwargs):
        """Performs a parallel ordered map with a progress bar."""
        generator = self._parallel(function, *iterables, num_cpus=num_cpus, **kwargs)
        result = list(generator)
        return result
        
    def weighted_tqdm(self, iterable, weights=None, name='', **kwargs):
        how_many = determine_length_of_iterable(iterable, weights, **kwargs)
        # add to total levels of the progress bar
        # add the weight of the new level to the weight_by_level list
        if len(name):
            name += ': '
        self.names.append(name)
        self.levels += 1
        my_level = self.levels # since this function is a generator, this will be the level of the progress bar for this loop
        # add weight_by_level
        weight_vals, weight_sum = make_weight_list(iterable, how_many, weights=weights)
        self.ind_by_level.append(0)
        if my_level == 1:
            weight_factor = 1 
        else:
            weight_factor = self.weight_by_level[-1][self.ind_by_level[my_level-2]]
        weight_factor = weight_factor/weight_sum
        weight_vals = [w*weight_factor for w in weight_vals]
        self.weight_by_level.append(weight_vals)
        # if this is the first level, create a new progress bar
        if my_level == 1:
            self.pbar = tqdm(total=self.total, bar_format=self.bar_format, **kwargs)
        # iterate through the iterable
        ind = 0
        # iterate through the iterable
        iterator = iter(iterable)
        elem = next(iterator)
        if self.print_val:
            self.pbar.set_description(self.names[-1]+str(elem)+' (' +str(ind) + '/' + str(how_many) + ')')
        else:
            self.pbar.set_description(self.names[-1]+'(' +str(ind) + '/' + str(how_many) + ')')
        yield elem
        for i in range(1, how_many):
            # first, check if there was a sub-tqdm call by checking my_level with the current level
            # if there wasn't, update the progress bar
            # if there was, destroy the sub-tqdm call and don't update the progress bar, as it was updated by the subcall
            # then yield the next item
            elem = next(iterator)
            if my_level == self.levels: # no sub-call -> update pbar
                self.current_count_float += self.weight_by_level[-1][ind]
                ind += 1
                new_count = round(self.current_count_float*self.total)
                diff_count = new_count - self.current_count
                new_time = time.time()
                if new_time - self.time > self.min_time:
                    if self.print_val:
                        self.pbar.set_description(self.names[-1]+str(elem)+' (' +str(ind) + '/' + str(how_many) + ')')
                    else:
                        self.pbar.set_description(self.names[-1]+'(' +str(ind) + '/' + str(how_many) + ')')
                    self.time = new_time
                self.pbar.update(diff_count)
                self.current_count = new_count
                destroyed_subcall_last = 0
            else: # there was a subcall -> destroy it
                ind += 1
                self.levels -= 1
                self.weight_by_level.pop()
                self.ind_by_level.pop()
                self.names.pop()
                destroyed_subcall_last = 1
            self.ind_by_level[my_level-1] = ind
            yield elem
        if not destroyed_subcall_last: # if there was a subcall, the progress bar was already updated
            self.current_count_float += self.weight_by_level[-1][ind]
            new_count = round(self.current_count_float*self.total)
            diff_count = new_count - self.current_count
            self.current_count = new_count
            new_time = time.time()
            if new_time - self.time > self.min_time:
                if self.print_val:
                    self.pbar.set_description(self.names[-1]+str(elem)+' (' +str(ind+1) + '/' + str(how_many) + ')')
                else:
                    self.pbar.set_description(self.names[-1]+'(' +str(ind+1) + '/' + str(how_many) + ')')
                self.time = new_time
            self.pbar.update(diff_count)
        # finished iterating through the iterable
        if my_level == 1:  # reset the object
            if self.print_val:
                self.pbar.set_description(self.names[-1]+str(elem)+' (' +str(ind+1) + '/' + str(how_many) + ')')
            else:
                self.pbar.set_description(self.names[-1]+'(' +str(ind+1) + '/' + str(how_many) + ')')
            self.time = time.time()
            self.pbar.close()
            self.pbar = None
            self.current_count = 0
            self.current_count_float = 0.0
            self.weight_by_level = []
            self.names = []
            self.levels = 0   
            new_time = time.time()
            if new_time - self.time > self.min_time: 
                if self.print_val:
                    self.pbar.set_description(self.names[-1]+str(elem)+' (' +str(ind+1) + '/' + str(how_many) + ')')
                else:
                    self.pbar.set_description(self.names[-1]+'(' +str(ind+1) + '/' + str(how_many) + ')')
                self.time = new_time
            
    def tqdm(self, iterable, **kwargs):
        return self.weighted_tqdm(iterable, **kwargs)
    
    def qudit_tqdm(self, iterable, dit=2, exp=3, **kwargs):
        return self.weighted_tqdm(iterable, weights=lambda i: (dit**i)**exp, **kwargs)
      
#p = progress(total=1000)
#for i in p.weighted_tqdm(range(5), weights=lambda i: (i+1), name='outer'):
#    for j in p.tqdm((1,2,3,4,5), name='inner'):
#        time.sleep(0.1*(i+1))      

class weighted_kronbinations_tqdm:
    def __init__(self, list_of_iterators, list_of_weights, total=1000, bar_format='{l_bar}{bar}| {elapsed}<{remaining}', max_rate=30, **kwargs):
        # this function takes a list of iterators and weights and returns a generator that iterates through the kronecker product of the iterators
        # Prepare data
        lengths = []
        weights = []
        for i, w in zip(list_of_iterators, list_of_weights):
            lengths.append(determine_length_of_iterable(i, w, **kwargs))
            weights_var, sum_weights = make_weight_list(i, lengths[-1], w)
            weights.append([j/sum_weights for j in weights_var])
        self.lengths = lengths
        self.total_length = np.prod(lengths)
        self.weights = weights
        self.total = total
        # Variables for subincrements 
        # similar to progress class but lowest level is kronbinations level and 
        # treated differently
        self.levels = 0
        self.weight_by_level = []
        self.ind_by_level = []
        self.names = []
        self.bar_format = bar_format
        self.last_update_time = time.time()
        self.min_t = 1/max_rate
        
    def init(self, indexes, **kwargs):
        # indexes is a 2d array of indexes, where each row is an index and each column is an iterator
        # Construct a pbar object, and find the total weight  of all indexes to renormalize for the pbar
        # find sum_of_weights = sum([weight of every index]), with weight of an index being the product of the weights of the iterators that make up that index
        weights = []
        for ind in indexes:
            weights.append(np.prod([self.weights[i][j] for i, j in enumerate(ind)]))
        sum_weights = sum(weights)
        if 'total' in kwargs:
            self.total = kwargs['total']
        factor = self.total / sum_weights 
        self.curr_weights = [i*factor for i in weights]

        self.indexes = indexes
        self.len_indexes = len(indexes)
        self.curr_ind = 0 # tracks the current indexes index in indexes
        self.cumm_weight = 0.0
        self.curr_pbar_index = 0
        self.pbar = tqdm(total=self.total, bar_format=self.bar_format)
        
                
    def _parallel(self, function, *iterables, num_cpus=None, **kwargs):
        # Modified version of p_tqdm works with weighted_tqdm generators

        # Determine num_cpus
        if num_cpus is None:
            num_cpus = cpu_count()
        elif type(num_cpus) == float:
            num_cpus = int(round(num_cpus * cpu_count()))

        # Create parallel generator
        pool = Pool(num_cpus)
        for item in self.sub_tqdm(pool.imap(function, *iterables), **kwargs):
            yield item
        pool.clear()
        
    def p_tqdm(self, function, *iterables, num_cpus=None, **kwargs):
        """Performs a parallel ordered map with a progress bar."""
        generator = self._parallel(function, *iterables, num_cpus=num_cpus, **kwargs)
        result = list(generator)
        return result
        
    def sub_tqdm(self, iterable, weights=None, name='', **kwargs):
        how_many = determine_length_of_iterable(iterable, weights, **kwargs)
        self.levels += 1
        my_level = self.levels
        if len(name):
            name += ': '
        self.names.append(name)
        self.ind_by_level.append(0)
        weight_vals, weight_sum = make_weight_list(iterable, how_many, weights=weights)
        if my_level == 1:
            weight_factor = self.curr_weights[self.curr_ind]  # multiply with current weight of level 0
        else:
            weight_factor = self.weight_by_level[-1][self.ind_by_level[my_level-2]]
        weight_factor = weight_factor/weight_sum
        weight_vals = [w*weight_factor for w in weight_vals]
        self.weight_by_level.append(weight_vals)
        ind = 0
        self.pbar.set_description(self.names[-1]+' (' +str(ind) + '/' + str(how_many) + ')')
        iterator = iter(iterable)
        yield next(iterator) 
        for i in range(1, how_many):
            elem = next(iterator)
            if my_level == self.levels: # no sub-call -> update pbar
                self.cumm_weight += self.weight_by_level[-1][ind]
                ind += 1
                new_count = round(self.cumm_weight)
                diff_count = new_count - self.curr_pbar_index
                self.pbar.set_description(self.names[-1]+' (' +str(ind) + '/' + str(how_many) + ')')
                self.pbar.update(diff_count)
                self.current_count = new_count
                self.curr_pbar_index = new_count
                destroyed_subcall_last = 0
            else: # there was a subcall -> destroy it
                ind += 1
                self.levels -= 1
                self.weight_by_level.pop()
                self.ind_by_level.pop()
                self.names.pop()
                destroyed_subcall_last = 1
            self.ind_by_level[my_level-1] = ind
            yield elem
        if not destroyed_subcall_last: # if there was a subcall, the progress bar was already updated
            self.cumm_weight += self.weight_by_level[-1][ind]
            new_count = round(self.cumm_weight)
            diff_count = new_count - self.current_count
            self.current_count = new_count
            self.curr_pbar_index = new_count
            self.pbar.set_description(self.names[-1]+'(' +str(ind+1) + '/' + str(how_many) + ')')
            self.pbar.update(diff_count)
        else:
            self.pbar.set_description(self.names[-1]+'(' +str(ind+1) + '/' + str(how_many) + ')')
                
    def increment(self):
        # increment 
        curr_weight = self.curr_weights[self.curr_ind]
        self.curr_ind += 1
        new_time = time.time()
        if new_time - self.last_update_time > self.min_t:
            self.pbar.set_description('(' +str(self.curr_ind) + '/' + str(self.total_length) + ')')
            self.last_update_time = new_time
        if self.levels == 0:
            self.cumm_weight += curr_weight 
            new_index = round(self.cumm_weight)
            diff = new_index - self.curr_pbar_index
            self.curr_pbar_index = new_index
            self.pbar.update(diff)
        else: # reset sublevels
            self.levels = 0
            self.weight_by_level = []
            self.ind_by_level = []
            self.names = []
            
    def close(self):
        self.pbar.set_description('(' +str(self.curr_ind) + '/' + str(self.total_length) + ')')
        self.pbar.update(0)
        self.pbar.close()
        
    def all_indexes(self):
        list_of_indexes = [list(np.arange(0, len(l))) for l in list_of_iterators]
        return np.array(list(itertools.product(*list_of_indexes)))
    