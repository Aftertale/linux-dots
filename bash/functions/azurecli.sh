#!/bin/bash

#function testMultiAccount() {
#
#}

function azActivate() {
	toActivate="$1" # should be dmcdowell-z or dmcdowell
	cp ~/.azureprofiles/${toActivate}.json ~/.azure/azureProfile.json
}

function azLogin() {
	az login --allow-no-subscriptions
	cp ~/.azure/azureProfile.json ~/.azureprofiles/dmcdowell.json
}

function azLoginZ() {
	az login
	cp ~/.azure/azureProfile.json ~/.azureprofiles/dmcdowell-z.json
}
