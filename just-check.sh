# ./check.sh [n-value] [t-value] [cpp src name] [infile] [outfile]

g++ $3 -o prog.out
./prog.out $2 < $4 > $5
rm ./prog.out

echo $2 > checker_input.txt
cat $4 >> checker_input.txt
cat $5 >> checker_input.txt

g++ checker.cpp -o check.out

./check.out < checker_input.txt
rm ./check.out
