from openpyxl import Workbook

info_name = 'Info'
tracking_name = 'Tracking'
save_dir = '/media/alex/ELISA_DD/TFG/AlejandroAlonso/results/'

def book_initializer(system: str, ss:str) -> Workbook:
    book = Workbook()

    sheet_info = book.create_sheet(info_name)
    sheet_tracking = book.create_sheet(tracking_name)
    del book['Sheet']

    sheet_info['B2'] = 'Sistema:'
    sheet_info['C2'] = system
    sheet_info['B3'] = 'SS:'
    sheet_info['C3'] = ss
    sheet_info['B4'] = 'Num bolas:'
    sheet_info['C4'] = 'TODO'
    # TODO Añadir mas info?

    sheet_tracking.merge_cells('A1:A2')
    sheet_tracking['A1'] = 'Frame'

    return book

def obtain_column_name(num: str) -> str:
  letters = ""
  # Add 1 so that A is index 0
  num += 1
  # Convert number to stirng, every 26 values start over
  while num > 0:
    num -= 1
    letters = chr(num % 26 + 65) + letters
    num //= 26
 
  # Base case
  if len(letters) == 0:
    return "A"
 
  return letters

# Obtains the tuple represented by the ball's id
def get_column_tuple_from_id(id: int) -> tuple[str,str]:
    return obtain_column_name(id*2-1), obtain_column_name(id*2)

def book_writer(book: Workbook, frame: int, id: int, coords: tuple[int, int]):
    sheetTracking = book[tracking_name]
    letter_1,letter_2 = get_column_tuple_from_id(id)


    if not sheetTracking[letter_1+'1'].value:
        sheetTracking.merge_cells(letter_1+'1:'+letter_2+'1')
        sheetTracking[letter_1+'1'] = f'Bola num {id}'
        sheetTracking[letter_1+'2'] = 'X'
        sheetTracking[letter_2+'2'] = 'Y'
    # TODO Igual hacer que si no se ha detectado alguna bola se ponga un guion en la fila o algo asi?
    sheetTracking[f'A{frame+2}'] = frame
    sheetTracking[letter_1+f'{frame+2}'] = coords[0]
    sheetTracking[letter_2+f'{frame+2}'] = coords[1]

def book_saver(book: Workbook, system: str, ss:str, sanitize: bool):
    if sanitize:
        book_sanitizer(book)
    book.save(f'{save_dir}tracking_{ss}_{system}.xlsx')
    print("Book "+ f'tracking_{ss}_{system}.xlsx' +" successfully saved in: "+ save_dir)

def book_sanitizer(book: Workbook):
    count = 3
    while not book[tracking_name][f'A{count}'].value:
        count += 1
    book[tracking_name].delete_rows(3,count-3)
    print("Book sanitized, ", count-3, " rows deleted")