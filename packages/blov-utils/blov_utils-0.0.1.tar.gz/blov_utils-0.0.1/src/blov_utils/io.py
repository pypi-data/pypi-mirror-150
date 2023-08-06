import json
import pickle

def save_dict_to_json(obj_dict, output_path):
    with open(output_path, 'w') as fp:
        json.dump(obj_dict, fp)

def load_dict_from_json(input_path):
    with open(input_path, 'r') as fp:
        obj_dict = json.load(fp)
    return obj_dict


def save_object_to_pickle(pickle_path, input_object):
    with open(pickle_path, 'wb') as handle:
        pickle.dump(input_object, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load_object_from_pickle(pickle_path):
    with open(pickle_path, 'rb') as handle:
        output_object = pickle.load(handle)

    return output_object