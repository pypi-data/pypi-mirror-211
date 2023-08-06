#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from infra_operator.clients.mod import clients
from infra_operator.operators.mod import dict_matcher, list_to_dict_by

client = clients["iam"]


def inline_policy_delete(current):
    RoleName = current["RoleName"]
    for policy in current.get("inline-policies", []):
        client.delete_role_policy(
            RoleName=RoleName,
            PolicyName=policy["PolicyName"]
        )


def managed_policy_detach(current):
    RoleName = current["RoleName"]
    for policy in current.get("managed-policies", []):
        client.detach_role_policy(
            RoleName=RoleName,
            PolicyArn=policy["PolicyArn"]
        )


def delete_role(current):
    check_list = [
        inline_policy_delete,
        managed_policy_detach,
    ]
    for check in check_list:
        check(current)
    client.delete_role(RoleName=current["RoleName"])
