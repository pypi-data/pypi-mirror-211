#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from functools import partial
from infra_operator.clients.mod import clients
from infra_operator.operators.mod import override, remove_inner_fields, sort_tags, to_args


def output(kind, content, info, current, filename):
