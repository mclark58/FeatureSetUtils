import csv
import os
import shutil
import uuid
from collections import defaultdict

from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenomeSearchUtil.GenomeSearchUtilClient import GenomeSearchUtil
from Workspace.WorkspaceClient import Workspace


class FeatureSetDownload:
    def __init__(self, config):
        self.cfg = config
        self.scratch = config['scratch']
        self.gsu = GenomeSearchUtil(os.environ['SDK_CALLBACK_URL'])
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.ws = Workspace(config["workspace-url"])

    @staticmethod
    def validate_params(params, expected={"workspace_name", "featureset_name"}):
        expected = set(expected)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))

    def to_tsv(self, params):
        working_dir = os.path.join(self.scratch,
                                   'featureset-download-'+str(uuid.uuid4()))
        os.makedirs(working_dir)
        header = ['Feature Id', 'Aliases', 'Genome', 'Type', 'Function']

        fs_name, fs_dicts = self.make_featureset_dict(params['featureset_ref'])
        files = {'file_path': "{}/{}.tsv".format(working_dir, fs_name)}
        writer = csv.DictWriter(open(files['file_path'], 'w'), header, delimiter='\t',
                                lineterminator='\n')
        writer.writeheader()
        for feat in fs_dicts:
            writer.writerow(feat)
        return fs_name, files

    def make_featureset_dict(self, fs_ref):
        features = []
        ret = self.dfu.get_objects({'object_refs': [fs_ref]})['data'][0]
        feat_set = ret['data']
        fs_name = ret['info'][1]

        feat_by_genome = defaultdict(list)
        for k, v in feat_set['elements'].items():
            feat_by_genome[v[0]].append(k)

        for genome, fids in feat_by_genome.items():
            genome_name = self.ws.get_object_info3({'objects': [{'ref': genome}]})['infos'][0][1]
            res = self.gsu.search({'ref': genome,
                                   'structured_query': {'feature_id': fids},
                                   'sort_by': [['contig_id', 1]],
                                   'start': 0,
                                   'limit': len(fids)
                                   })

            for feat in res['features']:
                features.append({'Feature Id': feat['feature_id'],
                                 'Aliases': ", ".join(feat['aliases'].keys()),
                                 'Genome': "{} ({})".format(genome_name, genome),
                                 'Type': feat['feature_type'],
                                 'Function': feat['function']
                                 })
        return fs_name, features

    def export(self, files, name, params):
        export_package_dir = os.path.join(self.scratch, name+str(uuid.uuid4()))
        os.makedirs(export_package_dir)
        for file in files:
            shutil.move(file, os.path.join(export_package_dir,
                                           os.path.basename(file)))

        # package it up and be done
        package_details = self.dfu.package_for_download({
            'file_path': export_package_dir,
            'ws_refs': [params['featureset_ref']]
        })

        return {'shock_id': package_details['shock_id']}