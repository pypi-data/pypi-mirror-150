#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from hpo import api


urlpatterns = [
    path( r'phenotype/', api.phenotype, name='phenotype'),
]
