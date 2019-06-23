from firebase import firebase
import datetime
import time
import serial
from SIMULATION import simulate

def get_data():
    FBConn = firebase.FirebaseApplication('https://test-6db14.firebaseio.com/', None)
    companyName1 = FBConn.get('/Company/Company1/', 'Name')
    companyName2 = FBConn.get('/Company/Company2/', 'Name')
    grrev1 = float(FBConn.get('/Company/Company1/', 'Data1v1'))
    grric1 = float(FBConn.get('/Company/Company1/', 'Data1v2'))
    grrasset1 = float(FBConn.get('/Company/Company1/', 'Data1v3'))
    grrliab1 = float(FBConn.get('/Company/Company1/', 'Data1v4'))
    grrentv1 = float(FBConn.get('/Company/Company1/', 'Data1v5'))

    grrev2 = float(FBConn.get('/Company/Company2/', 'Data2v1'))
    grric2 = float(FBConn.get('/Company/Company2/', 'Data2v2'))
    grrasset2 = float(FBConn.get('/Company/Company2/', 'Data2v3'))
    grrliab2 = float(FBConn.get('/Company/Company2/', 'Data2v4'))
    grrentv2 = float(FBConn.get('/Company/Company2/', 'Data2v5'))

    result2 = FBConn.get('/Company/CompanyData2', None)
    ls1 = simulate(companyName1, grrev1, grric1, grrasset1, grrliab1, grrentv1)
    ls2 = simulate(companyName2, grrev2, grric2, grrasset2, grrliab2, grrentv2)
    print(ls1)
    print(ls2)
    ls = [ls1, ls2, companyName1, companyName2]
    final_result(ls)
    return ls

def final_result(result_list):
    # Create the connection to our Firebase database - don't forget to change the URL!
    FBConn = firebase.FirebaseApplication('https://test-6db14.firebaseio.com/', None)
    
    data1v1 = result_list[0][0]
    data1v2 = result_list[0][1]
    data1v3 = result_list[0][2]
    data1v4 = result_list[0][3]
    data1v5 = result_list[0][4]
    data1v6 = result_list[0][5]
    data1v7 = result_list[0][6]
    data1v8 = result_list[0][7]
    data1v9 = result_list[0][8]
    data1v10 = result_list[0][9]
    data2v1 = result_list[1][0]
    data2v2 = result_list[1][1]
    data2v3 = result_list[1][2]
    data2v4 = result_list[1][3]
    data2v5 = result_list[1][4]
    data2v6 = result_list[1][5]
    data2v7 = result_list[1][6]
    data2v8 = result_list[1][7]
    data2v9= result_list[1][8]
    data2v10 = result_list[1][9]

    # Create a dictionary to store the data before sending to the database
    data_to_upload = {
        'Data0' : data1v1,
        'Data1' : data1v2,
        'Data2' : data1v3,
        'Data3' : data1v4,
        'Data4' : data1v5,
        'Data5' : data1v6,
        'Data6' : data1v7,
        'Data7' : data1v8,
        'Data8' : data1v9,
        'Data9' : data1v10
    }

    data_to_upload_2 = {
        'Data0' : data2v1,
        'Data1' : data2v2,
        'Data2' : data2v3,
        'Data3' : data2v4,
        'Data4' : data2v5,
        'Data5' : data2v6,
        'Data6' : data2v7,
        'Data7' : data2v8,
        'Data8' : data2v9,
        'Data9' : data2v10
    }
    # Post the data to the appropriate folder/branch within your database

    key1 = FBConn.post('/MLData/CompanyData1',data_to_upload)
    key2 = FBConn.post('/MLData/CompanyData2', data_to_upload_2)
    key1val = key1['name']
    key2val = key2['name']
    res1 = []
    res2 = []
    path1 = '/MLData/CompanyData1/' + key1val
    path2 = '/MLData/CompanyData2/' + key2val
    res1.append(FBConn.get(path1, 'Data0'))
    res1.append(FBConn.get(path1, 'Data1'))
    res1.append(FBConn.get(path1, 'Data2'))
    res1.append(FBConn.get(path1, 'Data3'))
    res1.append(FBConn.get(path1, 'Data4'))
    res1.append(FBConn.get(path1, 'Data5'))
    res1.append(FBConn.get(path1, 'Data6'))
    res1.append(FBConn.get(path1, 'Data7'))
    res1.append(FBConn.get(path1, 'Data8'))
    res1.append(FBConn.get(path1, 'Data9'))



    res2.append(FBConn.get(path2, 'Data0'))
    res2.append(FBConn.get(path2, 'Data1'))
    res2.append(FBConn.get(path2, 'Data2'))
    res2.append(FBConn.get(path2, 'Data3'))
    res2.append(FBConn.get(path2, 'Data4'))
    res2.append(FBConn.get(path2, 'Data5'))
    res2.append(FBConn.get(path2, 'Data6'))
    res2.append(FBConn.get(path2, 'Data7'))
    res2.append(FBConn.get(path2, 'Data8'))
    res2.append(FBConn.get(path2, 'Data9'))

    print(res1)
    print(res2)
    res = [res1, res2]
    return res


# res = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
# final_result(res)
# get_data()
