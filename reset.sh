#!/bin/bash
docker compose down
docker volume rm dockermc_config-files-volume
docker volume rm dockermc_world-volume
