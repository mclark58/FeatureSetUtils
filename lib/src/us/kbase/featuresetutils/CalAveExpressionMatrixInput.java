
package us.kbase.featuresetutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CalAveExpressionMatrixInput</p>
 * <pre>
 * required params:
 * expression_matrix_ref: ExpressionMatrix object reference
 * output_suffix: output average ExpressionMatrix name suffix
 * workspace_name: the name of the workspace it gets saved to
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "expression_matrix_ref",
    "output_suffix",
    "workspace_name"
})
public class CalAveExpressionMatrixInput {

    @JsonProperty("expression_matrix_ref")
    private String expressionMatrixRef;
    @JsonProperty("output_suffix")
    private String outputSuffix;
    @JsonProperty("workspace_name")
    private String workspaceName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("expression_matrix_ref")
    public String getExpressionMatrixRef() {
        return expressionMatrixRef;
    }

    @JsonProperty("expression_matrix_ref")
    public void setExpressionMatrixRef(String expressionMatrixRef) {
        this.expressionMatrixRef = expressionMatrixRef;
    }

    public CalAveExpressionMatrixInput withExpressionMatrixRef(String expressionMatrixRef) {
        this.expressionMatrixRef = expressionMatrixRef;
        return this;
    }

    @JsonProperty("output_suffix")
    public String getOutputSuffix() {
        return outputSuffix;
    }

    @JsonProperty("output_suffix")
    public void setOutputSuffix(String outputSuffix) {
        this.outputSuffix = outputSuffix;
    }

    public CalAveExpressionMatrixInput withOutputSuffix(String outputSuffix) {
        this.outputSuffix = outputSuffix;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CalAveExpressionMatrixInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("CalAveExpressionMatrixInput"+" [expressionMatrixRef=")+ expressionMatrixRef)+", outputSuffix=")+ outputSuffix)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
