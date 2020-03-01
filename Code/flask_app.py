# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os,glob
import pandas as pd
import re
import math
import copy
#!/usr/bin/env python3

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'HVZ.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'HVZ'
app.config['MYSQL_PASSWORD'] = 'Hrushi1!2@'
app.config['MYSQL_DB'] = 'HVZ$shopitems'
app.config['UPLOAD_FOLDER'] = 'mysite/uploads'


mysql = MySQL(app)
@app.route('/')
def index():

    return render_template('first.html')

#####################################################################################################################################
@app.route('/custornot',methods=['POST'])
def custornot():
    data =request.form['verif']
    if data == 'yes':
        return render_template('enterShopID.html')
    else:
        return redirect('/shopregister')

#####################################################################################################################################

@app.route('/customer',methods=['POST'])
def customer():
    id =request.form['shopid']
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT icode,iname FROM items where shopid=%s",(id))

    # data = cur.fetchall()
    # cur.close()
    data =[]
    row_list=[]
    os.chdir(app.config['UPLOAD_FOLDER'])
    for file in glob.glob(str(id)+"*"):
        # print(file)
        df=pd.read_csv(file)
        row_list=df.values.tolist()

        # eliminate nan values
        for i in range(len(row_list)):
            for j in range(len(row_list[0])):
                if pd.isnull(row_list[i][j]):
                    row_list[i][j] = '0';

        for i in range(len(row_list)):
            for j in range(len(row_list[i])):
                if row_list[i][j]!='0' and row_list[i][j]!='1' and row_list[i][j]!='2':
                    data.append(row_list[i][j])

    os.chdir("/home/HVZ")
    print(row_list)
    print(data)
    return render_template('customer.html',result=data,sid=id)

#####################################################################################################################################
# @app.route('/createTSPArray',methods=['POST'])
# def createTSPArray():

#     items =request.form.getlist('items')
#     print(items)
#     items2 = {}
#     for i in items:
#         items2[i] =1

#     # print(items2)

#     shopid =request.form['shopid']

#     os.chdir(app.config['UPLOAD_FOLDER'])
#     # os.chdir("/uploads")
#     shopLayout =[]
#     starting =[]

#     def getProductsOnCurrLevel(floor,items):

#         r=[]
#         print("floor is "+str(floor))
#         for i in range(len(floor)):
#             for j in range(len(floor[i])):
#                 if floor[i][j] in items2.keys():
#                     r.append([i,j])
#         print("r is "+str(r))
#         return r

#     def valid(x,y,xb,yb):
#         if x<xb and x>=0 and y<yb and y>=0:
#             return True

#         return False

#     def getPosOfNearestZ(sl,item):

#         xb =len(sl)
#         yb =len(sl[0])
#         if valid(item[0]+1,item[1],xb,yb)==True:
#             if sl[item[0]+1][item[1]]=='0':
#                 return [item[0]+1,item[1]]
#         elif valid(item[0]-1,item[1],xb,yb)==True:
#             if sl[item[0]-1][item[1]]=='0':
#                 return [item[0]-1,item[1]]

#         if valid(item[0],item[1]+1,xb,yb)==True:
#             if sl[item[0]][item[1]+1]=='0':
#                 return [item[0],item[1]+1]
#         elif valid(item[0],item[1]-1,xb,yb)==True:
#             if  sl[item[0]][item[1]-1]=='0':
#                 return [item[0],item[1]-1]

#         if item[0]==0 and item[1]==0:
#           if sl[1][1]=='0':
#               return [1,1]
#         if item[0] == 0 and item[1] == len(sl)-1:
#             if sl[1][len(sl)-2] == '0':
#                 return [1,len(sl)-2]
#         if item[0]==len(sl)-1 and item[1]==0:
#           if sl[len(sl)-2][1]=='0':
#               return [len(sl)-2,1]
#         if item[0]==len(sl)-1 and item[1]==len(sl)-1:
#           if sl[len(sl)-2][len(sl)-1]=='0':
#               return [len(sl)-2,len(sl)-1]
#         return "inaccessible"

