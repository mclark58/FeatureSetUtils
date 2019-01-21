import csv
import errno
import logging
import os
import re
import time
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeSearchUtilClient import GenomeSearchUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as Workspace


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class FeatureSetBuilder:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _validate_upload_featureset_from_diff_expr_params(self, params):
        """
        _validate_upload_featureset_from_diff_expr_params:
                validates params passed to upload_featureset_from_diff_expr method
        """

        log('start validating upload_featureset_from_diff_expr params')

        # check for required parameters
        for p in ['diff_expression_ref', 'workspace_name',
                  'p_cutoff', 'q_cutoff', 'fold_change_cutoff']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        p = params.get('fold_scale_type')
        if p and p != 'logarithm':
            raise ValueError('"fold_scale_type" parameter must be set to "logarithm", if used')

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def _generate_report(self, up_feature_set_ref_list, down_feature_set_ref_list,
                         filtered_expression_matrix_ref_list, workspace_name):
        """
        _generate_report: generate summary report
        """

        log('start creating report')

        output_html_files = self._generate_html_report(up_feature_set_ref_list,
                                                       down_feature_set_ref_list)

        objects_created = list()
        for up_feature_set_ref in up_feature_set_ref_list:
            objects_created += [{'ref': up_feature_set_ref,
                                 'description': 'Upper FeatureSet Object'}]
        for down_feature_set_ref in down_feature_set_ref_list:
            objects_created += [{'ref': down_feature_set_ref,
                                 'description': 'Lower FeatureSet Object'}]

        for filtered_expression_matrix_ref in filtered_expression_matrix_ref_list:
            objects_created += [{'ref': filtered_expression_matrix_ref,
                                 'description': 'Filtered ExpressionMatrix Object'}]

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'objects_created': objects_created,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_FeatureSetUtils_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _generate_html_report(self, up_feature_set_ref_list, down_feature_set_ref_list):
        """
        _generate_html_report: generate html summary report
        """

        log('start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        uppper_feature_content = ''
        for up_feature_set_ref in up_feature_set_ref_list:
            feature_set_obj = self.ws.get_objects2({'objects':
                                                    [{'ref':
                                                     up_feature_set_ref}]})['data'][0]
            feature_set_data = feature_set_obj['data']
            feature_set_info = feature_set_obj['info']

            feature_set_name = feature_set_info[1]

            elements = feature_set_data.get('elements')
            feature_ids = list(elements.keys())

            uppper_feature_content += '<tr><td>{}</td><td>{}</td></tr>'.format(feature_set_name,
                                                                               len(feature_ids))

        lower_feature_content = ''
        for down_feature_set_ref in down_feature_set_ref_list:
            feature_set_obj = self.ws.get_objects2({'objects':
                                                    [{'ref':
                                                     down_feature_set_ref}]})['data'][0]
            feature_set_data = feature_set_obj['data']
            feature_set_info = feature_set_obj['info']

            feature_set_name = feature_set_info[1]

            elements = feature_set_data.get('elements')
            feature_ids = list(elements.keys())

            lower_feature_content += '<tr><td>{}</td><td>{}</td></tr>'.format(feature_set_name,
                                                                              len(feature_ids))

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<tr><td>Upper_FeatureSet</td></tr>',
                                                          uppper_feature_content)

                report_template = report_template.replace('<tr><td>Lower_FeatureSet</td></tr>',
                                                          lower_feature_content)

                result_file.write(report_template)

        html_report.append({'path': result_file_path,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report'})
        return html_report

    def _process_diff_expression(self, diff_expression_set_ref, result_directory,
                                 condition_label_pair):
        """
        _process_diff_expression: process differential expression object info
        """

        log('start processing differential expression object')

        diff_expr_set_data = self.ws.get_objects2({'objects':
                                                  [{'ref':
                                                   diff_expression_set_ref}]})['data'][0]['data']

        set_items = diff_expr_set_data['items']

        diff_expr_matrix_file_name = 'gene_results.csv'
        diff_expr_matrix_file = os.path.join(result_directory, diff_expr_matrix_file_name)

        with open(diff_expr_matrix_file, 'w') as csvfile:
            fieldnames = ['gene_id', 'log2_fold_change', 'p_value', 'q_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        for set_item in set_items:
            diff_expression_ref = set_item['ref']

            diff_expression_data = self.ws.get_objects2({'objects':
                                                        [{'ref':
                                                         diff_expression_ref}]})['data'][0]['data']

            label_string = set_item['label']
            label_list = [x.strip() for x in label_string.split(',')]
            condition_1 = label_list[0]
            condition_2 = label_list[1]

            if condition_1 in condition_label_pair and condition_2 in condition_label_pair:
                genome_id = diff_expression_data['genome_ref']
                matrix_data = diff_expression_data['data']
                selected_diff_expression_ref = diff_expression_ref

                with open(diff_expr_matrix_file, 'a') as csvfile:
                    row_ids = matrix_data.get('row_ids')
                    row_values = matrix_data.get('values')
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    for pos, row_id in enumerate(row_ids):
                        row_value = row_values[pos]
                        writer.writerow({'gene_id': row_id,
                                         'log2_fold_change': row_value[0],
                                         'p_value': row_value[1],
                                         'q_value': row_value[2]})

        return diff_expr_matrix_file, genome_id, selected_diff_expression_ref

    def _generate_feature_set(self, feature_ids, genome_id, workspace_name, feature_set_name):
        """
        _generate_feature_set: generate FeatureSet object

        KBaseCollections.FeatureSet type:
        typedef structure {
            string description;
            list<feature_id> element_ordering;
            mapping<feature_id, list<genome_ref>> elements;
        } FeatureSet;
        """

        log('start saving KBaseCollections.FeatureSet object')

        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        elements = {feature_id: [genome_id] for feature_id in feature_ids}
        feature_set_data = {'description': 'Generated FeatureSet from DifferentialExpression',
                            'element_ordering': feature_ids,
                            'elements': elements}

        object_type = 'KBaseCollections.FeatureSet'
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': feature_set_data,
                         'name': feature_set_name}]}

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        feature_set_obj_ref = "{}/{}/{}".format(dfu_oi[6], dfu_oi[0], dfu_oi[4])

        return feature_set_obj_ref

    def _process_matrix_file(self, diff_expr_matrix_file, comp_p_value, comp_q_value,
                             comp_fold_change_cutoff):
        """
        _process_matrix_file: filter matrix file by given cutoffs
        """

        log('start processing matrix file')

        up_feature_ids = []
        down_feature_ids = []

        if comp_fold_change_cutoff < 0:
            comp_fold_change_cutoff = -comp_fold_change_cutoff

        with open(diff_expr_matrix_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                feature_id = row['gene_id']
                row_p_value = row['p_value']
                row_q_value = row['q_value']
                row_fold_change_cutoff = row['log2_fold_change']

                null_value = {'NA', 'null', ''}
                col_value = {row_p_value, row_q_value, row_fold_change_cutoff}

                if not col_value.intersection(null_value):
                    p_value_condition = float(row_p_value) <= comp_p_value
                    q_value_condition = float(row_q_value) <= comp_q_value

                    up_matches_condition = (p_value_condition and q_value_condition and
                                                         (float(row_fold_change_cutoff) >=
                                                         comp_fold_change_cutoff))

                    down_matches_condition = (p_value_condition and q_value_condition and
                                             (float(row_fold_change_cutoff) <=
                                             -comp_fold_change_cutoff))

                    if up_matches_condition:
                        up_feature_ids.append(feature_id)
                    elif down_matches_condition:
                        down_feature_ids.append(feature_id)

        return list(set(up_feature_ids)), list(set(down_feature_ids))

    def _filter_expression_matrix(self, expression_matrix_ref, feature_ids,
                                  workspace_name, filtered_expression_matrix_suffix="",
                                  diff_expression_matrix_ref=None,
                                  filtered_expression_matrix_name=None):
        """
        _filter_expression_matrix: generated filtered expression matrix
        """

        log('start saving ExpressionMatrix object')

        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        expression_matrix_obj = self.dfu.get_objects({'object_refs':
                                                     [expression_matrix_ref]})['data'][0]

        expression_matrix_info = expression_matrix_obj['info']
        expression_matrix_data = expression_matrix_obj['data']

        expression_matrix_name = expression_matrix_info[1]

        if not filtered_expression_matrix_name:
            if re.match('.*_*[Ee]xpression_*[Mm]atrix', expression_matrix_name):
                filtered_expression_matrix_name = re.sub('_*[Ee]xpression_*[Mm]atrix',
                                                         filtered_expression_matrix_suffix,
                                                         expression_matrix_name)
            else:
                filtered_expression_matrix_name = expression_matrix_name + \
                    filtered_expression_matrix_suffix

        filtered_expression_matrix_data = expression_matrix_data.copy()

        data = filtered_expression_matrix_data['data']

        row_ids = data['row_ids']
        values = data['values']
        filtered_data = data.copy()

        filtered_row_ids = list()
        filtered_values = list()
        for pos, row_id in enumerate(row_ids):
            if row_id in feature_ids:
                filtered_row_ids.append(row_id)
                filtered_values.append(values[pos])

        filtered_data['row_ids'] = filtered_row_ids
        filtered_data['values'] = filtered_values
        filtered_expression_matrix_data['data'] = filtered_data

        expression_obj = {'type': expression_matrix_info[2], 'data': filtered_expression_matrix_data,
                          'name': filtered_expression_matrix_name}
        # we now save the filtering DEM in a EM field added for this purpose
        if diff_expression_matrix_ref:
            expression_obj['data']['diff_expr_matrix_ref'] = diff_expression_matrix_ref
            expression_obj['extra_provenance_input_refs'] = [diff_expression_matrix_ref]

        save_object_params = {
            'id': workspace_id,
            'objects': [expression_obj]}

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        filtered_expression_matrix_ref = "{}/{}/{}".format(dfu_oi[6], dfu_oi[0], dfu_oi[4])

        return filtered_expression_matrix_ref

    def _xor(self, a, b):
        return bool(a) != bool(b)

    def _check_input_labels(self, condition_pairs, available_condition_labels):
        """
        _check_input_labels: check input condition pairs
        """
        checked = True
        for condition_pair in condition_pairs:

            label_string = condition_pair['label_string'][0].strip()
            label_list = [x.strip() for x in label_string.split(',')]
            first_label = label_list[0]
            second_label = label_list[1]

            if first_label not in available_condition_labels:
                error_msg = 'Condition: {} is not availalbe. '.format(first_label)
                error_msg += 'Available conditions: {}'.format(available_condition_labels)
                raise ValueError(error_msg)

            if second_label not in available_condition_labels:
                error_msg = 'Condition: {} is not availalbe. '.format(second_label)
                error_msg += 'Available conditions: {}'.format(available_condition_labels)
                raise ValueError(error_msg)

            if first_label == second_label:
                raise ValueError('Input conditions are the same')

        return checked

    def _get_condition_labels(self, diff_expression_set_ref):
        """
        _get_condition_labels: get all possible condition label pairs
        """
        log('getting all possible condition pairs')

        condition_label_pairs = list()
        available_condition_labels = set()
        diff_expression_set_obj = self.ws.get_objects2({'objects':
                                                       [{'ref': diff_expression_set_ref}]
                                                        })['data'][0]
        diff_expression_set_data = diff_expression_set_obj['data']
        items = diff_expression_set_data.get('items')
        for item in items:
            label_string = item['label']
            label_list = [x.strip() for x in label_string.split(',')]
            condition_label_pairs.append(label_list)
            available_condition_labels |= set(label_list)

        log('all pssible conditon pairs:\n{}'.format(condition_label_pairs))

        return condition_label_pairs, available_condition_labels

    def _get_feature_ids(self, genome_ref, ids):
        """
        _get_feature_ids: get feature ids from genome
        """

        genome_features = self.gsu.search({'ref': genome_ref,
                                           'limit': len(ids),
                                           'structured_query': {"$or": [{"feature_id": x}
                                                                        for x in ids]},
                                           'sort_by': [['feature_id', True]]})['features']

        features_ids = set((feature.get('feature_id') for feature in genome_features))

        return features_ids

    def _build_fs_obj(self, params):
        new_feature_set = {
            'description': '',
            'element_ordering': [],
            'elements': {}
        }
        genome_ref = params['genome']
        if params.get('base_feature_sets', []) and None not in params['base_feature_sets']:
            base_feature_sets = self.dfu.get_objects(
                {'object_refs': params['base_feature_sets']}
            )['data']
            for ret in base_feature_sets:
                base_set = ret['data']
                base_set_name = ret['info'][1]

                new_feature_set['element_ordering'] += [x for x in base_set['element_ordering']
                                                        if x not in new_feature_set['elements']]
                for element, genome_refs in base_set['elements'].items():
                    if element in new_feature_set['elements']:
                        new_feature_set['elements'][element] += [x for x in genome_refs if x not in
                                                                 new_feature_set['elements'][
                                                                     element]]
                    else:
                        new_feature_set['elements'][element] = genome_refs
                new_feature_set['description'] += 'From FeatureSet {}: {}\n'.format(
                    base_set_name, base_set.get('description'))
        new_feature_ids = []
        if params.get('feature_ids'):
            new_feature_ids += params['feature_ids']
        if params.get('feature_ids_custom'):
            new_feature_ids += params['feature_ids_custom'].split(',')
        if new_feature_ids:
            genome_feature_ids = self._get_feature_ids(genome_ref, new_feature_ids)
        for new_feature in new_feature_ids:
            if new_feature not in genome_feature_ids:
                raise ValueError('Feature ID {} does not exist in the supplied genome {}'.format(
                    new_feature, genome_ref))
            if new_feature in new_feature_set['elements']:
                if genome_ref not in new_feature_set['elements'][new_feature]:
                    new_feature_set['elements'][new_feature].append(genome_ref)
            else:
                new_feature_set['elements'][new_feature] = [genome_ref]
                new_feature_set['element_ordering'].append(new_feature)

        if params.get('description'):
            new_feature_set['description'] = params['description']

        return new_feature_set

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.ws = Workspace(self.ws_url, token=self.token)
        self.dfu = DataFileUtil(self.callback_url)
        self.gsu = GenomeSearchUtil(self.callback_url)
        self.scratch = config['scratch']

    def upload_featureset_from_diff_expr(self, params):
        """
        upload_featureset_from_diff_expr: create FeatureSet from RNASeqDifferentialExpression
                                          based on given threshold cutoffs

        required params:
        diff_expression_ref: DifferetialExpressionMatrixSet object reference
        expression_matrix_ref: ExpressionMatrix object reference
        p_cutoff: p value cutoff
        q_cutoff: q value cutoff
        fold_scale_type: one of ["linear", "log2+1", "log10+1"]
        fold_change_cutoff: fold change cutoff
        feature_set_suffix: Result FeatureSet object name suffix
        filtered_expression_matrix_suffix: Result ExpressionMatrix object name suffix
        workspace_name: the name of the workspace it gets saved to

        return:
        result_directory: folder path that holds all files generated
        up_feature_set_ref_list: list of generated upper FeatureSet object reference
        down_feature_set_ref_list: list of generated down FeatureSet object reference
        filtered_expression_matrix_ref_list: list of generated filtered ExpressionMatrix object ref
        report_name: report name generated by KBaseReport
        report_ref: report reference generated by KBaseReport
        """

        self._validate_upload_featureset_from_diff_expr_params(params)

        diff_expression_set_ref = params.get('diff_expression_ref')
        diff_expression_set_info = self.ws.get_object_info3({"objects":
                                                            [{"ref": diff_expression_set_ref}]}
                                                            )['infos'][0]
        diff_expression_set_name = diff_expression_set_info[1]

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        (available_condition_label_pairs,
         available_condition_labels) = self._get_condition_labels(diff_expression_set_ref)

        run_all_combinations = params.get('run_all_combinations')
        condition_pairs = params.get('condition_pairs')
        if not self._xor(run_all_combinations, condition_pairs):
            error_msg = "Invalid input:\nselect 'Run All Paired Condition Combinations' "
            error_msg += "or provide partial condition pairs. Don't do both or neither"
            raise ValueError(error_msg)

        if run_all_combinations:
            condition_label_pairs = available_condition_label_pairs
        else:
            if self._check_input_labels(condition_pairs, available_condition_labels):
                condition_label_pairs = list()
                for condition_pair in condition_pairs:
                    label_string = condition_pair['label_string'][0].strip()
                    condition_labels = [x.strip() for x in label_string.split(',')]
                    condition_label_pairs.append(condition_labels)

        up_feature_set_ref_list = list()
        down_feature_set_ref_list = list()
        filtered_expression_matrix_ref_list = list()

        for condition_label_pair in condition_label_pairs:
            condition_string = '-'.join(reversed(condition_label_pair))
            diff_expr_matrix_file, genome_id, diff_expr_matrix_ref = self._process_diff_expression(
                                                                diff_expression_set_ref,
                                                                result_directory,
                                                                condition_label_pair)
            up_feature_ids, down_feature_ids = self._process_matrix_file(
                                                                diff_expr_matrix_file,
                                                                params.get('p_cutoff'),
                                                                params.get('q_cutoff'),
                                                                params.get('fold_change_cutoff'))
            filtered_em_name = condition_string + params.get('filtered_expression_matrix_suffix')
            if params.get('expression_matrix_ref'):
                filtered_expression_matrix_ref = self._filter_expression_matrix(
                                                params.get('expression_matrix_ref'),
                                                up_feature_ids + down_feature_ids,
                                                params.get('workspace_name'), "",
                                                diff_expr_matrix_ref, filtered_em_name)
                filtered_expression_matrix_ref_list.append(filtered_expression_matrix_ref)

            feature_set_suffix = params.get('feature_set_suffix', "")
            up_feature_set_name = "{}_{}_up{}".format(
                diff_expression_set_name, condition_string, feature_set_suffix)
            up_feature_set_ref = self._generate_feature_set(up_feature_ids,
                                                            genome_id,
                                                            params.get('workspace_name'),
                                                            up_feature_set_name)
            up_feature_set_ref_list.append(up_feature_set_ref)

            down_feature_set_name = "{}_{}_down{}".format(
                diff_expression_set_name, condition_string, feature_set_suffix)
            down_feature_set_ref = self._generate_feature_set(down_feature_ids,
                                                              genome_id,
                                                              params.get('workspace_name'),
                                                              down_feature_set_name)
            down_feature_set_ref_list.append(down_feature_set_ref)

        returnVal = {'result_directory': result_directory,
                     'up_feature_set_ref_list': up_feature_set_ref_list,
                     'down_feature_set_ref_list': down_feature_set_ref_list,
                     'filtered_expression_matrix_ref_list': filtered_expression_matrix_ref_list}

        report_output = self._generate_report(up_feature_set_ref_list, down_feature_set_ref_list,
                                              filtered_expression_matrix_ref_list,
                                              params.get('workspace_name'))
        returnVal.update(report_output)

        return returnVal

    def filter_matrix_with_fs(self, params):
        self.validate_params(params, ('feature_set_ref', 'workspace_name',
                                      'expression_matrix_ref', 'filtered_expression_matrix_suffix'))
        ret = self.dfu.get_objects(
            {'object_refs': [params['feature_set_ref']]}
        )['data'][0]
        feature_set = ret['data']
        feature_set_name = ret['info'][1]
        feature_ids = set(feature_set['elements'].keys())
        filtered_matrix_ref = self._filter_expression_matrix(
            params['expression_matrix_ref'], feature_ids, params['workspace_name'],
            params['filtered_expression_matrix_suffix'])

        objects_created = [{'ref': filtered_matrix_ref,
                            'description': 'Filtered ExpressionMatrix Object'}]
        message = "Filtered Expression Matrix based of the {} feature ids present in {}"\
            .format(len(feature_ids), feature_set_name)

        report_params = {'message': message,
                         'workspace_name': params['workspace_name'],
                         'objects_created': objects_created,
                         'report_object_name': 'kb_FeatureSetUtils_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        return {'filtered_expression_matrix_ref': filtered_matrix_ref,
                'report_name': output['name'], 'report_ref': output['ref']}

    def build_feature_set(self, params):
        self.validate_params(params, {'output_feature_set', 'workspace_name', },
                             {'genome', 'feature_ids', 'feature_ids_custom', 'base_feature_sets',
                              'description'})
        feature_sources = ('feature_ids', 'feature_ids_custom', 'base_feature_sets')
        if not any([params.get(x) for x in feature_sources]):
            raise ValueError("You must supply at least one feature source: {}".format(
                ", ".join(feature_sources)))
        workspace_id = self.dfu.ws_name_to_id(params['workspace_name'])

        new_feature_set = self._build_fs_obj(params)
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': 'KBaseCollections.FeatureSet',
                         'data': new_feature_set,
                         'name': params['output_feature_set']}]}

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        feature_set_obj_ref = '{}/{}/{}'.format(dfu_oi[6], dfu_oi[0], dfu_oi[4])

        objects_created = [{'ref': feature_set_obj_ref,
                            'description': 'Feature Set'}]
        message = 'A new feature set containing {} features was created.'.format(
            len(new_feature_set['elements']))

        report_params = {'message': message,
                         'workspace_name': params['workspace_name'],
                         'objects_created': objects_created,
                         'report_object_name': 'kb_FeatureSetUtils_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        return {'feature_set_ref': feature_set_obj_ref,
                'report_name': output['name'], 'report_ref': output['ref']}
