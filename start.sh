#!/bin/bash
while true; do
    python 02_enrich_finqa_data_anthropic.py
    sleep 1  # Prevents rapid restarts in case of immediate failure
done
