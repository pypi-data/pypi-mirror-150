#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Dylan Wootton and Josh Pollock.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..example import ExampleWidget


def test_example_creation_blank():
    w = NerfNav()
    assert w.value == 'Hello World'
