
package us.kbase.featuresetutils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: UploadFeatureSetFromDiffExprInput</p>
 * <pre>
 * required params:
 * diff_expression_ref: DifferetialExpressionMatrixSet object reference
 * expression_matrix_ref: ExpressionMatrix object reference
 * p_cutoff: p value cutoff
 * q_cutoff: q value cutoff
 * fold_scale_type: one of ["linear", "log2+1", "log10+1"]
 * fold_change_cutoff: fold change cutoff
 * feature_set_suffix: Result FeatureSet object name suffix
 * filtered_expression_matrix_suffix: Result ExpressionMatrix object name suffix
 * workspace_name: the name of the workspace it gets saved to
 * run_all_combinations: run all paired condition combinations (default true)
 * or
 * condition_labels: conditions for expression set object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "diff_expression_ref",
    "expression_matrix_ref",
    "p_cutoff",
    "q_cutoff",
    "fold_scale_type",
    "fold_change_cutoff",
    "feature_set_suffix",
    "filtered_expression_matrix_suffix",
    "workspace_name",
    "run_all_combinations",
    "condition_labels"
})
public class UploadFeatureSetFromDiffExprInput {

    @JsonProperty("diff_expression_ref")
    private java.lang.String diffExpressionRef;
    @JsonProperty("expression_matrix_ref")
    private java.lang.String expressionMatrixRef;
    @JsonProperty("p_cutoff")
    private Double pCutoff;
    @JsonProperty("q_cutoff")
    private Double qCutoff;
    @JsonProperty("fold_scale_type")
    private java.lang.String foldScaleType;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    @JsonProperty("feature_set_suffix")
    private java.lang.String featureSetSuffix;
    @JsonProperty("filtered_expression_matrix_suffix")
    private java.lang.String filteredExpressionMatrixSuffix;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("run_all_combinations")
    private Long runAllCombinations;
    @JsonProperty("condition_labels")
    private List<String> conditionLabels;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("diff_expression_ref")
    public java.lang.String getDiffExpressionRef() {
        return diffExpressionRef;
    }

    @JsonProperty("diff_expression_ref")
    public void setDiffExpressionRef(java.lang.String diffExpressionRef) {
        this.diffExpressionRef = diffExpressionRef;
    }

    public UploadFeatureSetFromDiffExprInput withDiffExpressionRef(java.lang.String diffExpressionRef) {
        this.diffExpressionRef = diffExpressionRef;
        return this;
    }

    @JsonProperty("expression_matrix_ref")
    public java.lang.String getExpressionMatrixRef() {
        return expressionMatrixRef;
    }

    @JsonProperty("expression_matrix_ref")
    public void setExpressionMatrixRef(java.lang.String expressionMatrixRef) {
        this.expressionMatrixRef = expressionMatrixRef;
    }

    public UploadFeatureSetFromDiffExprInput withExpressionMatrixRef(java.lang.String expressionMatrixRef) {
        this.expressionMatrixRef = expressionMatrixRef;
        return this;
    }

    @JsonProperty("p_cutoff")
    public Double getPCutoff() {
        return pCutoff;
    }

    @JsonProperty("p_cutoff")
    public void setPCutoff(Double pCutoff) {
        this.pCutoff = pCutoff;
    }

    public UploadFeatureSetFromDiffExprInput withPCutoff(Double pCutoff) {
        this.pCutoff = pCutoff;
        return this;
    }

    @JsonProperty("q_cutoff")
    public Double getQCutoff() {
        return qCutoff;
    }

    @JsonProperty("q_cutoff")
    public void setQCutoff(Double qCutoff) {
        this.qCutoff = qCutoff;
    }

    public UploadFeatureSetFromDiffExprInput withQCutoff(Double qCutoff) {
        this.qCutoff = qCutoff;
        return this;
    }

    @JsonProperty("fold_scale_type")
    public java.lang.String getFoldScaleType() {
        return foldScaleType;
    }

    @JsonProperty("fold_scale_type")
    public void setFoldScaleType(java.lang.String foldScaleType) {
        this.foldScaleType = foldScaleType;
    }

    public UploadFeatureSetFromDiffExprInput withFoldScaleType(java.lang.String foldScaleType) {
        this.foldScaleType = foldScaleType;
        return this;
    }

    @JsonProperty("fold_change_cutoff")
    public Double getFoldChangeCutoff() {
        return foldChangeCutoff;
    }

    @JsonProperty("fold_change_cutoff")
    public void setFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
    }

    public UploadFeatureSetFromDiffExprInput withFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
        return this;
    }

    @JsonProperty("feature_set_suffix")
    public java.lang.String getFeatureSetSuffix() {
        return featureSetSuffix;
    }

    @JsonProperty("feature_set_suffix")
    public void setFeatureSetSuffix(java.lang.String featureSetSuffix) {
        this.featureSetSuffix = featureSetSuffix;
    }

    public UploadFeatureSetFromDiffExprInput withFeatureSetSuffix(java.lang.String featureSetSuffix) {
        this.featureSetSuffix = featureSetSuffix;
        return this;
    }

    @JsonProperty("filtered_expression_matrix_suffix")
    public java.lang.String getFilteredExpressionMatrixSuffix() {
        return filteredExpressionMatrixSuffix;
    }

    @JsonProperty("filtered_expression_matrix_suffix")
    public void setFilteredExpressionMatrixSuffix(java.lang.String filteredExpressionMatrixSuffix) {
        this.filteredExpressionMatrixSuffix = filteredExpressionMatrixSuffix;
    }

    public UploadFeatureSetFromDiffExprInput withFilteredExpressionMatrixSuffix(java.lang.String filteredExpressionMatrixSuffix) {
        this.filteredExpressionMatrixSuffix = filteredExpressionMatrixSuffix;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public UploadFeatureSetFromDiffExprInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("run_all_combinations")
    public Long getRunAllCombinations() {
        return runAllCombinations;
    }

    @JsonProperty("run_all_combinations")
    public void setRunAllCombinations(Long runAllCombinations) {
        this.runAllCombinations = runAllCombinations;
    }

    public UploadFeatureSetFromDiffExprInput withRunAllCombinations(Long runAllCombinations) {
        this.runAllCombinations = runAllCombinations;
        return this;
    }

    @JsonProperty("condition_labels")
    public List<String> getConditionLabels() {
        return conditionLabels;
    }

    @JsonProperty("condition_labels")
    public void setConditionLabels(List<String> conditionLabels) {
        this.conditionLabels = conditionLabels;
    }

    public UploadFeatureSetFromDiffExprInput withConditionLabels(List<String> conditionLabels) {
        this.conditionLabels = conditionLabels;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((("UploadFeatureSetFromDiffExprInput"+" [diffExpressionRef=")+ diffExpressionRef)+", expressionMatrixRef=")+ expressionMatrixRef)+", pCutoff=")+ pCutoff)+", qCutoff=")+ qCutoff)+", foldScaleType=")+ foldScaleType)+", foldChangeCutoff=")+ foldChangeCutoff)+", featureSetSuffix=")+ featureSetSuffix)+", filteredExpressionMatrixSuffix=")+ filteredExpressionMatrixSuffix)+", workspaceName=")+ workspaceName)+", runAllCombinations=")+ runAllCombinations)+", conditionLabels=")+ conditionLabels)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
