import sys
import openpyxl
import excel_utils as eu

""" system = 'test'
ss = '3'
book = eu.book_initializer(system, ss)
with open("demofile2.txt", "r") as infile:
    for data in infile:
        frame, id, position= data.split("|")[0],data.split("|")[1],data.split("|")[2]
        coord_x = position.split(", ")[0][1:]
        coord_y = position.split(", ")[1][:-2]
        print(int(frame)+1)
        eu.book_writer(book, int(frame)+1, int(id), (int(coord_x), int(coord_y)))
eu.book_saver(book,system, ss) """

""" data = eu.load_data('/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/tracking_5_AlejandroAlonso_red.xlsx')
print(data) """

book = openpyxl.load_workbook("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_5_bartonski.xlsx")

eu.denoise(book)

eu.book_saver(book, "denoise", "short")
