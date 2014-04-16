#!/usr/bin/env python3

from distutils.core import setup

desc = "A python library for communicating with a golang json rpc server."

setup(name             = "gojsonrpcclient",
      version          = "1.0",
      description      = desc,
      author           = "J. David Lee",
      author_email     = "johnl@cs.wisc.edu",
      maintainer       = "johnl@cs.wisc.edu",
      url              = "none",
      py_modules       = ["gojsonrpcclient"],
      )


