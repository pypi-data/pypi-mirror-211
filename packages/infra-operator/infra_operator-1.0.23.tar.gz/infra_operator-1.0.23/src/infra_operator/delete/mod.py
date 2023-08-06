from infra_operator.clients.mod import clients
from infra_operator.create.aws_appmesh import AppMeshController
from infra_operator.create.mod import ECSServiceController
from infra_operator.delete import aws_iam_delete
from infra_operator.operators.mod import add_field, metadata_to_args, to_args, transform, with_args, with_default, with_ec2_tags, with_tags
import infra_operator.create.aws_secretsmanager as secretsmanager_client
from infra_operator.read.mod import get_name

ecs = clients["ecs"]
task_set_ecs = ECSServiceController()
elbv2 = clients["elbv2"]
ec2 = clients["ec2"]
iam = clients["iam"]
appmesh = clients["appmesh"]
# Custom app mesh client, just for virtual router and route
custom_appmesh = AppMeshController()
servicediscovery = clients["servicediscovery"]
app_scaling = clients["application-autoscaling"]
asg = clients['asg']
sqs = clients['sqs']
lambda_aws = clients['lambda']
cloudwatch = clients['cloudwatch']
cloudfront = clients['cloudfront']


def delete(kind, content, info, current):
    metadata = content.get("metadata", {})
    spec = content.get("spec", {})
    switch = {
        "ECS/Cluster":
        (ecs, "delete_cluster",
         [with_args({"cluster": get_name(content, kind, info)})]),
        "TaskDefinition":
        (ecs, "deregister_task_definition",
         [with_args({"taskDefinition": current.get("taskDefinitionArn")})]),
        "TargetGroup":
        (elbv2, "delete_target_group",
         [with_args({"TargetGroupArn": current.get("TargetGroupArn")})]),
        "Service": (task_set_ecs, "delete_service", [
            with_args({
                "cluster": info.get("ecs_cluster"),
                "service": current.get("serviceName"),
                "force": content.get("metadata", {}).get("force", True)
            }),
        ]),
        "LoadBalancer":
        (elbv2, "delete_load_balancer",
         [with_args({"LoadBalancerArn": current.get("LoadBalancerArn")})]),
        "SecurityGroup": (ec2, "delete_security_group",
                          [with_args({"GroupId": current.get("GroupId")})]),
        "Role": (aws_iam_delete, "delete_role", [with_args({"current": current})]),
        "Mesh": (appmesh, "delete_mesh",
                 [with_args({"meshName": metadata.get("meshName")})]),
        "VirtualNode": (appmesh, "delete_virtual_node", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualNodeName": metadata.get("virtualNodeName")
            })
        ]),
        "VirtualRouter": (custom_appmesh, "delete_virtual_router", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualRouterName": metadata.get("virtualRouterName")
            })
        ]),
        "Route": (appmesh, "delete_route", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualRouterName": metadata.get("virtualRouterName"),
                "routeName": metadata.get("routeName")
            })
        ]),
        "VirtualGateway": (custom_appmesh, "delete_virtual_gateway", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualGatewayName": metadata.get("virtualGatewayName")
            })
        ]),
        "GatewayRoute": (appmesh, "delete_gateway_route", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualGatewayName": metadata.get("virtualGatewayName"),
                "gatewayRouteName": metadata.get("gatewayRouteName")
            })
        ]),
        "VirtualService": (appmesh, "delete_virtual_service", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualServiceName": metadata.get("virtualServiceName")
            })
        ]),
        "ServiceDiscoveryService": (servicediscovery, "delete_service",
                                    [lambda _: {
                                        "Id": current.get("Id")
                                    }], None),
        "Secret": (secretsmanager_client, "delete_secret", [
            with_args({
                "SecretId": current.get("ARN"),
                "ForceDeleteWithoutRecovery": True,
            })
        ]),
        "ScalingPolicy": (app_scaling, "delete_scaling_policy", [
            with_args({
                "PolicyName": current.get("PolicyName"),
                "ServiceNamespace": current.get("ServiceNamespace"),
                "ResourceId": current.get("ResourceId"),
                "ScalableDimension": current.get("ScalableDimension")
            })
        ]),
        "ScalableTarget": (app_scaling, "deregister_scalable_target", [
            with_args({
                "ServiceNamespace": current.get("ServiceNamespace"),
                "ResourceId": current.get("ResourceId"),
                "ScalableDimension": current.get("ScalableDimension")
            })
        ]),
        "Queue": (sqs, "delete_queue", [
            with_args({
                "QueueUrl": current.get("QueueUrl")
            })
        ]),
        "LaunchTemplate": (ec2, "delete_launch_template", [
            with_args({
                "LaunchTemplateName": metadata.get("LaunchTemplateName")
            })
        ]),
        "Lambda": (lambda_aws, "delete_function", [
            with_args({
                "FunctionName": metadata.get("FunctionName")
            })
        ]),
        "AutoScalingGroup": (asg, "delete_auto_scaling_group", [
            with_args({
                "AutoScalingGroupName": metadata.get("AutoScalingGroupName"),
                "ForceDelete": True
            })
        ]),
        "LambdaEventSource": (lambda_aws, "delete_event_source_mapping", [
            with_args({
                "UUID": current.get("UUID")
            })
        ]),
        "LifeCycleHook": (asg, "delete_lifecycle_hook", [
            with_args({
                "LifecycleHookName": metadata.get("LifecycleHookName"),
                "AutoScalingGroupName": spec.get("AutoScalingGroupName")
            })
        ]),
        "Alarm": (cloudwatch, "delete_alarms", [
            with_args({
                "AlarmNames": [metadata.get("AlarmName")]
            })
        ]),
        "AutoScalingPolicy": (asg, "delete_policy", [
            with_args({
                "PolicyName": metadata.get("PolicyName"),
                "AutoScalingGroupName": spec.get("AutoScalingGroupName")
            })
        ]),
        "Distribution": (cloudfront, "delete_distribution", [
            with_args({
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            })
        ]),
        "CachePolicy": (cloudfront, "delete_cache_policy", [
            with_args({
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            })
        ]),
        "ContinuousDeploymentPolicy": (cloudfront, "delete_continuous_deployment_policy", [
            with_args({
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            })
        ]),
        "Instance": (ec2, "terminate_instances", [
            with_args({
                "InstanceIds": [current.get("InstanceId")],
            })
        ]),
    }
    client, method, steps = switch[kind]
    func = getattr(client, method)
    args = content
    for step in steps:
        args = step(args)
    res = func(**args)
    return res
