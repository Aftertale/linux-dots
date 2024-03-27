#!/bin/bash

# Simple wrapper for common Azure DevOps tasks

function ado() {
	return 0
}

function wait_for_ci() {
	prNum="$1"
	complete=false
	while [[ -z $complete ]]; do
		az pipelines build list | jq --arg pr_num ${prNum} '[] | select(.status != "completed") | select(.requestedFor.uniqueName == "dmcdowell@costco.com"'

	done
}

function my_prs() {
	az repos pr list | jq '.[] | select(.createdBy.uniqueName == "dmcdowell@costco.com")'
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
