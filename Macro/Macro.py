
#格式1
opcode_one={"FIX":"C4","FLOAT":"C0","HIO":"F4","NORM":"C8","SIO":"F0","TIO":"F8"}
#格式2
opcode_two={"ADDR":"90","CLEAR":"B4","COMPR":"A0","DIVR":"9C","MULR":"98","RMO":"AC","SHIFTL":"A4",
            "SHIFTR":"A8","SUBR":"94","SVC":"B0","TIXR":"B8"}    
#格式3/4
opcode_three_four={"ADD":"18","ADDF":"58","AND":"40","COMP":"28","COMPF":"88","DIV":"24","DIVF":"64",
                   "J":"3C","JEQ":"30","JGT":"34","JLT":"38","JSUB":"48","LDA":"00","LDB":"68","LDCH":"50",
                   "LDF":"70","LDL":"08","LDS":"6C","LDT":"74","LDX":"04","LPS":"D0","MUL":"20","MULF":"60",
                   "OR":"44","RD":"D8","RSUB":"4C","SSK":"EC","STA":"0C","STB":"78","STCH":"54","STF":"80",
                   "STI":"D4","STL":"14","STS":"7C","STSW":"E8","STT":"84","STX":"10","SUB":"1C",
                   "SUBF":"5C","TD":"E0","TIX":"2C","WD":"DC"}

#虛指令判斷
def directive(col):
    if(col=="START"):
        return "START"
    elif(col == "BASE"):
        return "BASE"
    elif(col == "BYTE"):
        return "BYTE"
    elif(col == "WORD"):
        return "WORD"
    elif(col == "RESW"):
        return "RESW"
    elif(col == "RESB"):
        return "RESB"
    elif(col == "END"):
        return "END"
    elif(col=="MACRO"):
        return "MACRO"
    elif(col=="MEND"):
        return "MEND"
    else:
        return False
#檔案讀取
def read_file(data_name,arr = []):
    with open(data_name,"r",encoding="utf-8-sig") as fp:
        row = fp.readlines()
        for index_row,line in enumerate(row):
            line_strip = line.strip("\n")
            line_split = line_strip.split()
            #動態增加行數
            arr.append([])
            #取出分割後一個一個的字串
            for index,row_per in enumerate(line_split):
                #根據所在行數 動態新增 所分割後得到的字串            
                arr[index_row].append(row_per)
    fp.close()
#重新整合
def reshape_arr(one_d_arr=[],re_arr=[],arr=[[]]):
    #先將全部的指令存到一個新的1維陣列
    for index_row,row in enumerate(arr):
        #如果row裡面有值 且="." 代表是註解不用理他
        if(len(row)>0):
            if(row[0]=="."):
                continue                
        for index_col,col in enumerate(row):           
            if(col=="RSUB" or col=="MEND"):
                one_d_arr.append(col)
                one_d_arr.append("")
            else:
                one_d_arr.append(col)    
                
    for index,per in enumerate(one_d_arr):
        #將MARCO加入字典，當作是一個新指令
        if(per=="MACRO"):
            keep_marco_name.setdefault(one_d_arr[index-1])  
        #為了讓 opcode前面有+號的也能夠讀進去
        per = per.strip('+')   
        #如果讀到的字串 是虛指令或是有在opcode_dic中的指令
        if(directive(per)!=False or per in opcode_one or per in opcode_two or per in opcode_three_four or per in keep_marco_name):
            
            now_per = one_d_arr[index]
            next_per = one_d_arr[index+1]
            #如果現在是RSUB，則指將其陣列改為0 ， 因為RSUB沒有運算元 MEND也是
            if(now_per == "RSUB"):
                one_d_arr[index]='0'
            elif(now_per=="MEND"):
                one_d_arr[index]='0'
            #其餘的都有運算元，所以將本身和下一個改成0
            else:
                one_d_arr[index]='0'
                one_d_arr[index+1]='0'
            
            #當目前的前一個不為0時，代表是symbol
            if(one_d_arr[index-1]!='0'):  
                #RSUB因沒運算元 所以 append 0,RSUB,0
                if(now_per == "RSUB" or now_per == "MEND"):
                    re_arr.append(['',now_per,''])
                # symbol(上一個)、當前、下一個 一起append
                else:            
                    re_arr.append([one_d_arr[index-1],now_per,next_per])
            #其他代表沒有symbol
            else:
                re_arr.append(["",now_per,next_per])

