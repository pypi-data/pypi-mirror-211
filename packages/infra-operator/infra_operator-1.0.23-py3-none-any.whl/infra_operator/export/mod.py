import re
from copy import deepcopy
from infra_operator.operators.mod import enabled_disabled_to_bool, lift_field, list_to_args_overwrite, list_to_tags, map_nested_field,  remove_empty_list, remove_field, remove_fields, remove_fields_recursive, remove_inner_fields, remove_items_quantity, rename_fields, sort_field_by, spec_to_meta, template_fields, to_crd
from infra_operator.clients.mod import clients
from infra_operator.read.mod import get_resource


def cloudfront_export_tags(crd):
    kind = crd["kind"].lower()
    if kind not in set(["distribution"]):
        return crd
    account_id = clients["sts"].get_caller_identity()["Account"]
    id = crd["metadata"]["Id"]
    res = clients["cloudfront"].list_tags_for_resource(
        Resource=f"arn:aws:cloudfront::{account_id}:{kind}/{id}")
    tags = list_to_tags(res["Tags"]["Items"])
    crd["metadata"]["Tags"] = tags
    return crd


def tidy_tags(crd, capitalize=True):
    key = "Tags" if capitalize else "tags"
    crd = spec_to_meta(key)(crd)
    if key in crd["metadata"]:
        crd["metadata"][key] = list_to_tags(crd["metadata"][key], capitalize)
    return crd


def tidy_attributes(crd):
    crd = spec_to_meta("Attributes")(crd)
    crd["metadata"]["Attributes"] = list_to_tags(crd["metadata"]["Attributes"])
    return crd


def role_tidy(content):
    content["inline-policies"] = remove_inner_fields(
        ["RoleName"])(content["inline-policies"])
    content["managed-policies"] = remove_inner_fields(
        ["RoleName"])(content["managed-policies"])
    return content


def transform_subnets(content):
    content["Subnets"] = list(
        map(lambda one: one["SubnetId"], content["AvailabilityZones"]))
    del content["AvailabilityZones"]
    return content


