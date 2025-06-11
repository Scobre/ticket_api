#!/bin/bash

[ -f .env ] || cp .env.example .env

docker-compose up -d
