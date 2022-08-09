quicklook(){
  # "decrypted SFX image" AND (*112_* OR *113_*) in PDP logs
  gemini
  work gemini
  aws s3 cp $"s3://bsg-gemini-images-prod-sfx-packets/$1" . 
  image=$(basename $1)
  ./dist/dioptra-cli.pex make_pan ./$image
  rm ./$image
  parts=(${image//_/ })
  rm ./$"${parts[1]}_${parts[0]}_pan.tiff"
}

