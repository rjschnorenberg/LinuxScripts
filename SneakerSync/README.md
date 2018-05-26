# SneakerSync
These scripts use rsync to diff the files between two servers over SSH so that they can be copied to an external drive and synced manually.

[difffiles.sh](difffiles.sh) will print a list of files that exist locally in *SYNC_PATH* but not on the remote server.

[sneakersync.sh](sneakersync.sh) will copy files that exist in *SYNC_PATH* localy but not on the remote server to the same relative path in *BACKUP_PATH*.

If SSH is not running on port 22 it can be changed in *SSH_OPTIONS*.