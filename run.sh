rm /tmp/fuzzer_inp*
rm vul
rm vul.c.gcov
rm vul.gcda
rm vul.gcno
gcc -o vul vul.c --coverage 
rm -r "in"
rm -r "out"
mkdir "in"
echo "AAAA" > "./in/test"
mkdir "out"
python3 fuzzer.py
