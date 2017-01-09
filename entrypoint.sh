#!/bin/sh

set -e
if [[ "${DEBUG}" ]]; then
    set -x
fi

# match user uids / gids
source setuidgid.inc

exec gosu "${DOCKER_USER}" "$@"
