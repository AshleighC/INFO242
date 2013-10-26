DATA=2013-10-23-14.json
FILE=data.json

wget http://data.githubarchive.org/$DATA.gz
gunzip $DATA.gz
head -$1 $DATA > $FILE
python converter.py $FILE > data.xml