#     for file in glob.glob(str(shopid)+"*"):
#         # print(file)
#         df=pd.read_csv(file)
#         row_list=df.values.tolist()

#         for i in range(len(row_list)):
#             for j in range(len(row_list[0])):
#                 if pd.isnull(row_list[i][j]):
#                   row_list[i][j] =0;

#                 if row_list[i][j]=="start":
#                     starting.append([i,j])

#         shopLayout.append(row_list)

#     # print(shopLayout)

#     levelWiseProducts =[]

#     for i in range(len(shopLayout)):
#         prod =getProductsOnCurrLevel(shopLayout[i],items2)
#         levelWiseProducts.append(prod)

#     # print(shopLayout)
#     print(levelWiseProducts)

#     os.chdir("/home/HVZ")

#     with open("layout.txt", 'w') as file:
#         file.writelines('\t'.join(str(j) for j in i) + '\n' for i in shopLayout[i])

#     with open("items.txt", 'w') as file:
#         file.writelines('\t'.join(str(j) for j in i) + '\n' for i in levelWiseProducts)

#     updatedLevelWiseProducts = []
#     for i in range(len(shopLayout)):
#         l = []
#         for j in range(len(levelWiseProducts)):
#             crd =getPosOfNearestZ(shopLayout[i],levelWiseProducts[j])
#             if crd!="inaccessible":
#                 shopLayout[i][crd[0]][crd[1]] =1
#                 l.append([crd[0],crd[1]])
#         updatedLevelWiseProducts.append(l)
#     print(shopLayout)

#     for i in range(len(updatedLevelWiseProducts)):
#         l = []
#         for j in range(len(updatedLevelWiseProducts[i])):
#             x = []
#             for k in range(len(updatedLevelWiseProducts[i])):
#                 x.append(math.sqrt((updatedLevelWiseProducts[i][j][0] - updatedLevelWiseProducts[i][k][0])**2 + (updatedLevelWiseProducts[i][j][1]-updatedLevelWiseProducts[i][k][1])**2))
#             l.append(x)
#         visited = {}
#         count = len(l)
#         k =0
#         seq = []
#         seq.append(updatedLevelWiseProducts[i][0])
#         while count>1:
#             minVal = 10000000
#             index = -1
#             for j in range(len(l[k])):
#                 if k != j:
#                     if l[k][j] < minVal:
#                         minVal = l[k][j]
#                         index = j
#             seq.append(updatedLevelWiseProducts[i][index])
#             k = index
#             count-=1
#        return "check log"
def Cloning(li1):
    li_copy = li1[:]
    return li_copy

def getPosOfNearestZ(sl, item):
    xb = len(sl)
    yb = len(sl[0])
    print("item[0],item[1],xb and yb are: "+str([item[0],item[1],xb,yb]))
    print("item is: "+str(item))
    if valid(item[0] + 1, item[1], xb, yb) == True:
        if sl[item[0] + 1][item[1]] == '0':
            # print("in 1")
            return [item[0] + 1, item[1]]
    if valid(item[0] - 1, item[1], xb, yb) == True:
        if sl[item[0] - 1][item[1]] == '0':
            # print("in 2")
            return [item[0] - 1, item[1]]


    if valid(item[0], item[1] + 1, xb, yb) == True:
        if sl[item[0]][item[1] + 1] == '0':
            # print("in 3")
            return [item[0], item[1] + 1]
    if valid(item[0], item[1] - 1, xb, yb) == True:
        print("still here")
        if sl[item[0]][item[1] - 1] == '0':
            # print("the point: "+str(sl[item[0]][item[1]]))
            return [item[0], item[1] - 1]

    if valid(item[0]+1,item[1]+1,xb,yb)==True:
        if sl[item[0]+1][item[1]+1]=='0':
            return [item[0]+1, item[1]+1]
    if valid(item[0]+1,item[1]-1,xb,yb)==True:
        if sl[item[0]+1][item[1]-1]=='0':
            return [item[0]+1, item[1]-1]
    if valid(item[0]-1,item[1]+1,xb,yb)==True:
        if sl[item[0]-1][item[1]+1]=='0':
            return [item[0]-1, item[1]+1]
    if valid(item[0]-1,item[1]-1,xb,yb)==True:
        if sl[item[0]-1][item[1]-1]=='0':
            return [item[0]-1, item[1]-1]

    if item[0] == 0 and item[1] == 0:
        if sl[1][1] == '0':
            return [1, 1]
    if item[0] == 0 and item[1] == len(sl) - 1:
        if sl[1][len(sl) - 2] == '0':
            return [1, len(sl) - 2]
    if item[0] == len(sl) - 1 and item[1] == 0:
        if sl[len(sl) - 2][1] == '0':
            return [len(sl) - 2, 1]
    if item[0] == len(sl) - 1 and item[1] == len(sl) - 1:
        if sl[len(sl) - 2][len(sl) - 1] == '0':
            return [len(sl) - 2, len(sl) - 1]
    return "inaccessible"

