from textnode import TextNode, TextType
import os
import shutil
from helper import generate_pages_recursive, copy_files_recursive
import sys

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    p = "./docs"
    s = "./static"
    deleter(p)
    copy_files_recursive(s, p)

    generate_pages_recursive("content", "template.html", "docs", basepath)

def deleter(public):

    if os.path.exists(public):
        path_ls = os.listdir(public)
                
        for path in path_ls:
            temp_path = f"{public}/{path}"
            if os.path.isfile(temp_path):
                os.remove(temp_path)
            else:
                shutil.rmtree(temp_path)
                
    else:
        os.mkdir(public)

# def copy_recurs(public, static):
#     static_list = os.listdir(static)
#     for stat in static_list:
#         temp_stat = f"{static}/{stat}"
#         if os.path.isfile(temp_stat):
#             #print(temp_stat)
#             to_move = temp_stat.replace("static", "public")
#             #print(to_move)
#             dir_to_move = to_move.rsplit("/", 1)[0]
#             #print(dir_to_move)
#             if os.path.exists(dir_to_move):
#                 shutil.copy(temp_stat, dir_to_move)
#             else:
#                 #print("making it")
#                 os.mkdir(dir_to_move)
#                 #print("and now moving it")
#                 shutil.copy(temp_stat, dir_to_move)
#         else:
#             copy_recurs(public, temp_stat)




main()