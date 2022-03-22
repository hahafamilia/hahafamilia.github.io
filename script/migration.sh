for f in `ls ./*/*md`; do sed '/^date:/d' $f  > $f'2'; done

for f in `ls ./*/*.md`; do echo $f; done;

for f in `ls ./*/*.md`; do echo $f'2'; done;


for f in `ls ./*/*.md2`; do rm $f; done;

for f in `ls ./*/*.md`; do rm $f; done;

for f in `ls ./*/*.md2`; do mv $f ${f:0:-1}; done;


for f in `ls ./*/*.md`; do  echo $f | awk -F '/' '{print $2}' ; done;

sed -n "/^---.*\n/p" life/test.md

sed -i '' -e 's/](\/images\/.*\/2/](\/assets\/images\/2/g' development/kafka-zookeeper-troubleshooting.md
sed -i '' -e 's/n.m/aaa/g' test.txt

](/assets/images/2020

](/images/boo
[](/images/book/2020-0