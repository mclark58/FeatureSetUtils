# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from FeatureSetUtils.FeatureSetUtilsImpl import FeatureSetUtils
from FeatureSetUtils.FeatureSetUtilsServer import MethodContext
from FeatureSetUtils.authclient import KBaseAuth as _KBaseAuth


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
        cls.wsName = "test_kb_stringtie_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # upload differetial expression object
        cls.diff_expression_ref = '2409/228/1'

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_bad_upload_featureset_from_diff_expr_params(self):
        invalidate_input_params = {
          'missing_diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"diff_expression_ref" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'missing_feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"feature_set_name" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'missing_p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"p_cutoff" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'missing_q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"q_cutoff" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'missing_fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"fold_scale_type" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'missing_fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"fold_change_cutoff" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'fold_scale_type',
          'fold_change_cutoff': 'fold_change_cutoff',
          'missing_workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

        invalidate_input_params = {
          'diff_expression_ref': 'diff_expression_ref',
          'feature_set_name': 'feature_set_name',
          'p_cutoff': 'p_cutoff',
          'q_cutoff': 'q_cutoff',
          'fold_scale_type': 'invalid',
          'fold_change_cutoff': 'fold_change_cutoff',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Input fold scale type value \[invalid\] is not valid'):
            self.getImpl().upload_featureset_from_diff_expr(self.getContext(),
                                                            invalidate_input_params)

    def test_upload_featureset_from_diff_expr(self):

        feature_set_name = 'MyFeatureSet'
        input_params = {
            'diff_expression_ref': self.diff_expression_ref,
            'feature_set_name': feature_set_name,
            'p_cutoff': 0.05,
            'q_cutoff': 0.05,
            "fold_scale_type": 'log2+1',
            "fold_change_cutoff": 1,
            'workspace_name': self.getWsName()
        }

        result = self.getImpl().upload_featureset_from_diff_expr(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        self.assertTrue('feature_set_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
