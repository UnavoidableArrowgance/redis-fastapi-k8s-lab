#!/bin/bash

read -p "Enter the key: " key
read -p "Enter the value: " value

base_url="http://localhost/api"

echo "Storing value..."
curl -X POST "${base_url}/cache?key=${key}&value=${value}"

echo
echo "Retrieving value..."
curl "${base_url}/cache?key=${key}"

echo
