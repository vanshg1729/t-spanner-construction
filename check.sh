# ./check.sh [n-value] [t-value] [cpp src name] [infile] [outfile]

g++ dgg.cpp -o dgg
./dgg $1 > $4
rm ./dgg

g++ $3 -o prog
./prog $2 < $4 > $5
rm ./prog

echo $2 > checker_input.txt
cat $4 >> checker_input.txt
cat $5 >> checker_input.txt

g++ checker.cpp -o check

./check < checker_input.txt
rm ./check
