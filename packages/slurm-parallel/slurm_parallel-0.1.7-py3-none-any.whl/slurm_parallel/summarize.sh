#!/bin/bash

sacct -j $1 --format=State%20 -X
