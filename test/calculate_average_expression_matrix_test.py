# -*- coding: utf-8 -*-
import os  # noqa: F401
import time
import unittest
from configparser import ConfigParser  # py3
from os import environ

from FeatureSetUtils.FeatureSetUtilsImpl import FeatureSetUtils
from FeatureSetUtils.FeatureSetUtilsServer import MethodContext
from FeatureSetUtils.authclient import KBaseAuth as _KBaseAuth
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace as workspaceService


class FeatureSetUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('FeatureSetUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'FeatureSetUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = FeatureSetUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        suffix = int(time.time() * 1000)
        cls.wsName = "test_kb_featureset_util_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

        cls.dfu = DataFileUtil(cls.callback_url)
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # upload expression matrix object
        em_data = {'scale': 'log2',
                   'type': 'level',
                   'data': {'row_ids': ['gene_1', 'gene_2', 'gene_3'],
                            'values': [[1.0, 2.0, 3.0, 4.0],
                                       [0.1, 0.2, 0.3, 0.4],
                                       [0.4, 0.3, 0.2, 0.1]],
                            'col_ids': ['label_1', 'label_2', 'label_3', 'label_4']},
                   'feature_mapping': {'label_1': 'label_1',
                                       'label_2': 'label_2',
                                       'label_3': 'label_3',
                                       'label_4': 'label_4'},
                   'condition_mapping': {'label_1': 'condition_1',
                                         'label_2': 'condition_2',
                                         'label_3': 'condition_1',
                                         'label_4': 'condition_2'}}

        data_type = 'KBaseFeatureValues.ExpressionMatrix'
        res = cls.dfu.save_objects({'id': cls.dfu.ws_name_to_id(cls.wsName),
                                    'objects': [{'type': data_type,
                                                 'data': em_data,
                                                 'name': 'test_expression_matrix'}]
                                    })[0]

        cls.expression_matrix_ref = str(res[6]) + '/' + str(res[0]) + '/' + str(res[4])

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_bad_calculate_average_expression_matrix_params(self):
        invalidate_input_params = {'missing_expression_matrix_ref': 'expression_matrix_ref',
                                   'output_suffix': 'output_suffix',
                                   'workspace_name': 'workspace_name'}
        with self.assertRaisesRegexp(ValueError,
                                     '"expression_matrix_ref" parameter is required, but missing'):
            self.getImpl().calculate_average_expression_matrix(self.getContext(),
                                                               invalidate_input_params)

        invalidate_input_params = {'expression_matrix_ref': 'expression_matrix_ref',
                                   'missing_output_suffix': 'output_suffix',
                                   'workspace_name': 'workspace_name'}
        with self.assertRaisesRegexp(ValueError,
                                     '"output_suffix" parameter is required, but missing'):
            self.getImpl().calculate_average_expression_matrix(self.getContext(),
                                                               invalidate_input_params)

        invalidate_input_params = {'expression_matrix_ref': 'expression_matrix_ref',
                                   'output_suffix': 'output_suffix',
                                   'missing_workspace_name': 'workspace_name'}
        with self.assertRaisesRegexp(ValueError,
                                     '"workspace_name" parameter is required, but missing'):
            self.getImpl().calculate_average_expression_matrix(self.getContext(),
                                                               invalidate_input_params)

    def test_calculate_average_expression_matrix(self):

        input_params = {
            'expression_matrix_ref': self.expression_matrix_ref,
            'output_suffix': '_average',
            'workspace_name': self.getWsName()
        }

        result = self.getImpl().calculate_average_expression_matrix(self.getContext(),
                                                                    input_params)[0]

        self.assertTrue('average_expression_matrix_ref' in result)
        average_expression_matrix_ref = result['average_expression_matrix_ref']
        data = self.dfu.get_objects({'object_refs':
                                    [average_expression_matrix_ref]})['data'][0]['data']

        print(data)

        self.assertTrue('condition_mapping' in data)
        self.assertTrue('data' in data)
        self.assertTrue('row_ids' in data['data'])
        self.assertTrue('values' in data['data'])
        self.assertTrue('col_ids' in data['data'])

        col_ids = data['data']['col_ids']
        row_ids = data['data']['row_ids']
        values = data['data']['values']

        expected_col_ids = ['condition_1', 'condition_2']
        expected_row_ids = ['gene_1', 'gene_2', 'gene_3']
        expected_values = [[2.0, 3.0], [0.2, 0.3], [0.3, 0.2]]

        self.assertCountEqual(col_ids, expected_col_ids)
        self.assertCountEqual(row_ids, expected_row_ids)
        self.assertCountEqual(values, expected_values)

        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
