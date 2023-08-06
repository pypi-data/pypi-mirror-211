

allow_api_versions = [
    "wafv2.aws.infra/v1alpha1",
    "elbv2.aws.infra/v1alpha1",
    "ec2.aws.infra/v1alpha1",
    "iam.aws.infra/v1alpha1",
    "repo.ghe.infra/v1alpha1",
    "appmesh.aws.infra/v1alpha1",
    "servicediscovery.aws.infra/v1alpha1",
    "secretsmanager.aws.infra/v1alpha1",
    "anyscale.aws.infra/v1alpha1",
    "asg.aws.infra/v1alpha1",
    "sqs.aws.infra/v1alpha1",
    "lambda.aws.infra/v1alpha1",
    "cloudwatch.aws.infra/v1alpha1",
    "cloudfront.aws.infra/v1alpha1",
    "ecs.aws.infra/v1alpha1",
    "ecr.aws.infra/v1alpha1"
]

allow_kinds = [
    "TaskDefinition",
    "TargetGroup",
    "Service",
    "LoadBalancer",
    "SecurityGroup",
    "Role",
    "Repo",
    # appmesh
    "Mesh",
    "VirtualGateway",
    "GatewayRoute",
    "VirtualService",
    "VirtualRouter",
    "VirtualNode",
    "Route",
    # cloud map
    "ServiceDiscoveryService",
    # secretsmanager
    "Secret",
    # ECS sacling
    "ScalingPolicy",
    "ScalableTarget",
    # OSS yarn
    "AutoScalingGroup",
    "Lambda",
    "Queue",
    "LaunchTemplate",
    "LambdaEventSource",
    "LifeCycleHook",
    "Alarm",
    "AutoScalingPolicy",
    "Distribution",
    "CachePolicy",
    "ContinuousDeploymentPolicy",
    "ECS/Cluster",
    "Mesh",
    "Instance",
    "Volume",
    "Repository",
]


def verify(content):
    apiVersion = content.get("apiVersion")
    kind = content.get("kind")
    if apiVersion.replace(".binance/", ".infra/") not in allow_api_versions:
        raise Exception(
            f'Expected apiVersion in {allow_api_versions}\nactual apiVersion: {apiVersion}'
        )
    if kind not in allow_kinds:
        raise Exception(
            f'Expected kind in: {allow_kinds}\nactual kind: {kind}')
    return kind
