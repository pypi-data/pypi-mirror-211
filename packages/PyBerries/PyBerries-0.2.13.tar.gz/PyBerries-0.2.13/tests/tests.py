from os.path import join

import numpy as np
import pandas as pd

import pyberries as pyb

path = './tests/'
ds = 'Test_data'
data = pyb.data.DatasetPool(path=path, dsList=ds)
ref_bacteria = pd.read_csv(join(path, ds, f"{ds}_{0}.csv"), sep=';', low_memory=False)
ref_CFP = pd.read_csv(join(path, ds, f"{ds}_{1}.csv"), sep=';', low_memory=False)


class TestDatasetPool():

    def test_data_import(self):
        assert len(data.Bacteria) == len(ref_bacteria)
        assert len(data.CFP_spots) == len(ref_CFP)

    def test_rename_cols(self):
        data2 = pyb.data.DatasetPool(path=path, dsList=ds, rename_cols={'SpineLength': 'CellLength'})
        assert 'CellLength' in data2.Bacteria.columns
        assert 'SpineLength' not in data2.Bacteria.columns

    def test_filtering(self):
        data2 = pyb.data.DatasetPool(path=path, dsList=ds, filters={'Bacteria': 'SpineLength > 3'})
        assert len(data2.Bacteria) == len(ref_bacteria.query('SpineLength > 3'))
        data3 = data.apply_filters(filters={'Bacteria': 'SpineLength > 3'})
        assert len(data3.Bacteria) == len(ref_bacteria.query('SpineLength > 3'))

    def test_filter_propagation(self):
        data2 = data.apply_filters(filters={'Bacteria': 'SpineLength > 3'})
        assert len(data2.CFP_spots) == 42

    def test_parent_filter(self):
        data2 = data.apply_filters(filters={'CFP_spots': 'DistCC_oc2 < .4'})
        data2.filter_parent(source='CFP_spots', inplace=True)
        assert len(data2.Bacteria) == 25
        assert len(data2.CFP_spots) == 25

    def test_add_metadata(self):
        data.add_metadata({'Bacteria': 'DateTime'}, inplace=True)
        assert 'DateTime' in data.Bacteria.columns

    def test_parents(self):
        parents = {'Bacteria': None, 'CFP_spots': 'Bacteria',
                   'mCherry_spots': 'Bacteria', 'YFP_spots': 'Bacteria'}
        assert data._parents == parents

    def test_rename(self):
        data2 = data.rename_object(rename={'Bacteria': 'Bac'})
        assert ('Bac' in data2.objects) and ('Bacteria' not in data2.objects)
        assert (data2._parents['CFP_spots'] == 'Bac') and ('Bacteria' not in data2._parents.keys())
        assert not data2.Bac.empty

    def test_get_idx(self):
        data2 = data.get_idx(obj='Bacteria', idx=1, indices='Indices', newcol='new_col')
        test_index = (ref_bacteria['Indices']
                      .str.split('-', expand=True)
                      .iloc[:, 1]
                      .astype('int64')
                      )
        assert data2.Bacteria.new_col.equals(test_index)

    def test_get_histogram(self):
        hist = pyb.data.get_histogram(data.Bacteria, col='SpineLength',
                                      binsize=0.5, density=True, groupby='Dataset')
        assert not hist.empty

    def test_timeseries(self):
        timeseries_parameters = {'timeBin': 1}
        data.add_metadata({'Bacteria': 'DateTime'}, inplace=True)
        metrics_list = ['SpineLength', 'objectcount', 'intensity', 'quantile', 'aggregation', 'objectclass']
        columns_list = ['SpineLength', 'CFPCount', 'SpineLength', 'SpineLength', 'SpineLength', 'CFPCount']
        for col, m in zip(columns_list, metrics_list):
            timeseries_parameters['metric'] = m
            timeseries_parameters['col'] = col
            data_test = data.get_timeseries(object_name='Bacteria', **timeseries_parameters)
            assert not data_test.Bacteria_timeseries.empty

    def test_add_columns(self):
        data2 = data.add_columns(object_name='CFP_spots', metrics='Heatmap')
        assert 'normXpos' in data2.CFP_spots.columns
        data2 = data2.add_columns(object_name='Bacteria',
                                  metrics=['is_col_larger', 'bin_column', 'pca'],
                                  col='SpineLength', thr=3, binsize=1,
                                  include=['SpineWidth', 'SpineLength', 'CFPCount'])
        assert 'Comparison' in data2.Bacteria.columns
        assert 'SpineLength_bin' in data2.Bacteria.columns
        assert 'pca_0' in data2.Bacteria.columns
        assert 'pca_1' in data2.Bacteria.columns

    def test_add_from_parent(self):
        data2 = data.add_from_parent(object_name='CFP_spots', col=['SpineWidth', 'mCherryCount'])
        assert 'SpineWidth' in data2.Bacteria.columns
        assert 'mCherryCount' in data2.Bacteria.columns

    def test_split_fuse(self):
        data_test = (data
                     .split_column(object_name='Bacteria', col='Indices',
                                   new_cols=['Indices_0', 'Indices_1'], delimiter='-')
                     .fuse_columns(object_name='Bacteria',
                                   columns=['Indices_0', 'Indices_1'], new='Indices_fused', delimiter='-')
                     )
        assert 'Indices_0' in data_test.Bacteria.columns
        assert 'Indices_fused' in data_test.Bacteria.columns

    def test_copy(self):
        data_copy = data.copy()
        data_copy.Bacteria = pd.DataFrame()
        assert len(data.Bacteria) != len(data_copy.Bacteria)


class TestFit():

    def test_Fit(self):
        def model(x, a, b):
            return a*x+b
        test_fit = pyb.data.Fit(data.Bacteria, x='SpineWidth', y='SpineLength', model=model)
        rates = test_fit.get_fit_parameters(param_names=['Slope', 'Offset'])
        assert sum(rates.isna().any()) == 0
        models = ['monoexp_decay', 'biexp_decay', 'monoexp_decay_offset']
        model = pyb.data.get_model('monoexp_decay')
        data.Bacteria = (data.Bacteria
                         .assign(x=np.linspace(0, len(data.Bacteria), len(data.Bacteria)),
                                 y=lambda df: model(df.x, a=10, b=0.1)
                                 )
                         )
        for mod in models:
            test_fit = pyb.data.Fit(data.Bacteria, x='x', y='y', model_type=mod)
            rates2 = test_fit.get_rates(dt=1)
            assert not rates2.empty
