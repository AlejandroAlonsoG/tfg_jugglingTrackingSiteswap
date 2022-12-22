import sys
sys.path.insert(0, '../excel_utils')
import excel_utils

system = 'test'
ss = '3'

for i in range(1,50):
    print("i="+str(i)+": "+excel_utils.get_letter_from_id(i)[0])

book = excel_utils.book_initializer(system, ss)

excel_utils.book_writer(book,1,1,(100,100))
excel_utils.book_writer(book,1,2,(200,200))
excel_utils.book_writer(book,1,3,(300,300))

excel_utils.book_writer(book,2,1,(105,100))
excel_utils.book_writer(book,2,2,(100,200))
excel_utils.book_writer(book,2,3,(300,100))

excel_utils.book_writer(book,3,1,(110,15))
excel_utils.book_writer(book,3,2,(200,100))
excel_utils.book_writer(book,3,3,(100,300))
excel_utils.book_writer(book,3,4,(400,400))

excel_utils.book_saver(book, system, ss)
