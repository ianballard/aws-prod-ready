
if [ $# -eq 0 ] || [ $1 = "dev" ]; then
  file_name=development
elif [ $1 = "release" ]; then
  file_name=release
elif [ $1 = "prod" ]; then
  file_name=production
fi

# todo: update
profile=ianballard

# todo: mfa or sso login here
sam local start-api --port 2999 \
                    --template-file template.local.yaml \
                    --debug-port 5858 \
                    --skip-pull-image \
                    --debug \
                    --profile $profile \
                    --warm-containers LAZY \
                    --region us-east-2
# LAZY will build the container when it's first called or after a change is detected. 
# EAGER will build every container as soon as the command is run so your first boot will take several minutes.
# One issue, if any container crashes in eager mode, Sam terminates all containers and closes, so 
#--docker-network host  # Commented out due to weird issues in latest SAM CLI