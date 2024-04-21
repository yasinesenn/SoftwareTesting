import YazilimTest.gitOperations
import re
import os
from javalang import tree,parse,parser
from javalang.tree import Node

from .models import JavaClass
# GitHub reposu URL'si


singleLineComment = r"\/\/.*$"
multiLineComment = "/[*][^*][\\s\\S]*?[*]/"
javaDoc = "/[*]{2}[\\s\\S]*?[*]/"




def getSingleLine_Count(str_data):
        single_line_count = len(re.findall(singleLineComment, str_data, re.MULTILINE))
        return single_line_count

def getMultiLine_Count(str_data):
        multi_line_count = len(re.findall(multiLineComment, str_data, re.MULTILINE))
        return multi_line_count

def getJavadoc_Count(str_data):
        java_doc_count = len(re.findall(javaDoc, str_data, re.MULTILINE))
        java_doc_comments = re.findall(javaDoc, str_data, re.MULTILINE)
        java_doc_line_count = sum(1 for comment in java_doc_comments for line in comment.split('\n') if line.strip())
        java_doc_line_count -= java_doc_count*2
        return java_doc_line_count

def getAllLines_Count(str_data):
        return len(str_data.split("\n"))-1

def codeLine_Counter(str_data):

        regex = r"(\/\*[\s\S]*?\*\/)|(\/\/.*)|^\s*\n"
        subst = ""

        cleaned_content = re.sub(regex, subst, str_data, 0, re.MULTILINE)
        cleaned_content = re.sub(r"^\s*\n", "", cleaned_content, flags=re.MULTILINE)
    
        remaining_lines = len(cleaned_content.split('\n'))-1
        #print(cleaned_content)

        return remaining_lines


            
def getCommentDeviation_Perc(javadoc, comment, functionCount, codeLines):
    if functionCount <= 0 or codeLines <= 0:
        return 0  # Eğer functionCount veya codeLines sıfıra eşit veya daha küçükse, sonucu sıfır olarak döndür

    yg = ((javadoc + comment) * 0.8) / functionCount
    yh = (codeLines / functionCount) * 0.3
    
    return ((100 * yg) / yh) - 100
     

def find_function_comments(githubDepo,class_name,functionCount,str_data):

        
    function_single = getSingleLine_Count(str_data)
    function_multi = getMultiLine_Count(str_data)
    singlewithMulti = function_single+function_multi
    code_lines_count = codeLine_Counter(str_data)
    loc_Count = getAllLines_Count(str_data)
    function_java_doc = getJavadoc_Count(str_data)
    yorumSapma = getCommentDeviation_Perc(function_java_doc,singlewithMulti,functionCount,code_lines_count)


    return JavaClass(github_repo=githubDepo,class_name=class_name,javadoc_lines_count=function_java_doc,comment_lines_count=singlewithMulti,code_line_count=code_lines_count,loc_count=loc_Count,function_count=functionCount,comment_deviation_perc=yorumSapma)

def getAlllines_Count(str_data):
        return len(str_data.split("\n"))

def readWithpath(file_path):
    try:
        with open(file_path, 'r') as file:
            pathCode = file.read()
            return pathCode
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {file_path}")
        return None
    

def read_Java_Files(githubDepo,directory):
    YazilimTest.gitOperations.allOperations(githubDepo.url)
    java_files_content = {}
    parsed_class_content = {}
    javaModels = []

    commentLines_Count = 0
    javadocLines_Count = 0
    codeLine_Count = 0
    function_Count = 0
    Loc_Count = 0
    commentDeviation_Perc = 0


    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as java_file:
                    java_files_content[file_path] = java_file.read()
                    try:
                        commentLines_Count = 0
                        javadocLines_Count = 0
                        codeLine_Count = 0
                        function_Count = 0
                        Loc_Count = 0
                        commentDeviation_Perc = 0

                        parsed_code = parse.parse(java_files_content[file_path])  
                        for path, node in parsed_code.filter(tree.ClassDeclaration):
                            class_name = node.name
                            parsed_class_content[file_path] = java_files_content[file_path]
                        
                            function_counter = 0 
                            for member in node.body:
                                if isinstance(member, tree.MethodDeclaration) or isinstance(member, tree.ConstructorDeclaration):
                                    function_counter += 1

                            tmpModel = find_function_comments(githubDepo,class_name,function_counter,parsed_class_content[file_path])
                            tmpModel.save()
                            javaModels.append(tmpModel)
                            
                         
                            break  # İlk sınıfı bulduğumuzda döngüden çıkalım
                    except Exception as e:
                        print('Pars Etme Hatası:', e)

    return javaModels

    