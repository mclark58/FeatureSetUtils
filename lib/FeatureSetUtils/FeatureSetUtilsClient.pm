package FeatureSetUtils::FeatureSetUtilsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

FeatureSetUtils::FeatureSetUtilsClient

=head1 DESCRIPTION


A KBase module: FeatureSetUtils


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => FeatureSetUtils::FeatureSetUtilsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 upload_featureset_from_diff_expr

  $returnVal = $obj->upload_featureset_from_diff_expr($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a FeatureSetUtils.UploadFeatureSetFromDiffExprInput
$returnVal is a FeatureSetUtils.UploadFeatureSetFromDiffExprResult
UploadFeatureSetFromDiffExprInput is a reference to a hash where the following keys are defined:
	diff_expression_ref has a value which is a FeatureSetUtils.obj_ref
	expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	p_cutoff has a value which is a float
	q_cutoff has a value which is a float
	fold_scale_type has a value which is a string
	fold_change_cutoff has a value which is a float
	feature_set_suffix has a value which is a string
	filtered_expression_matrix_suffix has a value which is a string
	workspace_name has a value which is a string
	run_all_combinations has a value which is a FeatureSetUtils.boolean
	condition_labels has a value which is a reference to a list where each element is a string
obj_ref is a string
boolean is an int
UploadFeatureSetFromDiffExprResult is a reference to a hash where the following keys are defined:
	result_directory has a value which is a string
	up_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	down_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	filtered_expression_matrix_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a FeatureSetUtils.UploadFeatureSetFromDiffExprInput
$returnVal is a FeatureSetUtils.UploadFeatureSetFromDiffExprResult
UploadFeatureSetFromDiffExprInput is a reference to a hash where the following keys are defined:
	diff_expression_ref has a value which is a FeatureSetUtils.obj_ref
	expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	p_cutoff has a value which is a float
	q_cutoff has a value which is a float
	fold_scale_type has a value which is a string
	fold_change_cutoff has a value which is a float
	feature_set_suffix has a value which is a string
	filtered_expression_matrix_suffix has a value which is a string
	workspace_name has a value which is a string
	run_all_combinations has a value which is a FeatureSetUtils.boolean
	condition_labels has a value which is a reference to a list where each element is a string
obj_ref is a string
boolean is an int
UploadFeatureSetFromDiffExprResult is a reference to a hash where the following keys are defined:
	result_directory has a value which is a string
	up_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	down_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	filtered_expression_matrix_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description

upload_featureset_from_diff_expr: create a FeatureSet object from a RNASeqDifferentialExpression object

=back

=cut

 sub upload_featureset_from_diff_expr
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function upload_featureset_from_diff_expr (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to upload_featureset_from_diff_expr:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'upload_featureset_from_diff_expr');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "FeatureSetUtils.upload_featureset_from_diff_expr",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'upload_featureset_from_diff_expr',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method upload_featureset_from_diff_expr",
					    status_line => $self->{client}->status_line,
					    method_name => 'upload_featureset_from_diff_expr',
				       );
    }
}
 


=head2 calculate_average_expression_matrix

  $returnVal = $obj->calculate_average_expression_matrix($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a FeatureSetUtils.CalAveExpressionMatrixInput
$returnVal is a FeatureSetUtils.CalAveExpressionMatrixResult
CalAveExpressionMatrixInput is a reference to a hash where the following keys are defined:
	expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	output_suffix has a value which is a string
	workspace_name has a value which is a string
obj_ref is a string
CalAveExpressionMatrixResult is a reference to a hash where the following keys are defined:
	average_expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a FeatureSetUtils.CalAveExpressionMatrixInput
$returnVal is a FeatureSetUtils.CalAveExpressionMatrixResult
CalAveExpressionMatrixInput is a reference to a hash where the following keys are defined:
	expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	output_suffix has a value which is a string
	workspace_name has a value which is a string
obj_ref is a string
CalAveExpressionMatrixResult is a reference to a hash where the following keys are defined:
	average_expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description

calculate_average_expression_matrix: create an average ExpressionMatrix object from a ExpressionMatrix object

=back

=cut

 sub calculate_average_expression_matrix
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function calculate_average_expression_matrix (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to calculate_average_expression_matrix:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'calculate_average_expression_matrix');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "FeatureSetUtils.calculate_average_expression_matrix",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'calculate_average_expression_matrix',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method calculate_average_expression_matrix",
					    status_line => $self->{client}->status_line,
					    method_name => 'calculate_average_expression_matrix',
				       );
    }
}
 


=head2 featureset_to_tsv_file

  $files = $obj->featureset_to_tsv_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a FeatureSetUtils.FeatureSetToFileParams
$files is a FeatureSetUtils.FeatureSetTsvFiles
FeatureSetToFileParams is a reference to a hash where the following keys are defined:
	featureset_name has a value which is a string
	workspace_name has a value which is a string
FeatureSetTsvFiles is a reference to a hash where the following keys are defined:
	file_path has a value which is a string

</pre>

=end html

=begin text

$params is a FeatureSetUtils.FeatureSetToFileParams
$files is a FeatureSetUtils.FeatureSetTsvFiles
FeatureSetToFileParams is a reference to a hash where the following keys are defined:
	featureset_name has a value which is a string
	workspace_name has a value which is a string
