
def show(s):
    print(s)
    show_info()

def show_info(s = ''):
    hello()

def hello():
    import inspect
    frame,filename,line_number,function_name,lines,index = inspect.stack()[2]
    print(frame)

def show_info2():
    from inspect import currentframe, getframeinfo
    frameinfo = getframeinfo(currentframe())
    print(frameinfo.filename, frameinfo.lineno)
