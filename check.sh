# ./checker [t-value] [cpp src name] [infile] [outfile]

g++ $2 -o prog
./prog < $3 > $4

echo $1 > checker_input.txt
cat $3 >> checker_input.txt
cat $4 >> checker_input.txt

g++ checker.cpp -o check

./check < checker_input.txt