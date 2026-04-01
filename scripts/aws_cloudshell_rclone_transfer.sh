rclone copy b2:drivestats-iceberg/drivestats aws:backblaze-afr/processed/drivestats \
    --progress \
    --transfers 32 \
    --checkers 32
