pex_build(){
  gemini
  # sudo docker build -t pants-build -f infrastructure/dockerfiles/pants-build/Dockerfile .
  # sudo rm -rf .pants.d/
  dir_path=${1::-1}
  svc_name=${dir_path##*/}
  echo -e 'cd /code\n./pants binary $1/::\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  sudo chown $USER dist/$svc_name.pex
  cd -
}

pex_coverage(){
  gemini
  TEST_LOG_DIR="dist/coverage"
  COV_MODULES=$(find $1 -maxdepth 2 -name "__init__.py" | egrep -v '*/*test[s][_*]/*') || COV_MODULES=""
  COV_MODULES=$(echo ${COV_MODULES} | sed 's|/__init__.py||g' | sed 's| |,|g')
  echo $COV_MODULES
  echo -e 'cd /code\n./pants test $1:test --cache-test-pytest-ignore --test-pytest-coverage=$3 --test-pytest-coverage-output-dir=$2 --test-pytest-junit-xml-dir=$2\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1 $TEST_LOG_DIR $COV_MODULES
  cd -
}

pex_push(){
  gemini
  dir_path=${1::-1}
  svc_name=${dir_path##*/}
  echo -e 'cd /code\n./pants binary $1/::\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  sudo docker build -t registry.service.nsi.gemini/matthew/$svc_name -f $1/Dockerfile .
  sudo docker push registry.service.nsi.gemini/matthew/$svc_name
  sudo chown $USER dist/$svc_name.pex
  cd -
}

pex_test(){
  gemini
  echo -e 'cd /code\n./pants test $1/:: --tag=-integration\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  cd -
}

