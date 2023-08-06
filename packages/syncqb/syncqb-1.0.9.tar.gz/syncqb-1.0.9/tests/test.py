from syncqb import qb_client
from memory_profiler import profile
# from pprint import pprint
# from lxml.etree import _Element
@profile
def main():
    # table info:
    # database: bnsucj684
    # values valid for fid 6: 'Misc', '_other'
    # values valid for fid 9: 23
    # fid 3 is the record id, which is auto generated
    # use a value from fid 3 to update or delete a record
    # create a series of tests to test the functionality of each method for both xml and json
    # ONLY MODIFY OR DELETE RECORDS THAT YOU CREATED

    record_data = [
        {
            '6': 'Misc',
            '9': 23.0,
            '3': None
        },
        {
            '6': 'Misc',
            '9': 23.1,
            '3': None
        },
    ]
    record_data_csv = 'Misc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23'
    uploads = [
        {
            'field': '19',
            'filename': 'test.txt',
            'value': 'MjM='
        }
    ]

    main_asset_query = "{3.GT.0}"
    database = "bnj3r9rd8"
    columns = [
        1,
        2,
        3,
        4,
        5,
        7,
        8,
        9,
        10,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        57,
        59,
        60,
        61,
        63,
        64,
        65,
        66,
        67,
        68,
        70,
        71,
        73,
        85,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        105,
        106,
        107,
        108,
        114,
        121,
        124,
        126,
        128,
        131,
        132,
        136,
        145,
        185,
        160,
        254,
        236,
        238,
        239,
        240,
        254,
        255,
        259,
        262,
        266,
        267,
        268,
        269,
        272,
        276,
        277,
        278,
        279,
        284,
        285,
        286,
        299,
        303,
        304,
        307,
        305,
        306,
        309,
        314,
        315,
        318,
        320,
        340,
        389,
        402,
        405,
        411,
        425,
        426,
        427,
        428,
        454,
        455,
        457,
        456,
        458,
        461,
        468,
        470,
        471,
        472,
        478,
        479,
        480,
        481,
        482,
        483,
        484,
        492,
        493,
        494,
        495,
        496,
        497,
        498,
        499,
        507,
        509,
        519,
        523,
        528,
        529,
        541,
        561,
        562,
        567,
        569,
        571,
        572,
        577,
        583,
        585,
        594,
        597,
        598,
        605,
        607,
        617,
        621,
        625,
        631,
        640,
        642,
        645,
        646,
        652,
        653,
        654,
        655,
        658,
        681,
        685,
        721,
        722,
    ]

    client = qb_client.get_xml_client()
    client2 = qb_client.get_json_client()

    # xml_res = client.do_query(
    #     query='{3.EX.128}',
    #     # qid=10, 
    #     columns=[3, 6, 9], 
    #     database='bnsucj684', 
    #     # structured=True,
    #     # qid_custom_headers=True
    # )
    xml_res = 'N/A'
    # json_res = client2.do_query(
    #     query=main_asset_query,
    #     database=database,
    #     columns=columns,
    #     # high_volume=True,
    #     require_all=True,
    # )
    json_res = client2.do_query(
        query='{3.EX.128}',
        # qid=10,
        columns=[3, 6, 9], 
        database='bnsucj684',
    )
    # json_res = 'N/A'

    # print('xml_res:', xml_res)
    for record in json_res:
        print(record)
    print('json_res:', json_res)
    




if __name__ == '__main__':
    main()