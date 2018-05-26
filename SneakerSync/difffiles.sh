#!/usr/bin/env bash

SYNC_PATH="/mnt/files/"
REMOTE_HOST="example.com"
SSH_OPTIONS="ssh -p 22"

rsync -nav --size-only -e "$SSH_OPTIONS" "$SYNC_PATH" "$USER@$REMOTE_HOST:$SYNC_PATH" | while read file; do
  path="$SYNC_PATH$file"
  if [ -f "$path" ]; then
    echo $path
  fi
done
