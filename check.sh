# ./check.sh [n-value] [t-value] [cpp src name] [infile] [outfile]

g++ dgg.cpp -o dgg
./dgg $1 > $4

g++ $3 -o prog
./prog < $4 > $5

echo $2 > checker_input.txt
cat $4 >> checker_input.txt
cat $5 >> checker_input.txt

g++ checker.cpp -o check

./check < checker_input.txt