def getProductsOnCurrLevel(floor,items):

    r=[]
    # print("floor is "+str(floor))

    for i in range(len(floor)):
        for j in range(len(floor[i])):
            if floor[i][j] in items.keys():
                print(floor[i][j])
                r.append([i,j])

    # print("r is "+str(r))

    return r

def valid(x,y,xb,yb):
    if x<xb and x>=0 and y<yb and y>=0:
        return True

    return False

def findNearestZeroInCol(orig,p):

    x = copy.deepcopy(p[0])
    y = copy.deepcopy(p[1])
    crdxp, crdxn, crdyp, crdyn = [], [], [], []
    dxp,dxn,dyp,dyn=0,0,0,0
    onxp,onxn,onyp,onyn=3,3,3,3

    # print("values")
    while valid(x, y, len(orig), len(orig[0])) == True and (orig[x][y] != '3' and orig[x][y] != '0'):
        # print(type(orig[x][y]))
        x += 1;

    if valid(x, y, len(orig), len(orig[0])) == True:
        dxp = abs(x - p[0])
        crdxp = [x, y]
        if orig[x][y]=='3':
            onxp =3
        if orig[x][y]=='0':
            onxp =0
    else:
        dxp = 100000000
    # print("dxp is "+str(dxp))
    x = copy.deepcopy(p[0])
    y = copy.deepcopy(p[1])

    while valid(x, y, len(orig), len(orig[0])) == True and (orig[x][y] != '3' and orig[x][y] != '0'):
        x -= 1;
    if valid(x, y, len(orig), len(orig[0])) == True:
        dxn = abs(x - p[0])
        crdxn = [x, y]
        if orig[x][y]=='3':
            onxn =3
        if orig[x][y]=='0':
            onxn =0
    else:
        dxn = 100000000

    x = copy.deepcopy(p[0])
    y = copy.deepcopy(p[1])

    while valid(x, y, len(orig), len(orig[0])) == True and (orig[x][y] != '3' and orig[x][y] != '0'):
        y += 1;
    if valid(x, y, len(orig), len(orig[0])) == True:
        dyp = abs(y - p[1])
        crdyp = [x, y]
        if orig[x][y]=='3':
            onyp =3
        if orig[x][y]=='0':
            onyp =0
    else:
        dyp = 100000000

    x = copy.deepcopy(p[0])
    y = copy.deepcopy(p[1])

    while valid(x, y, len(orig), len(orig[0])) == True and (orig[x][y] != '3' and orig[x][y] != '0'):
        y -= 1;
    if valid(x, y, len(orig), len(orig[0])) == True:
        dyn = abs(y - p[1])
        crdyn = [x, y]
        if orig[x][y]=='3':
            onyn =3
        if orig[x][y]=='0':
            onyn =0
    else:
        dyn = 100000000


    ans = min(min(dxp, dxn), min(dyp, dyn))

    if ans == 100000000:
        return "inaccessible"
    else:
        ret =0
        if ans == dxp:
            if onxp==0:
                return crdxp
            else:
                ret =dxp
        if ans == dxn:
            if onxn==0:
                return crdxn
            else:
                ret =dxn
        if ans == dyp:
            if onyp==0:
                return crdyp
            else:
                ret =dyp
        if ans == dyn:
            if onyn==0:
                return crdyn
            else:
                ret =dyn

        if ret==dxp:
            return crdxp
        if ret==dxn:
            return crdxn
        if ret==dyp:
            return crdyp
        if ret==dyn:
            return crdyn

