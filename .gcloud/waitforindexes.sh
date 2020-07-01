#!/bin/bash

# Continue to wait on Datastore Indexes if they aren't ready
# Cannot continue with Django migrations otherwise

function get_indexes { 
    state=$(gcloud datastore indexes list --format "value(state,kind)")
    ready=$(echo $state | grep "READY" | wc -l)
    creating=$(echo $state | grep "CREATING" | wc -l)
} 

echo "Checking Datastore indexes are ready..."
get_indexes

if [ $creating -ne 0 ]; then 
    START=$(date +%s.%N)
    echo "... waiting for indexes to be ready";

    while [ $creating -ne 0 ]
    do
        echo "... $creating creating, $ready ready ..."
        sleep 5
        get_indexes
    done

    echo "... Indexes ready"
    echo $state
else
    echo "... ready"
fi
