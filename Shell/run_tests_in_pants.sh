gemini_tests() {
  gemini
  echo -e 'cd /code\n./test-all.sh > /tmp/tests.txt' > /tmp/tests.sh
  echo -e "grep -Eo '(.*):test.*\.\.\.\.\.   FAILURE' /tmp/tests.txt | sort | uniq -c | awk '{print \$4\": \"\$2}' && grep -Eo '\.\.\.\.\.   SUCCESS' /tmp/tests.txt | sort | uniq -c | awk '{print \$3\": \"\$1}'\nexit" >> /tmp/tests.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/tests.sh:/tests.sh pants-build bash tests.sh
  cd -
}

