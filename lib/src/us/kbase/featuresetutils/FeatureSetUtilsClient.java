package us.kbase.featuresetutils;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: FeatureSetUtils</p>
 * <pre>
 * A KBase module: FeatureSetUtils
 * </pre>
 */
public class FeatureSetUtilsClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public FeatureSetUtilsClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public FeatureSetUtilsClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public FeatureSetUtilsClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public FeatureSetUtilsClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: upload_featureset_from_diff_expr</p>
     * <pre>
     * upload_featureset_from_diff_expr: create a FeatureSet object from a RNASeqDifferentialExpression object
     * </pre>
     * @param   params   instance of type {@link us.kbase.featuresetutils.UploadFeatureSetFromDiffExprInput UploadFeatureSetFromDiffExprInput}
     * @return   parameter "returnVal" of type {@link us.kbase.featuresetutils.UploadFeatureSetFromDiffExprResult UploadFeatureSetFromDiffExprResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public UploadFeatureSetFromDiffExprResult uploadFeaturesetFromDiffExpr(UploadFeatureSetFromDiffExprInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<UploadFeatureSetFromDiffExprResult>> retType = new TypeReference<List<UploadFeatureSetFromDiffExprResult>>() {};
        List<UploadFeatureSetFromDiffExprResult> res = caller.jsonrpcCall("FeatureSetUtils.upload_featureset_from_diff_expr", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: calculate_average_expression_matrix</p>
     * <pre>
     * calculate_average_expression_matrix: create an average ExpressionMatrix object from a ExpressionMatrix object
     * </pre>
     * @param   params   instance of type {@link us.kbase.featuresetutils.CalAveExpressionMatrixInput CalAveExpressionMatrixInput}
     * @return   parameter "returnVal" of type {@link us.kbase.featuresetutils.CalAveExpressionMatrixResult CalAveExpressionMatrixResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public CalAveExpressionMatrixResult calculateAverageExpressionMatrix(CalAveExpressionMatrixInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<CalAveExpressionMatrixResult>> retType = new TypeReference<List<CalAveExpressionMatrixResult>>() {};
        List<CalAveExpressionMatrixResult> res = caller.jsonrpcCall("FeatureSetUtils.calculate_average_expression_matrix", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: featureset_to_tsv_file</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.featuresetutils.FeatureSetToFileParams FeatureSetToFileParams}
     * @return   parameter "files" of type {@link us.kbase.featuresetutils.FeatureSetTsvFiles FeatureSetTsvFiles}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public FeatureSetTsvFiles featuresetToTsvFile(FeatureSetToFileParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<FeatureSetTsvFiles>> retType = new TypeReference<List<FeatureSetTsvFiles>>() {};
        List<FeatureSetTsvFiles> res = caller.jsonrpcCall("FeatureSetUtils.featureset_to_tsv_file", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_featureset_as_tsv_file</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.featuresetutils.ExportParams ExportParams}
     * @return   parameter "output" of type {@link us.kbase.featuresetutils.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportFeaturesetAsTsvFile(ExportParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("FeatureSetUtils.export_featureset_as_tsv_file", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("FeatureSetUtils.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
