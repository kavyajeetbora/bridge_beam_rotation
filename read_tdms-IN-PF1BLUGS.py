from nptdms import TdmsFile
from pandas import DataFrame

def read_tdms_data(filename, side="AMR"):

    data_dict = {}
    with TdmsFile.open(filename) as tdms_file:
        group = tdms_file["Log"]
        
        for i in range(1,5):
            data_dict[f'B{i}'] = group[f"{side}-INC-BU{i}-01"][:]
        
    return DataFrame(data_dict)