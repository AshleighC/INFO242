DATA=2013-10-23-14.json
FILE=data.json
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

head -$COUNT $DATA > $FILE
python converter.py $FILE > data.xml

