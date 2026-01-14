#!/bin/bash

export BUILDX_NO_DEFAULT_ATTESTATIONS=1
docker buildx bake "$@"
