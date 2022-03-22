#!/bin/bash

total=0
test_total=0

function usage() {
    echo "Usage: $0 all | bkt | rdc | category[1-3]"
    exit 0
}

function fail() {
    local exit_code=$?
    echo "[ERROR] $1"
    exit $exit_code
}

function run_backtracking() {
    local t
    t=$( TIMEFORMAT=%R; time ( make -s run_backtracking CTG=${ctg} TEST=${i} 2>/dev/null 1>/dev/null ) 2>&1 ) || return $?
    bkt_time+=( $( printf "%.3f" $t ) )
}

function run_reduction() {
    local t1
    t1=$( TIMEFORMAT=%R; time ( make -s run_reduction CTG=${ctg} TEST=${i} 2>/dev/null 1>/dev/null ) 2>&1 ) || return $?
    local t2
    t2=$( TIMEFORMAT=%R; time ( python3 sat_solver.py tests/aux/${ctg}/test${i}.aux > tests/out/${ctg}/test${i}.out ) 2>&1 ) || return $?
    local t=$( echo "$t1 + $t2" | bc )
    rdc_time+=( $( printf "%.3f" $t ) )
}

function run_tests() {
    local aux_total=0
    total=0
    test_total=0
    if [[ ! -z $3 ]]; then
        local cs=( $3 )
    else
        local cs=( 1 2 3 )
    fi 

    for c in ${cs[@]}; do
        ctg=category${c}
        echo "RUNNING $1 $ctg"
        
        local test_no=$(ls tests/in/${ctg}/ | wc -l)
        test_total=$(( $test_total + $test_no ))

        for (( i=0; i<$test_no; i++ )); do
            echo "" > tests/out/${ctg}/test${i}.out
            local out_str="[TEST${i}] - "

            $2

            if [[ $? != 0 ]]; then
                out_str=${out_str}ERROR
            else
                local out=$(diff -w "tests/ref/${ctg}/test${i}.ref" "tests/out/${ctg}/test${i}.out" 2>&1)
                
                if [[ -z "$out" ]]; then
                    aux_total=$(( aux_total + 1 ))
                    out_str=${out_str}PASSED
                else
                    out_str=${out_str}FAILED
                fi
            fi
            
            echo "$out_str"
        done
    done

    total=$(( $total + $aux_total ))
    echo "TOTAL: ${total}/$(( $test_total ))"
}

function run_bkt_checks() {
    bkt_time=()
    run_tests "BACKTRACKING" run_backtracking $1 
    bkt_sum=$(printf "%.3f" $(IFS=+; echo "${bkt_time[*]}" | bc))
    echo "BACKTRACKING TOTAL TIME: ${bkt_sum}s"
    echo
}

function run_rdc_checks() {
    rdc_time=()
    run_tests "REDUCTION" run_reduction $1
    rdc_sum=$(printf "%.3f" $(IFS=+; echo "${rdc_time[*]}" | bc))
    echo "REDUCTION TOTAL TIME: ${rdc_sum}s"
    echo
}

function time_rep() {
    printf "REDUCTION / BACKTRACKING: %.3f\n" $(echo "scale=3; $rdc_sum / $bkt_sum" | bc)
}

# Prerun checks
[[ $# != 1 ]] && usage
[[ ! -e src/Makefile ]] && fail "Makefile not found"

# Prepare running directory (out)
rm -rf out 2>&1 1>/dev/null
mkdir out
cp -r src/* out/
cp sat_solver.py out/
cp -r tests out/
cp sat_solver.py out/
cd out
for c in {1..3}; do
    mkdir -p tests/aux/category${c}
    mkdir -p tests/out/category${c}
done

make -s build || fail "Build failed"

case "$1" in
    all)
        run_bkt_checks
        run_rdc_checks
        # echo "FINAL TOTAL: ${total}/$(( $TEST_NO * 2 ))"
        time_rep
    ;;
    bkt)
        run_bkt_checks
    ;;
    rdc)
        run_rdc_checks
    ;;
    category[1-3])
        CTG=${1:(-1)}
        run_bkt_checks $CTG
        run_rdc_checks $CTG
        time_rep
    ;;
    *)
    usage
    ;;
esac