def makeStar(dup,orig,item1,item2):
    print("instar")
    meetingPoint=[]
    path = []
    temp1 = copy.deepcopy(item1)
    temp2 = copy.deepcopy(item2)
    newPoint=[]

    if item1[0] > item2[0]:
        # whole path(basic) is highlighted with 1
        meetingPoint = [item2[0], item1[1]]
        if item1[1]<item2[1]:

            # print("meeting point is "+str(meetingPoint))
            while temp1 != meetingPoint:
                temp1[0] -= 1
                # print("point is "+str(temp1))
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[1] -= 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            print("path is "+str(path))
            # for d in orig:
            #     print(d)
            # checking if the path overlaps other elements. if so change
            for p in path:
                # print("curr point is: " + str(p))
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] == '0':
                    newPoint.append([p[0],p[1]])
                else:
                    # print("in")
                    crd = copy.deepcopy(p)
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    # print(newcrd)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

        elif item1[1]>=item2[1]:
            # print("meeting point is " + str(meetingPoint))
            while temp1 != meetingPoint:
                temp1[0] -= 1
                # print("point is " + str(temp1))
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[1] += 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            print("path is " + str(path))
            for d in orig:
                print(d)
            # checking if the path overlaps other elements. if so change
            for p in path:
                # print("curr point is: " + str(p))
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] == '0':
                    newPoint.append([p[0],p[1]])
                else:
                    # print("in")
                    crd = p
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    print(newcrd)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

    elif item1[0] < item2[0]:
        # whole path(basic) is highlighted with 1
        meetingPoint = [item1[0], item2[1]]
        if item1[1]>item2[1]:
            while temp1 != meetingPoint:
                temp1[1] -= 1
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[0] -= 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            # checking if the path overlaps other elements. if so change
            for p in path:
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] == '0':
                    newPoint.append([p[0],p[1]])
                else:
                    crd = p
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

        elif item1[1]<=item2[1]:
            while temp1 != meetingPoint:
                temp1[1] += 1
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[0] -= 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            # checking if the path overlaps other elements. if so change
            for p in path:
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] == '0':
                    newPoint.append([p[0],p[1]])
                else:
                    crd = p
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

    else:
        # whole path(basic) is highlighted with 1
        meetingPoint = temp1
        if item1[1] > item2[1]:
            while temp1 != meetingPoint:
                temp1[1] += 1
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[0] += 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            # checking if the path overlaps other elements. if so change
            for p in path:
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] != '0':
                    newPoint.append([p[0],p[1]])
                else:
                    crd = p
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

        else:
            while temp1 != meetingPoint:
                temp1[1] += 1
                dup[temp1[0]][temp1[1]] = '3'
                path.append([temp1[0], temp1[1]])

            while temp2 != meetingPoint:
                temp2[1] -= 1
                dup[temp2[0]][temp2[1]] = '3'
                path.append([temp2[0], temp2[1]])

            # print("path is " + str(path))
            # checking if the path overlaps other elements. if so change
            for p in path:
                print("curr path point: "+str(p))
                if orig[p[0]][p[1]] == '3' or orig[p[0]][p[1]] == '0':
                    newPoint.append([p[0],p[1]])
                else:
                    # print("in loop")
                    crd = copy.deepcopy(p)
                    dup[p[0]][p[1]] = orig[p[0]][p[1]]
                    newcrd = findNearestZeroInCol(orig, p)
                    if newcrd != "inaccessible":
                        dup[newcrd[0]][newcrd[1]] = '3'
                        newPoint.append([newcrd[0],newcrd[1]])
                    else:
                        dup[crd[0]][crd[1]] = orig[crd[0]][crd[1]]

    print("path is : "+str(path))
    return newPoint

