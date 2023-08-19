PY_FILES=$(find . -name '*.py' -exec echo {} \;)
EXIT_CODES=()
for i in $PY_FILES
do
    pylint --fail-under=10 $i 
    EXIT_CODES+=($?)
done


echo ".py lint count=${#EXIT_CODES[@]}"
echo "exit codes=${EXIT_CODES[@]}"
for i in "${EXIT_CODES[@]}"
do
    if [ "$i" -ne "0" ]; then
        exit 1
    fi
done