#!/bin/bash

AKS_PROFILES="$HOME/.aks/profile.yaml"

function aks() {
	case "$@" in
	"login"*)
		shift
		az login && grab-aks "$@"
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

function cluster() {
	case "$@" in
	"up"*)
		shift
		makecluster "$@"
		;;
	"down"*)
		shift
		unmakecluster "$@"
		;;
	"login"*)
		shift
		grab-aks "$@"
		;;
	*)
		echo "We do not support that yet!"
		;;
	esac
	return 0
}

function makecluster() {
	cluster=dmcdowell
	location=westus2
	branch=main
	org='https://dev.azure.com/CostcoWholesale'
	open=""

	while [ "$#" -gt 0 ]; do
		case "$1" in
		"-c")
			shift
			cluster=$1
			shift
			;;
		"-l")
			shift
			location=$1
			shift
			;;
		"-b")
			shift
			branch=$1
			shift
			;;
		"-o" | "--org")
			shift
			branch=$1
			shift
			;;
		"--open")
			shift
			open="--open"
			shift
			;;
		*)
			echo "unknown parameter"
			return 1
			;;
		esac
	done

	parameters="cloud_version=c2 scope=np location=$location cluster=$cluster deploy_cluster_stack=true enable_standard_tier_on_dev=false run_playbook=true install_dynatrace=false install_splunk=false run_tests=true install_cluster_dns_utility=false install_customer_tenants=false cleanup_on_failure=false $open"

	az pipelines run --branch $branch --org=$org --project ECP --name aks.cluster.deploy --parameters $parameters
}

function testPrms() {
	case "$@" in
	"login"*)
		shift
		echo "az login" && echo "$@"
		;;
	*)
		echo "do nothing"
		;;
	esac
}
