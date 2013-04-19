import re
import os
import sys
import pymongo


def updateMongo()

def print_details(name, listy):
    if len(listy)==0:
        return ""
    else:
        return_string = name + ':\n'
        for entry in listy:
            return_string += "    " + entry + '\n'
        return return_string

def getStuff(infile, typey): #type=1 for proc, type=2 for tables, type=3 for table types, type=4 for dependencyfile
    if 1==1:
        source_file = open(infile, "r")
        schema_group = []
        entity_group = []
        procs = []
        tts = []
        tts_def = []
        tables = []
        table_alias = []
        unks = []
        sequence = []
        procedure_defs = []
        for line in source_file.readlines():
            splitted = line.upper().rstrip("\n;").split(" ")
            if(re.match("--", line.upper())):
                continue
            schemas = re.search(r"([^ ]+)\.([A-Za-z0-9_]+)", line.upper())
            if schemas:
                if schemas.group(2).replace("\"", "") not in entity_group:
                    #print splitted
                    token_type = ""
                    try:
                        curr_index = [ i for i, word in enumerate(splitted) if word.startswith(schemas.group(1) + "." + schemas.group(2)) ][0]
                        if curr_index > 2 and (splitted[curr_index-2].replace(",", "").endswith("OUT") or splitted[curr_index-2].replace(",", "").endswith("IN")):
                                token_type = "Table type"
                        elif splitted[curr_index-1].endswith("CALL"):
                                token_type = "Procedure"
                        elif splitted[curr_index-1].endswith("TYPE"):
                            token_type = "Table type def"
                        elif splitted[curr_index-1].endswith("PROCEDURE"):
                            token_type = "ProcedureDef"
                        elif splitted[curr_index-1].endswith("JOIN") or splitted[curr_index-1].endswith("FROM") or splitted[curr_index-1].endswith("TABLE"):
                            token_type = "Table"
                        elif splitted[curr_index-1].endswith("WHERE") or splitted[curr_index-1].endswith("AND") or splitted[curr_index-1].endswith("SELECT"):
                            token_type = "Table name alias"
                        elif splitted[curr_index-1].endswith("SEQUENCE"):
                            token_type = "Sequence"
                        elif splitted[curr_index-1].endswith("INTO") and splitted[curr_index-1].endswith("INTO"):
                            token_type = "Table"
                        else:
                            token_type = "Unknown"
                    except ValueError:
                        token_type = "Unknown"
                    if token_type == "Table type":
                        tts.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "Table":
                        tables.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "Procedure":
                        procs.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "Table name alias":
                        table_alias.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "Sequence":
                        sequence.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "ProcedureDef":
                        procedure_defs.append(schemas.group(1) + "." + schemas.group(2))
                    elif token_type == "Table type def":
                        tts_def.append(schemas.group(1) + "." + schemas.group(2))
                    else:
                        unks.append(schemas.group(1) + "." + schemas.group(2))
                    schema_group.append(schemas.group(1).replace("\"", ""))
                    entity_group.append(schemas.group(2).replace("\"", ""))
        source_file.close()
        if typey==1:
            return procs
        elif typey==2:
            return tables
        elif typey==3:
            return tts
        elif typey==4:
            return sequence
        elif typey==7:
            return tts_def
        else:
            return procedure_defs

def main(config_path):
    listy = []
    defs = []
    file_list = []
    all_files = []
    exclude = []
    slash_char = ""
    types = []

    config_file = open(config_path, "r")
    for line in config_file.readlines():
	key_val = line.rstrip().split("=")
	key = key_val[0]
	val = key_val[1]
	if (key=="path"):
	    path = val
	if(key=="exlude"):
	    for entry in val.split(","):
	        exclude.append(entry)
    config_file.close()
    
    for r,d,f in os.walk(path):
        if(r.rfind("/")==-1):
            slash_char = "\\"
            indy = r.rfind("\\")
        else:
            slash_char = "/"
            indy = r.rfind("/")
        splitter = r.split(slash_char)
        cont = 0
        for direct in splitter:
            if(direct in exclude):
                   cont = 1
        if(cont==1):
            continue
        for files in f:
            if files.endswith(".sql"):
                file_list.append(os.path.join(r,files))
    for infile in file_list:
        defs.append(getStuff(infile, 5))
    return_string = "{\"data\":["
    for proc in defs:
        if len(proc) > 0:
    	    for entry in proc:
    	        return_string += "\"" + entry + "\","
    return_string = return_string.rstrip(",") + "]}"
    return return_string

main('config.txt')
