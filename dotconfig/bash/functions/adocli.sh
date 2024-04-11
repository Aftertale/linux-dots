#!/bin/bash

# Simple wrapper for common Azure DevOps tasks
# format:
# ado <repos | pipe(line)s | tasks
# fall back to git?
function ado() {
	while [ $# -gt 0 ]; do
		case "$1" in
		"repos")
			handleRepos
			;;
		*)
			echo "$1 not implemented"
			;;
		esac
	done
}

function handleRepos() {
	echo "repos $@"
}

function handlePipelines() {
	echo "pipelines $@"
}

function handleTasks() {
	echo "tasks $@"
}

function pr() {
	# pipe the modified pr template through
	echo "pr"
}

function wait_for_ci() {
	prNum="$1"
	incomplete=false
	while [[ -n "$incomplete" ]]; do
		incomplete=$(az pipelines build list | jq --arg pr_num ${prNum} '[] | select(.status != "completed") | select(.requestedFor.uniqueName == "dmcdowell@costco.com"')
		sleep 60
	done
}

function my_prs() {
	az repos pr list | jq '.[] | select(.createdBy.uniqueName == "dmcdowell@costco.com")'
}

function __checkValue() {
	return 0
}

# note ... this might be worthwhile to turn into a tui
# todo
# PRs:
#   open PR
#   edit PR
#   view PR
#   approve PR
#   comment on PR
#   view diffs and whatnot
# WorkItems:
#   see all work items
#   see my work items
#   see work items by team member
#   change status of work item
#   create work itemk
function cluster() {
	case "$@" in
	"build")
		echo "build"
		;;
	*)
		echo "not implemented"
		;;
	esac
}
