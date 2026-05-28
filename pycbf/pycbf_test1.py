from sys import argv

import pycbf

def to_str(s):
    if isinstance(s, bytes):
        return s.decode()
    return s

object = pycbf.cbf_handle_struct() # FIXME
object.read_file(argv[1].encode(),pycbf.MSG_DIGEST)
object.rewind_datablock()
with open(argv[2],'w',newline='\n') as f:
    print("Found",object.count_datablocks(),"blocks",sep="",file=f)
    object.select_datablock(0)
    print("Zeroth is named",to_str(object.datablock_name()),sep="",file=f)
    object.rewind_category()
    categories = object.count_categories()
    for i in range(categories):
        print("Category:",i,sep="", end=' ', file=f)
        object.select_category(i)
        category_name = to_str(object.category_name())
        print("Name:",category_name,sep="", end=' ', file=f)
        rows=object.count_rows()
        print("Rows:",rows,sep="", end=' ', file=f)
        cols = object.count_columns()
        print("Cols:",cols,sep="",file=f)
        loop=1
        object.rewind_column()
        while loop==1:
            column_name = to_str(object.column_name())
            print("column name \"",column_name,"\"",sep="", end=' ', file=f)
            try:
               object.next_column()
            except:
               break
        for j in range(rows):
            object.select_row(j)
            object.rewind_column()
            if j==0: print(file=f)
            print("row:",j,sep="",file=f)
            for k in range(cols):
                name=to_str(object.column_name())
                print("col:",name,sep="", end=' ', file=f)
                object.select_column(k)
                typeofvalue=to_str(object.get_typeofvalue())
                print("type:",typeofvalue,sep="",file=f)
                if typeofvalue.find("bnry") > -1:
                    s=object.get_integerarray_as_string()
                    print(len(s), file=f)
                    try:
                       import numpy
                       d = numpy.frombuffer(bytes(s),numpy.uint32)
                       # Hard wired Unsigned Int32
                       print(d.shape, file=f)
                       print(d[0:10],d[int(d.shape[0]/2)],d[len(d)-1],file=f)
                       print(d[int(d.shape[0]/3):int(d.shape[0]/3+20)], file=f)
                       d=numpy.reshape(d,(2300,2300))
    #                   from matplotlib import pylab
    #                   pylab.imshow(d,vmin=0,vmax=1000)
    #                   pylab.show()
                    except ImportError:
                       print("You need to get numpy and matplotlib to see the data", file=f)
                else:
                    value=to_str(object.get_value())
                    print("Val:",value," ",i,sep="",file=f)
        print(file=f)
    del(object)
    #
    #object.free_handle(handle)
