
sc_id="$1"
filename="$2"

while read -r line
do
	remainder="$line"
	item_id="${remainder%%:*}"; 
	toml="${remainder#*: }"
	toml_v="${toml%%.toml*}"; 
    if [ "$sc_id" = "$item_id" ]; then
    	echo "Found SC $sc_id with TOML version $toml_v"
	fi;
done < "$filename"
