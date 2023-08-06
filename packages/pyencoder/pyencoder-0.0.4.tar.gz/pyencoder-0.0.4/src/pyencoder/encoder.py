def encode_list(lists, level_parent=''):
    encoded_str = list()
    level_cnt = 0
    for data in lists:
        if type(data) == list:
            level_cnt += 1
            val = '%list' + level_parent + '_' + str(level_cnt) + ';'
            val += encode_list(data, level_parent + '_' + str(level_cnt))
            val += '%list' + level_parent + '_' + str(level_cnt) + ';'
        elif type(data) == int:
            val = '%int;' + str(data) + ';'
        elif type(data) == float:
            val = '%float;' + str(data) + ';'
        elif type(data) == str:
            val = '%str;' + data + ';'
        else:
            raise ValueError("Encode Error, Unknown type : " + type(data))

        encoded_str.append(val)
    return ''.join(encoded_str)

def decode_list(encoded_str):
    decoded_list = list()
    encoded_str_list = encoded_str.split(';')

    is_data = False
    continue_until = None
    for data in encoded_str_list:
        if continue_until is not None:
            if data == continue_until:
                continue_until = None
            continue
        if is_data is False:
            if '%list' in data:
                from re import search
                data_sc = data + ';' # sc (semi colon) is needed. otherwise, sub_encoded_str won't extracted properly.
                sub_encoded_str = search(data_sc + '(.+)' + data_sc, encoded_str).group(1)
                continue_until = data
                val = decode_list(sub_encoded_str)
                decoded_list.append(val)
            elif '%int' in data:
                is_data = int
            elif '%float' in data:
                is_data = float
            elif '%str' in data:
                is_data = str
        else:
            if is_data is int:
                val = int(data)
                decoded_list.append(val)
            elif is_data is float:
                val = float(data)
                decoded_list.append(val)
            elif is_data is str:
                val = data
                decoded_list.append(val)
            is_data = False

    return decoded_list

def list2str(lists):
    encoded_str = list()
    for data in lists:
        if type(data) == list:
            val = list2str(data)
        elif type(data) == int:
            val = str(data) + ', '
        elif type(data) == float:
            val = str(data) + ', '
        elif type(data) == str:
            val = data + ', '
        else:
            raise ValueError("Encode Error, Unknown type : " + type(data))
        encoded_str.append(val)
    encoded_str = ''.join(encoded_str)
    if encoded_str[-2:-1] == ",":
        encoded_str = encoded_str[0:-2]
    encoded_str = "[" + encoded_str + "]"
    return encoded_str
