from sys import argv

# version of pycbf_test1 with write logic added
import pycbf

def to_str(s):
    if isinstance(s, bytes):
        return s.decode()
    return s

object = pycbf.cbf_handle_struct()
newobject = pycbf.cbf_handle_struct()
object.read_file(argv[1].encode(),pycbf.MSG_DIGEST)
object.rewind_datablock()
with open(argv[2],'w',newline='\n') as f:
    print("Found",object.count_datablocks(),"blocks",sep="",file=f)
    object.select_datablock(0)
    print("Zeroth is named",to_str(object.datablock_name()),sep="",file=f)
    newobject.force_new_datablock(to_str(object.datablock_name()));
    object.rewind_category()
    categories = object.count_categories()
    for i in range(categories):
        print("Category:",i,sep="", end= ' ', file=f)
        object.select_category(i)
        category_name = to_str(object.category_name())
        print("Name:",category_name,sep="", end=' ', file=f)
        newobject.new_category(category_name)
        rows=object.count_rows()
        print("Rows:",rows,sep="", end=' ', file=f)
        cols = object.count_columns()
        print("Cols:",cols,sep="",file=f)
        loop=1
        object.rewind_column()
        while loop==1:
            column_name = to_str(object.column_name())
            print("column name \"",column_name,"\"",sep="", end=' ', file=f)
            newobject.new_column(column_name)
            try:
               object.next_column()
            except:
                break
        print(file=f)
        for j in range(rows):
            object.select_row(j)
            newobject.new_row()
            object.rewind_column()
            print("row:",j,sep="",file=f)
            for k in range(cols):
                name=to_str(object.column_name())
                print("col:",name,sep="", end=' ', file=f)
                object.select_column(k)
                newobject.select_column(k)
                typeofvalue=to_str(object.get_typeofvalue())
                print("type:",typeofvalue,sep="",file=f)
                if typeofvalue.find("bnry") > -1:
                    s=object.get_integerarray_as_string()
                    print(len(s), file=f)
                    (compression, binaryid, elsize, elsigned, \
                        elunsigned, elements, minelement, maxelement, \
                        byteorder,dimfast,dimmid,dimslow,padding) = \
                        object.get_integerarrayparameters_wdims_fs()
                    if dimfast==0:
                        dimfast = 1
                    if dimmid==0:
                        dimmid = 1
                    if dimslow == 0:
                        dimslow = 1
                    print("compression: ",compression,sep="",file=f)
                    print("binaryid", binaryid, sep="", file=f)
                    print("elsize", elsize, sep="", file=f)
                    print("elsigned", elsigned, sep="", file=f)
                    print("elunsigned",elunsigned,sep="",file=f)
                    print("elements", elements, sep="", file=f)
                    print("minelement", minelement, sep="", file=f)
                    print("maxelement", maxelement, sep="", file=f)
                    print("byteorder", byteorder, sep="", file=f)
                    print("dimfast", dimfast, sep="", file=f)
                    print("dimmid", dimmid, sep="", file=f)
                    print("dimslow",dimslow,sep="",file=f)
                    print("padding", padding, sep="", file=f)
                    newobject.set_integerarray_wdims_fs(\
                      pycbf.CBF_BYTE_OFFSET,binaryid,s,elsize,elsigned,\
                      elements,byteorder,dimfast,dimmid,dimslow,padding)
                    try:
                       import numpy
                       d = numpy.frombuffer(s,numpy.uint32)
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
                    newobject.set_value(value)
                    print("Val:",value," ",i,sep="",file=f)
        print(file=f)
    del(object)
    newobject.write_widefile(argv[3].encode(),pycbf.CBF,\
        pycbf.MIME_HEADERS|pycbf.MSG_DIGEST|pycbf.PAD_4K,0)
    #
    #object.free_handle(handle)
