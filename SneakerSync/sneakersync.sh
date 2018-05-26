#!/usr/bin/env bash

SYNC_PATH="/mnt/files/"
BACKUP_PATH="/mnt/external/"
REMOTE_HOST="example.com"
SSH_OPTIONS="ssh -p 22"

rsync -nav --size-only -e "$SSH_OPTIONS" "$SYNC_PATH" "$USER@$REMOTE_HOST:$SYNC_PATH" | while read file; do
  path="$SYNC_PATH$file"
  if [ -f "$path" ]; then
    destination=${path/"$SYNC_PATH"/"$BACKUP_PATH"}
    if [ -f "$destination" ]; then
      echo "$destination already exists, skipping"
    else
      echo "Copying $path to $destination"
      destination_dir=`dirname "$destination"`
      mkdir -p "$destination_dir"
      cp "$path" "$destination"
    fi
  fi
done
