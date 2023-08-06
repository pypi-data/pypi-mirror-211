#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import types
import boto3
from infra_operator.clients.ghe import GHE


def get_account_id(self):
    return self.get_caller_identity()["Account"]


def find_distribution(self, Id=None, Alias=None, DomainName=None):
    if Id is None:
        pager = self.get_paginator("list_distributions")
        matched = []
        for res in pager.paginate():
            for dist in res["DistributionList"]["Items"]:
                if DomainName is None:
                    if Alias in dist["Aliases"].get("Items", []):
                        matched.append(dist)
                else:
                    if dist["DomainName"] == DomainName:
                        matched.append(dist)
        if len(matched) == 1:
            Id = matched[0]["Id"]
        elif len(matched) == 0:
            return None
        else:
            raise Exception(
                f"found {len(matched)} distribution with Alias: {Alias}. please specify by Id")
    res = self.get_distribution(Id=Id)
    res["Distribution"]["DistributionConfig"]["Id"] = Id
    res["Distribution"]["DistributionConfig"]["ETag"] = res["ETag"]
    res["Distribution"]["DistributionConfig"]["DomainName"] = res["Distribution"]["DomainName"]
    return res


def list_continuous_deployment_policies_(self):
    res = self.list_continuous_deployment_policies()
    marker = res["ContinuousDeploymentPolicyList"]
    marker = None
    while True:
        if marker:
            res = self.list_continuous_deployment_policies(Marker=marker)
        else:
            res = self.list_continuous_deployment_policies()
        marker = res["ContinuousDeploymentPolicyList"].get("NextMarker")
        for one in res["ContinuousDeploymentPolicyList"]["Items"]:
            one["ContinuousDeploymentPolicy"]["ContinuousDeploymentPolicyConfig"]["Id"] = one["ContinuousDeploymentPolicy"]["Id"]
            yield one["ContinuousDeploymentPolicy"]["ContinuousDeploymentPolicyConfig"]
        if marker is None:
            break


def try_get_continuous_deployment_policy(self, Id=None, StagingDistributionDnsNames=None):
    if Id is None:
        for one in self.list_continuous_deployment_policies_():
            if set(one["StagingDistributionDnsNames"]["Items"]) == set(StagingDistributionDnsNames):
                Id = one["Id"]
                break
    if Id:
        return self.get_continuous_deployment_policy(Id=Id)


def list_cache_policies_(self):
    marker = None
    while True:
        if marker:
            res = self.list_cache_policies(Marker=marker)
        else:
            res = self.list_cache_policies()
        marker = res["CachePolicyList"].get("NextMarker")
        for one in res["CachePolicyList"]["Items"]:
            one["CachePolicy"]["CachePolicyConfig"]["Id"] = one["CachePolicy"]["Id"]
            yield one["CachePolicy"]["CachePolicyConfig"]
        if marker is None:
            break


def find_cache_policy(self, Id=None, Name=None):
    if Id is None:
        cache_policies = list(self.list_cache_policies_())
        res = [one for one in cache_policies if one["Name"] == Name]
        if len(res) == 0:
            return None
        Id = res[0]["Id"]
    result = self.get_cache_policy(Id=Id)
    if result is None:
        return None
    Id = result["CachePolicy"]["Id"]
    config = result["CachePolicy"]["CachePolicyConfig"]
    config["Id"] = Id
    config["ETag"] = result["ETag"]
    return config


cloudfront = boto3.client('cloudfront')
cloudfront.find_distribution = types.MethodType(find_distribution, cloudfront)
cloudfront.list_cache_policies_ = types.MethodType(
    list_cache_policies_, cloudfront)
cloudfront.find_cache_policy = types.MethodType(find_cache_policy, cloudfront)
cloudfront.list_continuous_deployment_policies_ = types.MethodType(
    list_continuous_deployment_policies_, cloudfront)
cloudfront.try_get_continuous_deployment_policy = types.MethodType(
    try_get_continuous_deployment_policy, cloudfront)

sts = boto3.client("sts")
sts.get_account_id = types.MethodType(get_account_id, sts)


def find_instance(this, InstanceId, Name):
    if InstanceId:
        return this.describe_instances(InstanceIds=[InstanceId])
    else:
        return this.describe_instances(Filters=[{
            'Name': 'tag:Name',
            'Values': [Name]
        }])


def find_volume(this, VolumeId=None, Name=None):
    if VolumeId:
        return this.describe_volumes(VolumeIds=[VolumeId])
    else:
        return this.describe_volumes(Filters=[{
            'Name': 'tag:Name',
            'Values': [Name]
        }])


def find_launch_template(this, LaunchTemplateId=None, LaunchTemplateName=None):
    if LaunchTemplateId:
        return this.describe_launch_templates(LaunchTemplateIds=[LaunchTemplateId])
    else:
        return this.describe_launch_templates(LaunchTemplateNames=[LaunchTemplateName])


def update_instance(this, content, current):
    fields = [
        "SourceDestCheck",
        "Attribute",
        "BlockDeviceMappings",
        "DisableApiTermination",
        "EbsOptimized",
        "EnaSupport",
        "Groups",
        "InstanceId",
        "InstanceInitiatedShutdownBehavior",
        "InstanceType",
        "Kernel",
        "Ramdisk",
        "SriovNetSupport",
        "UserData",
        "Value",
        "DisableApiStop",
    ]
    for field in fields:
        pass


ec2 = boto3.client("ec2")
ec2.find_instance = types.MethodType(find_instance, ec2)
ec2.find_volume = types.MethodType(find_volume, ec2)
ec2.find_launch_template = types.MethodType(find_launch_template, ec2)


def find_repository(this, registryId, repositoryName):
    if registryId:
        return this.describe_repositories(registryId=registryId, repositoryNames=[repositoryName])
    else:
        return this.describe_repositories(repositoryNames=[repositoryName])


ecr = boto3.client('ecr')
ecr.find_repository = types.MethodType(find_repository, ecr)

clients = {
    "ecr":
    ecr,
    "ecs":
    boto3.client('ecs'),
    "elbv2":
    boto3.client("elbv2"),
    "ec2": ec2,
    "iam":
    boto3.client("iam"),
    "appmesh":
    boto3.client("appmesh"),
    "servicediscovery":
    boto3.client("servicediscovery"),
    "secretsmanager":
    boto3.client("secretsmanager"),
    "ghe":
    GHE(base_url="https://git.toolsfdg.net/api/v3",
        login_or_token=os.getenv('GITHUB_TOKEN')),
    "application-autoscaling":
        boto3.client("application-autoscaling"),
    "sqs":
        boto3.resource('sqs'),
    "lambda":
        boto3.client('lambda'),
    "asg":
        boto3.client('autoscaling'),
    "cloudwatch":
        boto3.client('cloudwatch'),
    "cloudfront":
        cloudfront,
    "sts":
        sts,
}
