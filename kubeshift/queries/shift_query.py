"""Openshift names query APIs."""
from kubeshift.constants import DEFAULT_NAMESPACE
from kubeshift.queries import base


class ShiftQueryMixin(object):
    """Provide Openshift name query APIs."""

    @base.queryapi(version='v1', kind='AppliedClusterResourceQuota', nsarg=True)
    def appliedclusterresourcequotas(self, namespace=DEFAULT_NAMESPACE):
        """Query appliedclusterresourcequotas."""

    @base.queryapi(version='v1', kind='BuildConfig', nsarg=True)
    def buildconfigs(self, namespace=DEFAULT_NAMESPACE):
        """Query buildconfigs."""

    @base.queryapi(version='v1', kind='Build', nsarg=True)
    def builds(self, namespace=DEFAULT_NAMESPACE):
        """Query builds."""

    @base.queryapi(version='v1', kind='ClusterNetwork', nsarg=False)
    def clusternetworks(self):
        """Query clusternetworks."""

    @base.queryapi(version='v1', kind='ClusterPolicy', nsarg=False)
    def clusterpolicies(self):
        """Query clusterpolicies."""

    @base.queryapi(version='v1', kind='ClusterPolicyBinding', nsarg=False)
    def clusterpolicybindings(self):
        """Query clusterpolicybindings."""

    @base.queryapi(version='v1', kind='ClusterResourceQuota', nsarg=False)
    def clusterresourcequotas(self):
        """Query clusterresourcequotas."""

    @base.queryapi(version='v1', kind='ClusterRoleBinding', nsarg=False)
    def clusterrolebindings(self):
        """Query clusterrolebindings."""

    @base.queryapi(version='v1', kind='ClusterRole', nsarg=False)
    def clusterroles(self):
        """Query clusterroles."""

    @base.queryapi(version='v1', kind='DeploymentConfigRollback', nsarg=True)
    def deploymentconfigrollbacks(self, namespace=DEFAULT_NAMESPACE):
        """Query deploymentconfigrollbacks."""

    @base.queryapi(version='v1', kind='DeploymentConfig', nsarg=True)
    def deploymentconfigs(self, namespace=DEFAULT_NAMESPACE):
        """Query deploymentconfigs."""

    @base.queryapi(version='v1', kind='EgressNetworkPolicy', nsarg=True)
    def egressnetworkpolicies(self, namespace=DEFAULT_NAMESPACE):
        """Query egressnetworkpolicies."""

    @base.queryapi(version='v1', kind='Group', nsarg=False)
    def groups(self):
        """Query groups."""

    @base.queryapi(version='v1', kind='HostSubnet', nsarg=False)
    def hostsubnets(self):
        """Query hostsubnets."""

    @base.queryapi(version='v1', kind='Identity', nsarg=False)
    def identities(self):
        """Query identities."""

    @base.queryapi(version='v1', kind='Image', nsarg=False)
    def images(self):
        """Query images."""

    @base.queryapi(version='v1', kind='ImageSignature', nsarg=False)
    def imagesignatures(self):
        """Query imagesignatures."""

    @base.queryapi(version='v1', kind='ImageStreamImage', nsarg=True)
    def imagestreamimages(self, namespace=DEFAULT_NAMESPACE):
        """Query imagestreamimages."""

    @base.queryapi(version='v1', kind='ImageStreamImport', nsarg=True)
    def imagestreamimports(self, namespace=DEFAULT_NAMESPACE):
        """Query imagestreamimports."""

    @base.queryapi(version='v1', kind='ImageStreamMapping', nsarg=True)
    def imagestreammappings(self, namespace=DEFAULT_NAMESPACE):
        """Query imagestreammappings."""

    @base.queryapi(version='v1', kind='ImageStream', nsarg=True)
    def imagestreams(self, namespace=DEFAULT_NAMESPACE):
        """Query imagestreams."""

    @base.queryapi(version='v1', kind='ImageStreamTag', nsarg=True)
    def imagestreamtags(self, namespace=DEFAULT_NAMESPACE):
        """Query imagestreamtags."""

    @base.queryapi(version='v1', kind='LocalResourceAccessReview', nsarg=True)
    def localresourceaccessreviews(self, namespace=DEFAULT_NAMESPACE):
        """Query localresourceaccessreviews."""

    @base.queryapi(version='v1', kind='LocalSubjectAccessReview', nsarg=True)
    def localsubjectaccessreviews(self, namespace=DEFAULT_NAMESPACE):
        """Query localsubjectaccessreviews."""

    @base.queryapi(version='v1', kind='NetNamespace', nsarg=False)
    def netnamespaces(self):
        """Query netnamespaces."""

    @base.queryapi(version='v1', kind='OAuthAccessToken', nsarg=False)
    def oauthaccesstokens(self):
        """Query oauthaccesstokens."""

    @base.queryapi(version='v1', kind='OAuthAuthorizeToken', nsarg=False)
    def oauthauthorizetokens(self):
        """Query oauthauthorizetokens."""

    @base.queryapi(version='v1', kind='OAuthClientAuthorization', nsarg=False)
    def oauthclientauthorizations(self):
        """Query oauthclientauthorizations."""

    @base.queryapi(version='v1', kind='OAuthClient', nsarg=False)
    def oauthclients(self):
        """Query oauthclients."""

    @base.queryapi(version='v1', kind='Policy', nsarg=True)
    def policies(self, namespace=DEFAULT_NAMESPACE):
        """Query policies."""

    @base.queryapi(version='v1', kind='PolicyBinding', nsarg=True)
    def policybindings(self, namespace=DEFAULT_NAMESPACE):
        """Query policybindings."""

    @base.queryapi(version='v1', kind='ProjectRequest', nsarg=False)
    def projectrequests(self):
        """Query projectrequests."""

    @base.queryapi(version='v1', kind='Project', nsarg=False)
    def projects(self):
        """Query projects."""

    @base.queryapi(version='v1', kind='ResourceAccessReview', nsarg=True)
    def resourceaccessreviews(self, namespace=DEFAULT_NAMESPACE):
        """Query resourceaccessreviews."""

    @base.queryapi(version='v1', kind='RoleBinding', nsarg=True)
    def rolebindings(self, namespace=DEFAULT_NAMESPACE):
        """Query rolebindings."""

    @base.queryapi(version='v1', kind='Role', nsarg=True)
    def roles(self, namespace=DEFAULT_NAMESPACE):
        """Query roles."""

    @base.queryapi(version='v1', kind='Route', nsarg=True)
    def routes(self, namespace=DEFAULT_NAMESPACE):
        """Query routes."""

    @base.queryapi(version='v1', kind='SelfSubjectRulesReview', nsarg=True)
    def selfsubjectrulesreviews(self, namespace=DEFAULT_NAMESPACE):
        """Query selfsubjectrulesreviews."""

    @base.queryapi(version='v1', kind='SubjectAccessReview', nsarg=True)
    def subjectaccessreviews(self, namespace=DEFAULT_NAMESPACE):
        """Query subjectaccessreviews."""

    @base.queryapi(version='v1', kind='Template', nsarg=True)
    def templates(self, namespace=DEFAULT_NAMESPACE):
        """Query templates."""

    @base.queryapi(version='v1', kind='UserIdentityMapping', nsarg=False)
    def useridentitymappings(self):
        """Query useridentitymappings."""

    @base.queryapi(version='v1', kind='User', nsarg=False)
    def users(self):
        """Query users."""
