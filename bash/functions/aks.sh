#!/bin/bash

function grab-aks() {
	zone=${2:-westus2}
	echo "${zone}-${1}"
	az aks get-credentials -n "${1}" -g c2-np-${zone}-ecp-aks-${1}-rg --overwrite-existing --admin
	ECP_CLUSTER_CONTEXT=${1}-admin
}
