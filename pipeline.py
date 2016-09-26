import os

def execute_pipleline(n_prototipes, window_size, step, max_level):
    call1 = 'python 1.sample.py lightcurves.R.txt {0} std {1} {2}'.format(n_prototipes, window_size, step)
    call2 = 'python 2.twed.py lightcurves.R.txt {0} std {1} {2}'.format(n_prototipes, window_size, step)
    call3 = 'python 3.tree_building.py lightcurves.R.txt {0} std weighted {1} {2} {3}'.format(n_prototipes, window_size,
                                                                                              step, max_level)
    model_name = 'sequence_tree_lightcurves.R.txt_{0}samples_semistdFalse_stdTrue_20levels_{1}_{2}.dill'.format(n_prototipes,
                                                                                                          window_size, step)
    call4 = 'python 4.ndcg_test.py {0} 100 20'.format(model_name)
    print('RUNNING 1.SAMPLE')
    os.system(call1)
    print('RUNNING 2.TWED')
    os.system(call2)
    print('RUNNING 3.TREE_BUILDING')
    os.system(call3)
    print('RUNNING 4.NDCG_TEST')
    os.system(call4)
    print('DONE')

if __name__ == '__main__':
    n = 2
    window = 250
    step = 10
    max_level = 20
    execute_pipleline(n, window, step, max_level)

