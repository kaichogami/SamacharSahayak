#!/usr/bin/env bash

samachar=$(pwd)
rm -r $HOME/.personal_lambda/
mkdir -p $HOME/.personal_lambda/samachar

cd $HOME/.personal_lambda
virtualenv venv
source venv/bin/activate

cd samachar

cp -rf $samachar/. .

pip install -r $samachar/requirements.txt -t .

zip -r lambda_samachar.zip .

cp -rf lambda_samachar.zip $HOME/Documents/


