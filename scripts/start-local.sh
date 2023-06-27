
# todo: mfa or sso login here
sam local start-api --port 2999 \
                    --debug-port 5858 \
                    --debug \
                    --region us-east-2 \
                    --warm-containers LAZY