def common(item1,item2):
    if (item1[0]==item2[0] and abs(item1[1]-item2[1])==1) or (item1[1]==item2[1] and abs(item1[0]-item2[0])==1) or (abs(item1[0]-item2[0])==abs(item1[1]-item2[1]) and abs(item1[0]-item2[0])==1):
        return True

    return False

@app.route('/createTSPArray',methods=['POST'])
def createTSPArray():

    items =request.form.getlist('items')
    print(items)

    items2 = {}
    for i in items:
        items2[i] =1

    # print(items2)

    shopid =request.form['shopid']

    os.chdir(app.config['UPLOAD_FOLDER'])
    # os.chdir("/uploads")
    shopLayout=[]
    starting =[]
    stairs =[]
    for file in glob.glob(str(shopid)+"*"):
        # print(file)
        df=pd.read_csv(file)
        row_list=df.values.tolist()

        for i in range(len(row_list)):
            for j in range(len(row_list[0])):
                if pd.isnull(row_list[i][j]):
                  row_list[i][j] ='0'

                if row_list[i][j]=="start":
                    starting.append([i,j])
                if row_list[i][j]=="stairs":
                    stairs.append([i,j])

        shopLayout.append(row_list)

    # print(shopLayout)
    os.chdir("/home/HVZ")
    levelWiseProducts =[]
    for i in range(len(shopLayout)):
        prod =getProductsOnCurrLevel(shopLayout[i],items2)
        if len(starting)>i:
            prod.append([starting[i][0],starting[i][1]])
        if len(stairs)>i:
            prod.append([stairs[i][0],stairs[i][1]])
        levelWiseProducts.append(prod)

    print("levelwise is: "+str(levelWiseProducts))
    updatedLevelWiseProducts = []

    for i in range(len(shopLayout)):
        l = []
        for j in range(len(levelWiseProducts[i])):

            crd = getPosOfNearestZ(shopLayout[i], levelWiseProducts[i][j])
            if crd != "inaccessible":
                shopLayout[i][crd[0]][crd[1]] = '1'
                print("crd is " + str(crd))
                l.append([crd[0], crd[1]])
            else:
                print("inaccessible")
        updatedLevelWiseProducts.append(l)


    distArray = []
    for i in range(len(updatedLevelWiseProducts)):
        l = []
        for j in range(len(updatedLevelWiseProducts[i])):
            x = []
            for k in range(len(updatedLevelWiseProducts[i])):
                x.append(math.sqrt((updatedLevelWiseProducts[i][j][0] - updatedLevelWiseProducts[i][k][0]) ** 2 + (
                        updatedLevelWiseProducts[i][j][1] - updatedLevelWiseProducts[i][k][1]) ** 2))
            l.append(x)
        distArray.append(l)

    # print(distArray)

    sequence = []
    for i in range(len(updatedLevelWiseProducts)):
        visited = {}
        seq = []
        seq.append(0)
        seq2 = []
        count = len(distArray[i])
        j = 0
        while count > 1:
            minVal = 100000
            index = -1
            for k in range(len(distArray[i])):
                if j != k:
                    if minVal > distArray[i][j][k] and (k in visited.keys()) == False:
                        index = k
                        minVal = distArray[i][j][k]

            seq.append(index)
            visited[j] = 1
            count -= 1
            j = index

        for l in range(len(seq)):
            seq2.append(updatedLevelWiseProducts[i][seq[l]])
        sequence.append(seq2)

    print("sequence is "+str(sequence))

    duplicateShopLayout = copy.deepcopy(shopLayout)
    print("")
    # for d in duplicateShopLayout[0]:
    #     print(d)

    for i in range(len(shopLayout)):
        for j in range(1,len(sequence[i])):
            print("in dbl loop")
            print("seq: "+str(sequence[i][j-1])+str(sequence[i][j]))
            np =makeStar(duplicateShopLayout[i],shopLayout[i],sequence[i][j-1],sequence[i][j])
            # compare(duplicateShopLayout[i],shopLayout[i])
            print("the newpath is: "+str(np))
            prev =np[0]
            for k in range(1,len(np)):
                if common(prev,np[k])==True: #consider diagonals also
                    prev =np[k]
                else:
                    np2= makeStar(duplicateShopLayout[i],shopLayout[i],prev,np[k])
                    prev =np[k]



    print(items2)
    print("shoplayout :")
    for d in shopLayout[0]:
        print(d)

    print("duplicateShopLayout:")
    for d in duplicateShopLayout[0]:
        print(d)

    return render_template('result.html',result=duplicateShopLayout)
    # return "check log"

