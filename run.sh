DATA=2013-10-23-14.json
COUNT=5

if [ ! -f $DATA ]
then
  wget http://data.githubarchive.org/$DATA.gz
  gunzip $DATA.gz
fi

if [ $# -eq 1 ]
then
  COUNT=$1
fi

head -$COUNT $DATA > raw.json
python converter.py raw.json > raw.xml
python transformer.py raw.xml > data.xml