def export(kind, current, info):
    switch = {"Repo": [remove_fields(["metadata"])],
              "Distribution": [remove_items_quantity,
                               remove_fields(["ETag", "DomainName"]),
                               lambda tidied: template_fields(
                                   deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                               lambda content: to_crd(
                                   content, "cloudfront.aws.infra/v1alpha1", "Distribution"),
                               cloudfront_export_tags],
              "CachePolicy": [remove_items_quantity,
                              remove_field("ETag"),
                              lambda content: to_crd(
                                  content, "cloudfront.aws.infra/v1alpha1", "CachePolicy"),
                              cloudfront_export_tags
                              ],
              "ContinuousDeploymentPolicy": [remove_items_quantity,
                                             remove_field("ETag"),
                                             lambda content: to_crd(
                                                 content, "cloudfront.aws.infra/v1alpha1", "ContinuousDeploymentPolicy"),
                                             cloudfront_export_tags
                                             ],
              "LoadBalancer": [remove_fields(["LoadBalancerArn", "DNSName", "CanonicalHostedZoneId", "CreatedTime", "State"]),
                               remove_fields_recursive(
                                   ["ListenerArn", "RuleArn"]),
                               transform_subnets,
                               rename_fields({"LoadBalancerName": "Name"}),
                               remove_items_quantity,
                               sort_field_by(["Listeners"],
                                             lambda one: (one["Protocol"], one["Port"])),
                               sort_field_by(["Listeners", list, "Rules"],
                                             lambda one: one["Priority"]),
                               sort_field_by(["Listeners", list, "Rules", list, "Conditions"],
                                             lambda one: one["Field"]),
                               lambda content: to_crd(
                                   content, "elbv2.aws.infra/v1alpha1", "LoadBalancer"),
                               tidy_tags,
                               tidy_attributes,
                               ],
              "SecurityGroup": [remove_fields(["Rules", "OwnerId", "GroupId"]),
                                rename_fields(
                                    {"IpPermissions": "ingress", "IpPermissionsEgress": "egress"}),
                                remove_empty_list,
                                lambda content: to_crd(
                                    content, "ec2.aws.infra/v1alpha1", "SecurityGroup"),
                                tidy_tags,
                                ],
              "Role": [remove_fields(["RoleId", "Arn", "CreateDate", "RoleLastUsed"]),
                       role_tidy,
                       lambda content: to_crd(
                           content, "iam.aws.infra/v1alpha1", "Role"),
                       spec_to_meta("AssumeRolePolicyDocument"),
                       tidy_tags],
              "TargetGroup": [remove_fields(["LoadBalancerArns", "TargetGroupArn", "IpAddressType", "ProtocolVersion"]),
                              rename_fields({"TargetGroupName": "Name"}),
                              lambda content: to_crd(
                                  content, "elbv2.aws.infra/v1alpha1", "TargetGroup"),
                              tidy_tags,
                              ],
              "ECS/Cluster": [remove_fields(["status", "clusterArn", "runningTasksCount", "pendingTasksCount", "activeServicesCount", "registeredContainerInstancesCount"]),
                              remove_empty_list,
                              lambda content: to_crd(
                                  content, "ecs.aws.infra/v1alpha1", "ECS/Cluster"),
                              lambda crd: tidy_tags(crd, False),
                              ],
              "Instance": [remove_fields(["VpcId", "Hypervisor", "Architecture", "PublicDnsName", "PrivateDnsName", "PrivateDnsName",
                                          "RootDeviceName", "RootDeviceType", "UsageOperation", "LaunchTime", "UsageOperationUpdateTime",
                                          "PrivateIpAddress", "VirtualizationType", "StateTransitionReason", "EnaSupport",
                                          "SourceDestCheck", "AmiLaunchIndex", [
                                              "IamInstanceProfile", "Id"], "State", "CpuOptions", "SecurityGroups",
                                          "MetadataOptions", "NetworkInterfaces", "PlatformDetails",
                                          "ClientToken"
                                          ]),
                           map_nested_field(
                               ["Monitoring", "State"], enabled_disabled_to_bool),
                           rename_fields(
                               [(["Monitoring", "State"], "Enabled")]),
                           remove_empty_list,
                           lambda content: to_crd(
                               content, "ec2.aws.infra/v1alpha1", "Instance"),
                           lambda crd: tidy_tags(crd, True),
                           ],
              "Service": [remove_fields(["events", "status", "createdAt", "deployments", "roleArn", "createdBy", "serviceArn", "clusterArn", "runningCount", "pendingCount", "platformFamily"]),
                          remove_empty_list,
                          sort_field_by(
                              ["networkConfiguration", "awsvpcConfiguration", "subnets"], lambda one: one),
                          lambda content: to_crd(
                              content, "ecs.aws.infra/v1alpha1", "Service"),
                          tidy_tags,
                          ],
              "TaskDefinition": [remove_fields(["status", "registeredBy", "taskDefinitionArn", "revision", "registeredAt", "compatibilities", "requiresAttributes"]),
                                 remove_empty_list,
                                 lambda content: to_crd(
                                     content, "ecs.aws.infra/v1alpha1", "TaskDefinition"),
                                 tidy_tags,
                                 ],
              "Mesh": [remove_fields(["metadata", "status"]),
                       remove_empty_list,
                       lift_field("spec"),
                       lambda content: to_crd(
                           content, "appmesh.aws.infra/v1alpha1", "Mesh"),
                       tidy_tags,
                       ],
              "VirtualGateway": [remove_fields(["metadata", "status"]),
                                 remove_empty_list,
                                 lift_field("spec"),
                                 lambda content: to_crd(
                                     content, "appmesh.aws.infra/v1alpha1", "VirtualGateway"),
                                 tidy_tags,
                                 ],
              "GatewayRoute": [remove_fields(["metadata", "status"]),
                               remove_empty_list,
                               lift_field("spec"),
                               lambda content: to_crd(
                                   content, "appmesh.aws.infra/v1alpha1", "GatewayRoute"),
                               tidy_tags,
                               ],
              "VirtualNode": [remove_fields(["metadata", "status"]),
                              remove_empty_list,
                              lift_field("spec"),
                              lambda content: to_crd(
                                  content, "appmesh.aws.infra/v1alpha1", "VirtualNode"),
                              tidy_tags,
                              ],
              "VirtualRouter": [remove_fields(["metadata", "status"]),
                                remove_empty_list,
                                lift_field("spec"),
                                lambda content: to_crd(
                                    content, "appmesh.aws.infra/v1alpha1", "VirtualRouter"),
                                tidy_tags,
                                ],
              "VirtualService": [remove_fields(["metadata", "status"]),
                                 remove_empty_list,
                                 lift_field("spec"),
                                 lambda content: to_crd(
                                     content, "appmesh.aws.infra/v1alpha1", "VirtualService"),
                                 tidy_tags,
                                 ],
              "Repository": [remove_fields(["repositoryArn", "repositoryUri", "createdAt"]),
                             lambda content: to_crd(
                                 content, "ecr.aws.infra/v1alpha1", "Repository"),
                             tidy_tags,
                             ],
              "Volume": [remove_fields(["State", "CreateTime", "Attachments"]),
                         lambda content: to_crd(
                             content, "ec2.aws.infra/v1alpha1", "Volume"),
                         tidy_tags,
                         ],
              "Secret": [remove_fields(["ARN", "VersionId", "VersionStages", "CreatedDate", "DeletedDate", "LastAccessedDate", "LastChangedDate", "LastRotatedDate", "RotationEnabled", "RotationLambdaARN", "RotationRules"]),
                         lambda content: to_crd(
                             content, "secretsmanager.aws.infra/v1alpha1", "Secret"),
                         tidy_tags,
                         ],
              "LaunchTemplate": [remove_fields(["CreatedBy", "LatestVersionNumber", "CreateTime"]),
                                 map_nested_field(
                                     ["LaunchTemplateData", "TagSpecifications", list, "Tags"], list_to_args_overwrite),
                                 lambda content: to_crd(
                  content, "ec2.aws.binance/v1alpha1", "LaunchTemplate"),
        tidy_tags,
    ],
    }
    for func in switch[kind]:
        current = func(current)
    return current


def collect_cache_policy_id_(acc, content, info):
    if type(content) == dict:
        v = content.get("CachePolicyId")
        if v is not None and re.match(r"^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", v):
            copied = deepcopy(info)
            copied["cloudfront_type"] = "CachePolicy"
            acc[v] = ("CachePolicy", {"metadata": {"Id": v}}, copied)
        for k, v in content.items():
            collect_cache_policy_id_(acc, v, info)
    elif type(content) == list:
        for one in content:
            collect_cache_policy_id_(acc, one, info)


def collect_mesh_gateways(refs, info):
    def wrap(content):
        meshName = content["metadata"]["meshName"]
        result = get_resource({
            "metadata": {"meshName": meshName}}, "VirtualGateways", {})
        for one in result:
            copied = deepcopy(info)
            copied["appmesh_type"] = "VirtualGateway"
            refs[one["virtualGatewayName"]] = ("VirtualGateway",
                                               {"metadata": {
                                                   "meshName": meshName,
                                                   "virtualGatewayName": one["virtualGatewayName"]}},
                                               copied)
    return wrap


def collect_cache_policy_id(refs, info):
    def wrap(content):
        collect_cache_policy_id_(refs, content, info)
        return content
    return wrap


def collect_continuous_deployment_policy_id(refs, info):
    def remove_staging(str):
        return re.sub(r"\.staging(\.\d+)?", "", str)

    def wrap(content):
        v = content["ContinuousDeploymentPolicyId"]
        if re.match(r"^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", v):
            copied = deepcopy(info)
            copied["cloudfront_type"] = "ContinuousDeploymentPolicy"
            copied["refed_filename"] = remove_staging(copied["name"])
            refs[v] = ("ContinuousDeploymentPolicy", {
                "metadata": {"Id": v}}, copied)
        return content
    return wrap


def collect_cloudfront_domain(refs, info):
    def wrap(content):
        domains = content["StagingDistributionDnsNames"]["Items"]
        for i, domain in enumerate(domains):
            if re.match(r"^\w+\.cloudfront\.net$", domain):
                copied = deepcopy(info)
                copied["cloudfront_type"] = "Distribution"
                n = f".{i}" if i != 0 else ""
                copied["refed_filename"] = f'{copied["name"]}.staging{n}'
                copied["ref_template"] = "$file({}, DomainName)"
                refs[domain] = ("Distribution", {
                    "metadata": {"DomainName": domain}}, copied)
        return content
    return wrap


def export_ref(kind, current, info):
    refs = {}
    switch = {
        "Distribution": [collect_cache_policy_id(refs, info),
                         collect_continuous_deployment_policy_id(refs, info),
                         remove_items_quantity,
                         remove_fields(["ETag", "DomainName"]),
                         lambda tidied: template_fields(
                             deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                         lambda content: to_crd(
                             content, "cloudfront.aws.infra/v1alpha1", "Distribution"),
                         cloudfront_export_tags],
        "ContinuousDeploymentPolicy": [collect_cloudfront_domain(refs, info),
                                       remove_items_quantity,
                                       remove_field("ETag"),
                                       lambda content: to_crd(
                                           content, "cloudfront.aws.infra/v1alpha1", "ContinuousDeploymentPolicy"),
                                       cloudfront_export_tags
                                       ],
        "Mesh": [lambda current: export(kind, current, info),
                 collect_mesh_gateways(refs, info),
                 ],
    }
    if kind in switch:
        for func in switch[kind]:
            current = func(current)
        return refs, current
    else:
        return {}, export(kind, current, info)