###################################################################################################################################

@app.route('/shopregister')
def shopregister():
    return render_template('register.html')
#####################################################################################################################################

@app.route('/shoplogin')
def shoplogin():
    return render_template('login.html')

#####################################################################################################################################
@app.route('/verify',methods=['GET','POST'])
def verify():
    cur = mysql.connection.cursor()
    cur.execute("SELECT shopid,username FROM shop where username=%s and password=%s",(request.form['username'],request.form['password']))
    data = cur.fetchall()
    cur.close()

    if len(data)==1:
        return render_template('mainpage.html',userdata=data)
    else:
        return "<html><body>Wrong credentials.<a href='/shoplogin'>Retry</a></body></html>"

#####################################################################################################################################

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        shopid = request.form['shopid']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO shop (shopid,username, email, password) VALUES (%s,%s, %s, %s)", (shopid,username, email, password))
        mysql.connection.commit()

        return render_template('login.html')

#####################################################################################################################################
@app.route('/processcsv',methods = ['GET','POST'])
def processcsv():

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        username =request.form['username']
        shopid =request.form['shopid']
        #parse the csv files and store them in the database
        for u in uploaded_files:
            # u.save(os.path.join(app.config['UPLOAD_FOLDER'],u.filename))

            #get level
            fname =str(u.filename)
            print(type(fname))
            temp = re.findall(r'\d+', fname)
            res = list(map(int, temp))
            print(res)
            level=res[0]

            u.save(os.path.join(app.config['UPLOAD_FOLDER'],str(shopid)+"_"+str(level)+"_"+u.filename));

            df=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'],str(shopid)+"_"+str(level)+"_"+u.filename))
            row_list=df.values.tolist()

            # eliminate nan values
            for i in range(len(row_list)):
              for j in range(len(row_list[0])):
                if pd.isnull(row_list[i][j]):
                  row_list[i][j] =0;

            print(row_list)
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from items")
            data = cur.fetchall()
            cur.close()

            st_index =len(data)+1;

            for i in range(len(row_list)):
              for j in range(len(row_list[0])):
                if row_list[i][j]!=0 and row_list[i][j]!=2:

                  try:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO items (shopid,icode,iname,x,y,level) VALUES (%s,%s,%s,%s,%s,%s)", (shopid,st_index,row_list[i][j],i,j,level))
                    mysql.connection.commit()
                    st_index+=1
                  except:
                    pass

    return "Your file has been submitted to the server. Now the customers of your shop can view the shortest path.<br>To check ,Please go to starting page and choose Yes"

#####################################################################################################################################

# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record Has Been Deleted Successfully")
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
#     mysql.connection.commit()
#     return redirect(url_for('Index'))

# @app.route('/update',methods=['POST','GET'])
# def update():

#     if request.method == 'POST':
#         id_data = request.form['id']
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         cur = mysql.connection.cursor()
#         cur.execute("""
#               UPDATE students
#               SET name=%s, email=%s, phone=%s
#               WHERE id=%s
#             """, (name, email, phone, id_data))
#         flash("Data Updated Successfully")
#         mysql.connection.commit()
#         return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)