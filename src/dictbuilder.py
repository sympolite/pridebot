import os

class DictParseError(Exception): pass


def open_dict(dict_file):
    dict_data = []
    with open(dict_file, 'r') as df:
        for line in df:
            dict_data.append(line)
    return dict_data

def parse_dict(data):
    temp_dict = {}
    for line in data:
        d1 = line.split(':', 1)
        filename = d1[0].strip().lower()
        keywords = d1[1].strip().lower()
        realpath = os.path.join("flags", filename+'.png')
        fullpath = os.path.join(os.getcwd(),realpath)
        if not os.path.exists(fullpath):
            raise DictParseError(f'"{filename}" does not refer to an actual file.')
        if keywords is None: #empty keyword list
            raise DictParseError(f'Keyword list for "{filename}" is blank.')
        keyword_list = keywords.split()
        temp_dict[filename] = keyword_list
    return temp_dict

def build_dict(dict_file):
    temp = parse_dict(open_dict(dict_file))
    final = {}
    for key, val in temp.items():
        for item in val:
            final[item] = key
    return final


if __name__ == '__main__':
    print('TESTING...')
    
    final = build_dict('config.txt')
    for key, val in final.items():
        print(f'{key}: {val}')
    print('\nTest run complete!')
    q = input('Press any key to exit.')
        
        
        
