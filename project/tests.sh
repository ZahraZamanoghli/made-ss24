#!/bin/bash

DATA_DIR="../data"

echo "Cleaning previous test data..."
rm -rf $DATA_DIR/*
mkdir -p $DATA_DIR
echo "Previous test data cleaned successfully"

echo "Running the data pipeline..."
python3 project.py
echo "Data pipeline ran successfully"

echo "Running tests..."
pytest tests.py
