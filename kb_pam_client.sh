#/bin/bash

#This script should be placed in /usr/bin/ and made executable
#on every server you'd like to protect.
#Additionally, you need to add the following line to the
#end of /etc/pam.d/sshd on every server you'd like to protect:
#session required pam_exec.so seteuid /usr/bin/kb_pam_client.sh

#Modify anything encased in <CARROT_BRACKETS> to match your
#individual set-up.

if [ "$PAM_TYPE" != "close_session" ]; then
    KB_AUTH_URL=<http:// or https:// address to your auth server>
    KB_AUTH_TOKEN=<The auth token set in your environment on the auth server>
    SERVER_NAME=<The name you would like to identify this server as in chat>

    MSG_ID=`curl -X POST -d user=$PAM_USER -d server=$SERVER_NAME -d remote=$PAM_RHOST -d token=$KB_AUTH_TOKEN "$KB_AUTH_URL/request"`
    START_TIME=`date +'%s'`
    while :
    do
        if  (( ( `date +'%s'` - $NOW ) >= 15 )); then
            curl -X POST -d token=$KB_AUTH_TOKEN -d msg_id=$MSG_ID "$KB_AUTH_URL/timeout"
            exit 1
        fi
        STATUS=`curl -X GET "$KB_AUTH_URL/$MSG_ID?token=$KB_AUTH_TOKEN"`
        if [ "$STATUS" -eq "approved" ]; then
            exit 0
        fi
        if [ "$STATUS" -eq "denied" ]; then
            exit 1
        fi
    done
fi