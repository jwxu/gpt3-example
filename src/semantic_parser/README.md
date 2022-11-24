## Start Remote
ssh oval@wikidata-qa.westus2.cloudapp.azure.com

## In Remote
screen 

source ~/.virtualenv/genie/bin/activate

cd wikidata-workdir
./run-nlu-server.sh 30

## In Local

ssh oval@wikidata-qa.westus2.cloudapp.azure.com -NfL 8400:localhost:8400

node index.js 

