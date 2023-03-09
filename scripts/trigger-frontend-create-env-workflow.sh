#!/bin/sh
github_user=$1
github_pat=$2
org=$3
repo=$4
branch=$5

test -z $github_user && echo "github user is required." 1>&2 && exit 1
test -z $github_pat && echo "github pat is required." 1>&2 && exit 1
test -z $org && echo "org is required." 1>&2 && exit 1
test -z $repo && echo "repo is required." 1>&2 && exit 1
test -z $branch && echo "branch is required." 1>&2 && exit 1

frontend_branch=$(curl -u "$github_user:$github_pat" "https://api.github.com/repos/$org/$repo/branches/$branch")
frontend_branch_name=$(echo "${frontend_branch}" | jq -r '.name')

if [ "$frontend_branch_name" = "null" ]
then
      echo "branch $branch doesn't exist in $org:$repo"
      curl -u "$github_user:$github_pat" https://api.github.com/repos/$org/$repo/actions/workflows/create_ephemeral_env.yml/dispatches -d "{\"ref\":\"develop\",\"inputs\":{\"branch\":\"$branch\"}}"

else
      echo "branch $frontend_branch_name exists in $org:$repo"
      frontend_prs=$(curl -u "$github_user:$github_pat" "https://api.github.com/repos/$org/$repo/pulls?head=$org:$frontend_branch_name&base=develop")
      frontend_prs_len=$(echo "${frontend_prs}" | jq -r '.' | jq length)
      echo "$frontend_prs_len pull requests exist for $org:$frontend_branch_name"

      if [ "$frontend_prs_len" = 0 ]
      then
            echo "creating a pr for $org:$frontend_branch_name"
            curl -u "$github_user:$github_pat" https://api.github.com/repos/$org/$repo/pulls -d "{\"title\":\"$frontend_branch_name\",\"head\":\"$org:$frontend_branch_name\",\"base\":\"develop\",\"body\":\"auto generated from a github workflow\"}"
      fi

fi