#紀錄marco 並刪除re_arr中marco的部分
def keep_marco(keep_marco_ins=[],re_arr=[[]]):
    marco = False
    for index_row,row in enumerate(re_arr):        
        if(row[1]=="MACRO"):
            marco=True
        if(marco==True):
            keep_marco_ins.append(row)
        if(row[1]=="MEND"):
            marco=False
    for index_row,row in enumerate(keep_marco_ins):
        if (row in re_arr):
            re_arr.remove(row)


#尋找該聚集名稱的全部指令
def marco_search(marco_name,parameter,keep_marco_ins=[[]]):
    marco = False
    array=[]
    #判斷該聚集指令所在陣列的範圍
    for index_row,row_ in enumerate(keep_marco_ins):
        if(marco_name in row_):
            marco = True
        if(marco==True):
            #要記得用copy不然會參照到同一個內容 導致改一個其他就跟著改
            temp = row_.copy()
            array.append(temp)
        if(row_[1] == "MEND"):
            marco = False
    #將marco參數 替換    
    marco_parameter = array[0][2].split(",")
    for index_row2,row2 in enumerate(array):       
        if(row2[1]=="MACRO" or row2[1]=="MEND"):
            array.remove(row2)
        else:          
            for i in range(len(marco_parameter)):                
                row2[2] = row2[2].replace(marco_parameter[i],parameter[i])
    return array 
#展開
def expend(row=[],return_arr=[[]]):

    expend_arr = []
    keep=[]
    #如果有symbol要保留 
    if(row[0]!=""):
        keep.append(row[0])
        keep.append(return_arr[0][1])
        keep.append(return_arr[0][2])
    else:
        keep.append(return_arr[0][0])
        keep.append(return_arr[0][1])
        keep.append(return_arr[0][2])
        
    #將一筆一筆加入回傳的陣列
    for index_row,row in enumerate(return_arr):
        if(index_row==0):
            expend_arr.append(keep)
        else:
            expend_arr.append(row)


    return expend_arr
    
#找到marco指令 並進行參數代換
def marco_replace(keep_marco_ins=[[]],re_arr=[[]],ans=[],rrr=[]):
    
    for index_row,row in enumerate(re_arr):
        
        #先找到marco指令 並將其後面的參數找出來
        if(row[1] in keep_marco_name):
            parameter = row[2].split(",")
            #在儲存marco的List 找到符合該聚集名稱的地方
            return_arr = marco_search(row[1],parameter,keep_marco_ins)           
            expend_arr = expend(row,return_arr)

            #print(expend_arr)
            for i,per_row in enumerate(expend_arr):
                ans.append(per_row)
        else:
            ans.append(row)
    return ans           
#印出來
def print_ans(re_arr=[[]]):
    for index_row,row in enumerate(re_arr):
        for index_col,col in enumerate(row):     
            if(index_col==len(re_arr[index_row])-1):   
                print('%-13s' % re_arr[index_row][index_col])
            else:
                print('%-13s' % re_arr[index_row][index_col],end="")            
                       
'''主程式 '''
keep_marco_name = {}
keep_marco_ins = []              
arr = []
one_d_arr=[]
re_arr = []

ans =[]
data_name = "MACRO.txt"
read_file(data_name,arr)
reshape_arr(one_d_arr,re_arr,arr)

keep_marco(keep_marco_ins,re_arr)
marco_replace(keep_marco_ins,re_arr,ans)
print_ans(ans)