FeatureSetTsvFiles is a reference to a hash where the following keys are defined:
	file_path has a value which is a string


=end text

=item Description



=back

=cut

 sub featureset_to_tsv_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function featureset_to_tsv_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to featureset_to_tsv_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'featureset_to_tsv_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "FeatureSetUtils.featureset_to_tsv_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'featureset_to_tsv_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method featureset_to_tsv_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'featureset_to_tsv_file',
				       );
    }
}
 


=head2 export_featureset_as_tsv_file

  $output = $obj->export_featureset_as_tsv_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a FeatureSetUtils.ExportParams
$output is a FeatureSetUtils.ExportOutput
ExportParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a string
ExportOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string

</pre>

=end html

=begin text

$params is a FeatureSetUtils.ExportParams
$output is a FeatureSetUtils.ExportOutput
ExportParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a string
ExportOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string


=end text

=item Description



=back

=cut

 sub export_featureset_as_tsv_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function export_featureset_as_tsv_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to export_featureset_as_tsv_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'export_featureset_as_tsv_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "FeatureSetUtils.export_featureset_as_tsv_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'export_featureset_as_tsv_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method export_featureset_as_tsv_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'export_featureset_as_tsv_file',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "FeatureSetUtils.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "FeatureSetUtils.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'export_featureset_as_tsv_file',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method export_featureset_as_tsv_file",
            status_line => $self->{client}->status_line,
            method_name => 'export_featureset_as_tsv_file',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for FeatureSetUtils::FeatureSetUtilsClient\n";
    }
    if ($sMajor == 0) {
        warn "FeatureSetUtils::FeatureSetUtilsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 obj_ref

=over 4



=item Description

An X/Y/Z style reference


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 UploadFeatureSetFromDiffExprInput

=over 4



=item Description

required params:
diff_expression_ref: DifferetialExpressionMatrixSet object reference
expression_matrix_ref: ExpressionMatrix object reference
p_cutoff: p value cutoff
q_cutoff: q value cutoff
fold_scale_type: one of ["linear", "log2+1", "log10+1"]  DEPRICATED NOW
fold_change_cutoff: fold change cutoff
feature_set_suffix: Result FeatureSet object name suffix
filtered_expression_matrix_suffix: Result ExpressionMatrix object name suffix
workspace_name: the name of the workspace it gets saved to
run_all_combinations: run all paired condition combinations (default true)
or
condition_labels: conditions for expression set object


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
diff_expression_ref has a value which is a FeatureSetUtils.obj_ref
expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
p_cutoff has a value which is a float
q_cutoff has a value which is a float
fold_scale_type has a value which is a string
fold_change_cutoff has a value which is a float
feature_set_suffix has a value which is a string
filtered_expression_matrix_suffix has a value which is a string
workspace_name has a value which is a string
run_all_combinations has a value which is a FeatureSetUtils.boolean
condition_labels has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
diff_expression_ref has a value which is a FeatureSetUtils.obj_ref
expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
p_cutoff has a value which is a float
q_cutoff has a value which is a float
fold_scale_type has a value which is a string
fold_change_cutoff has a value which is a float
feature_set_suffix has a value which is a string
filtered_expression_matrix_suffix has a value which is a string
workspace_name has a value which is a string
run_all_combinations has a value which is a FeatureSetUtils.boolean
condition_labels has a value which is a reference to a list where each element is a string


=end text

=back



=head2 UploadFeatureSetFromDiffExprResult

=over 4



=item Description

result_directory: folder path that holds all files generated by upload_featureset_from_diff_expr
up_feature_set_ref_list: list of generated upper FeatureSet object reference
down_feature_set_ref_list: list of generated down FeatureSet object reference
filtered_expression_matrix_ref_list: list of generated filtered ExpressionMatrix object reference
report_name: report name generated by KBaseReport
report_ref: report reference generated by KBaseReport


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
result_directory has a value which is a string
up_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
down_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
filtered_expression_matrix_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
result_directory has a value which is a string
up_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
down_feature_set_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
filtered_expression_matrix_ref_list has a value which is a reference to a list where each element is a FeatureSetUtils.obj_ref
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 CalAveExpressionMatrixInput

=over 4



=item Description

required params:
expression_matrix_ref: ExpressionMatrix object reference
output_suffix: output average ExpressionMatrix name suffix
workspace_name: the name of the workspace it gets saved to


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
output_suffix has a value which is a string
workspace_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
output_suffix has a value which is a string
workspace_name has a value which is a string


=end text

=back



=head2 CalAveExpressionMatrixResult

=over 4



=item Description

average_expression_matrix_ref: generated average ExpressionMatrix object reference
report_name: report name generated by KBaseReport
report_ref: report reference generated by KBaseReport


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
average_expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
average_expression_matrix_ref has a value which is a FeatureSetUtils.obj_ref
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 FeatureSetTsvFiles

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
file_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
file_path has a value which is a string


=end text

=back



=head2 FeatureSetToFileParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
featureset_name has a value which is a string
workspace_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
featureset_name has a value which is a string
workspace_name has a value which is a string


=end text

=back



=head2 ExportParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_ref has a value which is a string


=end text

=back



=head2 ExportOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
shock_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
shock_id has a value which is a string


=end text

=back



=cut

package FeatureSetUtils::FeatureSetUtilsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
