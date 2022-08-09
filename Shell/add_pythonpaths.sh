add_pypaths() {
  PYTHONPATH=~/Code/gemini/dist/
  for dir in ~/Code/gemini/cli/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/libraries/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/services/*/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/submodules/gemini-mothra-tomls/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/submodules/obscura-plugins/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/test-utilities/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/tools/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/validation/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  export PYTHONPATH=$PYTHONPATH
}

