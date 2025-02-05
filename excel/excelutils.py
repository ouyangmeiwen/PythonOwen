#pip install openpyxl
import os
import pandas as pd
from typing import Tuple, Dict

# 确保当前工作目录是脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ExcelUtils:
    def readExcel(Path)-> Tuple[Dict[str, str], Dict[int, str]]:
        df = pd.read_excel(Path)
        for row in df.itertuples(index=False, name='Row'):
            dic_name=dict() 
            dic_index=dict()
            index=1
            for column in df.columns:
                try:
                    value=getattr(row, column)
                    dic_name[column]=value
                    dic_index[index]=value
                except:
                    print(column+'不存在')
                index=index+1
            #print(dic_name)
            #print(dic_index)
            break  #只打印一行测试书
        return dic_name,dic_index
    
if __name__ == "__main__":
    #ExcelUtils.readExcel("/home/owen/Github/django/server/test/excel/20241020在架图书数据V4.xlsx")
    dic_name, dic_index = ExcelUtils.readExcel("20241020在架图书数据V4.xlsx")
    print("处理结束")
    print("dic_name:", dic_name)
    print("dic_index:", dic_index)