# Function definitions for easier git schtuff

PROVIDER="ADO"
GIT_DEFAULT_ORG="CostcoWholesale"
GIT_DEFAULT_PROJECT="ECP"

# Git aliases
alias gunstage="git restore --staged "
alias k="kubectl"
alias gco="git checkout "
alias ga="git add "
alias gpl="git pull"
alias gpr="git pull-request"
function gp() {
	branchName=$(git rev-parse --abrev-ref HEAD)
	if [ "$branchName" = "main" ]; then
		echo "You are on the main branch! Checkout a new branch before you push!"
		exit 1
	fi
	hub push 2>/dev/null || git push 2>&1 | sed -n 's/.*\(git push.*\)/\1/p' | xargs command
}

function git() {
	case "$@" in
	"env")
		echo "setting environment vars"
		;;
	"freak")
		echo "linking main to master"
		git symbolic-ref refs/heads/main refs/heads/master
		;;

	"clean")
		git branch --merged | egrep -v "(^\*|main|master)" | xargs git branch -d
		;;

	# override clone behavior to deal with ado sillyness
	"clone -ado "*)
		org="$GIT_DEFAULT_ORG"
		project="$GIT_DEFAULT_PROJECT"
		if [[ "$#" -eq 5 ]]; then
			repo="$5"
			project="$4"
			org="$3"
		elif [[ "$#" -eq 4 ]]; then
			repo="$4"
			project="$3"
		else
			repo="$3"
		fi
		/usr/bin/git clone https://${org}@dev.azure.com/${org}/${project}/_git/${repo}
		;;

	"delete --olderthan"*)
		date=$3
		for item in $(git ls-files); do
			result=$(git --no-pager log --since "$date" -- $item)
			if [[ "$result" == "" ]]; then
				echo $item
				rm $item
			fi
		done
		;;

	"pull-request -v")
		/usr/bin/git pr view --web
		;;

	"pull-request")
		_getRemoteType &&
			az repos pr create ||
			gh pull-request
		;;

	"unstage")
		gunstage
		;;

	"unstash")
		git stash pop
		;;

	"api "*)
		/usr/bin/git "$@"
		;;

	*)
		/usr/bin/git "$@"
		;;
	esac
}

# determine whether remote is GitHub or ADO
function _getRemoteType() {
	adoUrl=$(/usr/bin/git remote get-url origin | awk -F@ '{ print $2 }')
	if [[ -n $adoUrl ]]; then
		return 1
	fi
	return 0
}

function gpr() {
	# Get the most recent commit message
	if [ -z $last_commit_message]; then
		git pull-request
		exit 0
	fi
	git pull-request -m $last_commit_message | pbcopy
}

function gcmtest() {
	PS3='Change type: '
	nouns=("feat" "fix" "refactor" "cancel")
	select noun in "${nouns[@]}"; do
		case $noun in
		"feat")
			echo "you chose choice 1"
			;;
		"fix")
			echo "you chose choice 2"
			;;
		"refactor")
			echo "you chose choice $REPLY which is $noun"
			;;
		"cancel")
			break
			;;
		*) echo "invalid option $REPLY" ;;
		esac
	done
}

function grr() {
	pushd $(git rev-parse --show-toplevel)
}

function gokeeb() {
	pushd $HOME/qmk_firmware/keyboards/gmmk/pro/
}

function flushdns() {
	sudo dscacheutil -flushcache
	sudo killall -HUP mDNSResponder
}

function git-branch-clean() {
	git branch --merged | egrep -v "(^\*|main)" | xargs git branch -d
}

#function releaseConsumerApp() {
#	imageVersion="$1"
#	hr="./apps/us-east-1/live/consumer-app-prod/consumer-app.yaml"
#	cd ~/code/src/github.com/updater/kubernetes-clusters/
#	current=$(git branch --show-current)
#	git checkout main
#	git pull
#	git branch --merged | egrep -v "(^\*|main)" | xargs git branch -d
#	git checkout -b release-consumer-app
#	sed -i '' "s/\(appVersion: \).*/\1${imageVersion}/" $hr
#	newVersion=$(dasel select -f "$hr" '.spec.values.appVersion')
#	if [ $imageVersion != $newVersion ]; then
#		echo "Something went wrong, do your change manually."
#		exit 1
#	fi
#	git add "$hr"
#	git commit -m "chore(apps/us-east-1/live/consumer-app-prod): release consumer app"
#	gp
#	url=$(git pull-request -m "chore(apps/us-east-1/live/consumer-app-prod): release consumer app ${imageVersion}")
#	echo $url | pbcopy
#	open $url
#}

#function alertRunFinished() {
#	echo "can I see?"
#	repo="$1"
#	run_status="in_progress"
#	counter=100
#	while [[ $run_status == "in_progress" ]] && [[ "counter" -gt 0 ]]; do
#		sleep 1
#		runs=$(gh api -H 'Accept: application/vnd.github+json' "/repos/Updater/$repo/actions/runs")
#		run_status=$(echo $runs | jq '.workflow_runs[0].status')
#		counter=($counter-1)
#	done
#	printf \\a
#}
#
function setGitEnvVars() {
	export GITHUB_TOKEN=$(op item get Github --field label=personal_token)
}
