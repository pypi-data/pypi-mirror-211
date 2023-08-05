from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

APIRateLimit: Code
AuthStrategyRuleExisted: Code
AuthTokenForbidden: Code
BadRequest: Code
BatchSizeOverLimit: Code
CMDBNotFindHost: Code
CMDBPluginException: Code
CircuitBreakerRuleExisted: Code
ClientAPINotOpen: Code
DESCRIPTOR: _descriptor.FileDescriptor
DataConflict: Code
DataNoChange: Code
DecryptConfigFileException: Code
EmptyAutToken: Code
EmptyQueryParameter: Code
EmptyRequest: Code
EncryptConfigFileException: Code
ExecuteException: Code
ExecuteSuccess: Code
ExistReleasedConfig: Code
ExistedResource: Code
FaultDetectRuleExisted: Code
HealthCheckNotOpen: Code
HeartbeatExceedLimit: Code
HeartbeatException: Code
HeartbeatOnDisabledIns: Code
HeartbeatTypeNotFound: Code
IPRateLimit: Code
InstanceRegisTimeout: Code
InstanceTooManyRequests: Code
InvalidAuthStrategyID: Code
InvalidAuthStrategyName: Code
InvalidAuthStrategyOwners: Code
InvalidCircuitBreakerBusiness: Code
InvalidCircuitBreakerComment: Code
InvalidCircuitBreakerDepartment: Code
InvalidCircuitBreakerID: Code
InvalidCircuitBreakerName: Code
InvalidCircuitBreakerNamespace: Code
InvalidCircuitBreakerOwners: Code
InvalidCircuitBreakerToken: Code
InvalidCircuitBreakerVersion: Code
InvalidConfigFileContentLength: Code
InvalidConfigFileFormat: Code
InvalidConfigFileGroupName: Code
InvalidConfigFileName: Code
InvalidConfigFileTags: Code
InvalidConfigFileTemplateName: Code
InvalidDiscoverResource: Code
InvalidFaultDetectID: Code
InvalidFaultDetectName: Code
InvalidFaultDetectNamespace: Code
InvalidFluxRateLimitId: Code
InvalidFluxRateLimitQps: Code
InvalidFluxRateLimitSetKey: Code
InvalidInstanceHost: Code
InvalidInstanceID: Code
InvalidInstanceIsolate: Code
InvalidInstanceLogicSet: Code
InvalidInstancePort: Code
InvalidInstanceProtocol: Code
InvalidInstanceVersion: Code
InvalidMeshParameter: Code
InvalidMetadata: Code
InvalidNamespaceName: Code
InvalidNamespaceOwners: Code
InvalidNamespaceToken: Code
InvalidNamespaceWithAlias: Code
InvalidParameter: Code
InvalidPlatformComment: Code
InvalidPlatformDepartment: Code
InvalidPlatformDomain: Code
InvalidPlatformID: Code
InvalidPlatformName: Code
InvalidPlatformOwner: Code
InvalidPlatformQPS: Code
InvalidPlatformToken: Code
InvalidPrincipalType: Code
InvalidQueryInsParameter: Code
InvalidRateLimitAmounts: Code
InvalidRateLimitID: Code
InvalidRateLimitLabels: Code
InvalidRateLimitName: Code
InvalidRequestID: Code
InvalidRoutingID: Code
InvalidRoutingName: Code
InvalidRoutingPolicy: Code
InvalidRoutingPriority: Code
InvalidServiceAlias: Code
InvalidServiceAliasComment: Code
InvalidServiceAliasOwners: Code
InvalidServiceBusiness: Code
InvalidServiceCMDB: Code
InvalidServiceComment: Code
InvalidServiceDepartment: Code
InvalidServiceMetadata: Code
InvalidServiceName: Code
InvalidServiceOwners: Code
InvalidServicePorts: Code
InvalidServiceToken: Code
InvalidUserEmail: Code
InvalidUserGroupID: Code
InvalidUserGroupOwners: Code
InvalidUserID: Code
InvalidUserMobile: Code
InvalidUserName: Code
InvalidUserOwners: Code
InvalidUserPassword: Code
InvalidUserToken: Code
InvalidWatchConfigFileFormat: Code
NamespaceExistedCircuitBreakers: Code
NamespaceExistedConfigGroups: Code
NamespaceExistedMeshResources: Code
NamespaceExistedServices: Code
NoNeedUpdate: Code
NotAllowAliasBindRule: Code
NotAllowAliasCreateInstance: Code
NotAllowAliasCreateRateLimit: Code
NotAllowAliasCreateRouting: Code
NotAllowAliasUpdate: Code
NotAllowBusinessService: Code
NotAllowCreateAliasForAlias: Code
NotAllowDifferentNamespaceBindRule: Code
NotAllowModifyDefaultStrategyPrincipal: Code
NotAllowModifyOwnerDefaultStrategy: Code
NotAllowedAccess: Code
NotFoundAuthStrategyRule: Code
NotFoundCircuitBreaker: Code
NotFoundInstance: Code
NotFoundMasterConfig: Code
NotFoundNamespace: Code
NotFoundOwnerUser: Code
NotFoundPlatform: Code
NotFoundRateLimit: Code
NotFoundResource: Code
NotFoundResourceConfigFile: Code
NotFoundRouting: Code
NotFoundService: Code
NotFoundServiceAlias: Code
NotFoundSourceService: Code
NotFoundTagConfig: Code
NotFoundTagConfigOrService: Code
NotFoundUser: Code
NotFoundUserGroup: Code
OperationRoleForbidden: Code
ParseCircuitBreakerException: Code
ParseException: Code
ParseRateLimitException: Code
ParseRoutingException: Code
ResourcesExistedMesh: Code
SameInstanceRequest: Code
ServiceExistedAlias: Code
ServiceExistedCircuitBreakers: Code
ServiceExistedFluxRateLimits: Code
ServiceExistedInstances: Code
ServiceExistedRateLimits: Code
ServiceExistedRoutings: Code
ServiceSubscribedByMeshes: Code
ServicesExistedMesh: Code
StoreLayerException: Code
SubAccountExisted: Code
TokenDisabled: Code
TokenNotExisted: Code
Unauthorized: Code
Unknown: Code
UserExisted: Code
UserGroupExisted: Code

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
