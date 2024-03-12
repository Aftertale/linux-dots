#!/bin/bash

AKS_PROFILES="$HOME/.aks/profile.yaml"

function aks() {
	case "#@" in
	"login "*)
		echo "az login command $2" # login and update cluster config
		;;
	"list")
		echo "az list clusters"
		;;
	*)
		echo "not yet supported"
		;;
	esac
}
function grab-aks() {
	zone=${2:-westus2}
	echo "${zone}-${1}"
	az aks get-credentials -n "${1}" -g c2-np-${zone}-ecp-aks-${1}-rg --overwrite-existing --admin
	ECP_CLUSTER_CONTEXT=${1}-admin
}
