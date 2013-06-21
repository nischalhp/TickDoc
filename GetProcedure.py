def show_tomdoc(path):
    print 
    procedure_file = open(path)
    comment = ""
    print path
    for line in procedure_file.readlines():
        if line.lstrip().startswith('--'):
            comment += line.lstrip('- \t').rstrip() + "\n"
        else:
            break
    return comment

