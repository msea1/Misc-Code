import toml

COLUMNS = ['SAP Family', 'SAP Full Name', 'SAP ID', 'Description/Comments', 'Data Type', 'Data Size', 'Default Value', 'Units', 'Rationale']
WE_CARE_ABOUT = [1, 2, 3, 4, 6, 7]
data_type_col = 'Data Type'
def_val_col = 'Default Value'


def main():
    conf_dict = {'saps': []}
    with open('./conf.txt') as conf_file:
        conf_data = conf_file.readlines()
    for line in conf_data:
        cols = line.split('\t')
        sap_info = {COLUMNS[i]: x for i, x in enumerate(cols) if i in WE_CARE_ABOUT}
        if len(sap_info) == len(WE_CARE_ABOUT):
            if is_number(sap_info.get(def_val_col)):
                decl = sap_info.get(data_type_col)
                if decl == 'Double' or decl == 'Float':
                    sap_info[def_val_col] = float(sap_info[def_val_col])
                elif 'integer' in decl.lower():
                    sap_info[def_val_col] = int(sap_info[def_val_col])
            conf_dict['saps'].append(sap_info)
    with open('./saps.toml', 'w') as output:
        toml.dump(conf_dict, output)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main()
