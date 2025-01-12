from os import system
from typing import Iterable, Any, Hashable
from tkinter import *
from tkinter import ttk, font, filedialog
from tkinter.ttk import Treeview, Style
from tkinter.messagebox import askyesno, showinfo, showerror
from BL.mini_bl import get_data, search_std, edit_std, create_std, age, delete_std, source_path, create_backup, clear_database

# region Common
widgets = []
pad = 10

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
    return filename      

def show_error(messages: dict):
    list = []

    for field, err in messages.items():
        list.append(f"{field} Error > {err}")

    showerror("ERROR", "\n".join(list))


def show_success(message: str):
    showinfo(title='SUCCESS', message=f"{message}")

def extract():
    result = get_data(r'notes.data_source')

    if not result['SUCCESS']:
        show_error(result['ERR_MSG'])
        return []
    return result['RETURN']


def _isvalid(student: dict):
    """_summary_

    Args:
        student (dict): _description_
        items (Iterable): _description_

    Returns:
        _type_: _description_
    """

    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    if not student['name']:
        function_result['ERR_MSG']['name'] = 'Name column is empty'
    elif not student['name'].isalpha():
        function_result['ERR_MSG']['name'] = 'Name is not alphabet'

    if not student['family']:
        function_result['ERR_MSG']['family'] = 'Family column is empty'
    elif not student['family'].isalpha():
        function_result['ERR_MSG']['family'] = 'Famlily is not alphabet'

    if not student['gender']:
        function_result['ERR_MSG']['gender'] = 'Gender is empty'
    elif student['gender'] not in ('male', 'female', 'other'):
        function_result['ERR_MSG']['gender'] = 'unvalid gender'

    if not student['stcode']:
        function_result['ERR_MSG']['stcode'] = 'Student Code is empty'
    elif len(student['stcode']) != 12:
        function_result['ERR_MSG']['stcode'] = 'Student Code must be 12 digits'
    if not student['stcode'].isdecimal():
        function_result['ERR_MSG']['stcode'] = 'Student Code must contain digits only'

    if not student['ncode']:
        function_result['ERR_MSG']['ncode'] = 'National Code is empty'
    elif len(student['ncode']) != 11:
        function_result['ERR_MSG']['ncode'] = 'Nantionl Code must be 11 digits'
    elif not student['ncode'].isdecimal():
        function_result['ERR_MSG']['ncode'] = 'National Code must contain digits only'

    if not student['birth']:
        function_result['ERR_MSG']['birth'] = 'Birth is empty'
    elif age(student['birth']) not in range(8, 120):
        function_result['ERR_MSG']['birth'] = 'Age is not in valid range\n(must be between 8 and 120)'
    elif not student['birth'].isdecimal():
        function_result['ERR_MSG']['birth'] = 'Birth must contain digits only'

    if function_result['ERR_MSG']:
        function_result['SUCCESS'] = False

    return function_result

def search_code(stcode: str = None, ncode: str = None):
    
    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    if not (stcode or ncode):
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['ENTRY'] = 'At least one entry is required'
        return function_result
    
    if ncode:
        if len(ncode) != 11:
            function_result['SUCCESS'] = False
            function_result['ERR_MSG']['NCODE'] = 'Nantionl Code must be 11 digits'
        if not ncode.isdecimal():
            function_result['SUCCESS'] = False
            function_result['ERR_MSG']['NCODE'] = 'National Code must contain digits only'
        
        if function_result['SUCCESS']:
            result = search_std(key='ncode', value=ncode)
            if not result['SUCCESS']:
                function_result['SUCCESS'] = False
                function_result['ERR_MSG'] = result['ERR_MSG']
                return function_result
            function_result['RETURN'] = result['RETURN']
    if stcode:
        if len(stcode) != 12:
            function_result['SUCCESS'] = False
            function_result['ERR_MSG']['STCODE'] = 'Student Code must be 12 digits'
        if not stcode.isdecimal():
            function_result['SUCCESS'] = False
            function_result['ERR_MSG']['STCODE'] = 'Student Code must contain digits only'
        
        if function_result['SUCCESS']:
            result = search_std(key= 'stcode', value=stcode)
            if not result['SUCCESS']:
                function_result['SUCCESS'] = False
                function_result['ERR_MSG'] = result['ERR_MSG']
                return function_result

            if not function_result['RETURN'] == result['RETURN']:
                function_result['SUCCESS'] = False
                function_result['ERR_MSG']['SEARCH'] = 'Student code and national code do not match.'
                return function_result    
            function_result['RETURN'] = result['RETURN']
    
    return function_result
            
def Student(values: Iterable[str]):
    keys = ['name', 'family', 'gender', 'birth', 'ncode', 'stcode']
    return {f'{key}': f'{value}' for key, value in zip(keys, values)}
        
# endregion

# region Top-Levels

# region Entry

def _entry_form(table, dark, theme, mode = 'add', selected = None):

    # region Entry Initilazation
    entry_form = Toplevel()
    entry_width, entry_height = 450, 580
    entry_x_coordinate = int(
        (entry_form.winfo_screenwidth()/2) - (entry_width/2))
    entry_y_coordinate = int(
        (entry_form.winfo_screenheight()/2) - (entry_height/2))
    entry_form.geometry(
        f'{entry_width}x{entry_height}+{entry_x_coordinate}+{entry_y_coordinate}')
    entry_form.resizable(width=False, height=False)
    entry_form.title('Student Entry')
    widgets.append(entry_form)
    entry_form.wm_iconphoto(False, theme['main_image'])


    # endregion

    #region Entry Theme

    colors = {
        'dark': dark,
        'bg': '#ffffff',
        'div': '#d3d3d3',
        'txt': '#3a3a3a',
        'btn_bg': '#f7f7f7',
        'btn_active_bg': '#c7c7c7'
    }

    if not colors['dark']:
        colors['dark'] = False
        colors['bg'] = '#ffffff'
        colors['div'] = '#d3d3d3'
        colors['txt'] = '#3a3a3a'
        colors['btn_bg'] = '#f7f7f7'
        colors['btn_active_bg'] = '#c7c7c7'

    else:
        colors['dark'] = True
        colors['bg'] = '#000000'
        colors['div'] = '#303030'
        colors['txt'] = '#ffffff'
        colors['btn_bg'] = '#494949'
        colors['btn_active_bg'] = '#1b1b1b'

    def apply_theme():

        entry_form.config(bg=colors['bg'])

        style = ttk.Style(master=entry_form)
        style.theme_use('default')

        style.configure(
            'Large.TRadiobutton',
            background=colors['div'],
            foreground=colors['txt'],
            fieldbackground=colors['div'],
            rowheight=25,
            bd=0,
            relief=FLAT
        )

        style.configure(
            'TCombobox',
            background = colors['bg'],
            foreground = colors['txt'],
            fieldbackground=colors['bg'],
            rowheight=25,
            bd=0,
            highlightthickness=0,
            relief=FLAT
        )


        for widget in widgets:
            try:
                widget_type = widget.winfo_class()
                if widget_type == 'Frame':
                    widget.config(bg=colors['div'])
                elif widget_type == 'Label':
                    widget.config(bg=colors['div'], fg=colors['txt'])
                elif widget_type == 'Button':
                    widget.config(bg=colors['btn_bg'],
                                activebackground=colors['btn_active_bg'])
                elif widget_type == 'Toplevel':
                    widget.config(bg=colors['bg'])
                elif widget_type == 'Tk':
                    widget.config(bg=colors['bg'])
            except TclError:
                pass
    #endregion

    # region Rntry Header

    entry_header = Frame(
        master=entry_form,
        height=100
    )
    entry_header.pack(side=TOP, fill=X, padx=pad, pady=pad)
    entry_header.propagate(False)
    widgets.append(entry_header)

    entry_image = PhotoImage(file=r'icons\add.png')
    entry_pic = Label(master=entry_header, image=entry_image)
    entry_pic.pack(side=LEFT, padx=pad)
    widgets.append(entry_pic)

    entry_title = Label(
        master=entry_header,
        text='Entry Form',
        font=theme['title_font']
    )
    entry_title.pack(side=LEFT, padx=pad)
    widgets.append(entry_title)

    # endregion

    # region Entry Body


    label_font = ("Cambria", 15, "bold")
    label_width = 6

    entry_body = Frame(
        master=entry_form,
    )
    entry_body.pack(side=TOP, fill=BOTH, padx=pad, pady=pad, expand=True)
    widgets.append(entry_body)


    # region Profile Selection


    picture_select = Frame(master= entry_body)
    picture_select.pack(
        side= TOP,
        fill= X,
        expand= True,
        padx= pad,
        pady= 0
    )
    widgets.append(picture_select)

    picture = Label(master= picture_select)
    picture.pack(side= TOP, pady= pad, padx= pad)
    widgets.append(picture)

    # endregion
    
    # region Data Entry
    student = {
        'name' : '',
        'family' : '',
        'gender' : 'other',
        'birth' : '',
        'ncode' : '11 Digits',
        'stcode' : '12 Digits'
    }

    if mode == 'edit':
        student = new_student = {key: value for key, value in zip(student.keys(),table.item(table.selection()[0])['values'])}
        print(f'\n{student}')
            
    variables = {
        key: StringVar(value=value) for key,value in student.items()
    }

    frames = {
        key: Frame(master= entry_body) for key in student.keys()
    }

    labels = {
        key: Label(
            master=frames[key],
            text=key,
            font=label_font,
            anchor=W,
            width=label_width
        )

        for key in student.keys()
    }

    for key in student.keys():
        frames[key].pack(side=TOP, fill=X, pady= (1,5))
        labels[key].pack(side=LEFT, padx=pad)
        widgets.append(frames[key])
        widgets.append(labels[key])

    entries = {
        key : {
            'master': frames[key],
            'textvariable': variables[key]
        }
        for key in student.keys()
    }


    # endregion

    img_male = PhotoImage(file = r'icons\profile_m.png')
    img_female = PhotoImage(file = r'icons\profile_f.png')
    img_other = PhotoImage(file = r'icons\profile_o.png')

    def pic_update():
        
        match variables['gender'].get():

            case 'male':
                image = img_male

            case 'female':
                image = img_female
            case _:
                image = img_other

        picture.configure(image=image)
    
    pic_update()

    entry_list = {}
    
    for key, value in entries.items():
        if key == 'gender':
            entry_list[f'{key}_male'] = ttk.Radiobutton(
                master=value['master'],
                text='Male',
                variable=value['textvariable'],
                value='male',
                style='Large.TRadiobutton',
                command= pic_update
            )
            widgets.append(entry_list[f'{key}_male'])
            entry_list[f'{key}_male'].pack(side = LEFT, padx= 2*pad)

            entry_list[f'{key}_female'] = ttk.Radiobutton(
                master=value['master'],
                text= 'Female',
                variable=value['textvariable'],
                value= 'female',
                style='Large.TRadiobutton',
                command= pic_update
            )
            widgets.append(entry_list[f'{key}_female'])
            entry_list[f'{key}_female'].pack(side = LEFT, padx= pad)

            entry_list[f'{key}_other'] = ttk.Radiobutton(
                master=value['master'],
                text= 'Other',
                variable=value['textvariable'],
                value= 'other',
                style='Large.TRadiobutton',
                command= pic_update
            )
            widgets.append(entry_list[f'{key}_other'])
            entry_list[f'{key}_other'].pack(side = LEFT, padx= pad)
        elif key == 'birth':

            # Generate the list of years from the last 120 years
            years = [str(year) for year in range(2023, 2023-120, -1)]
            year_menu = ttk.Combobox(
                value['master'],
                textvariable=value['textvariable'],
                values=years,
                style='TCombobox'
            )
            year_menu.pack(pady=pad, padx = (0,pad), fill= X)
            widgets.append(year_menu)
        
        else:
            entry_list[key] = Entry(
                master=value['master'],
                font=theme['entry_font'],
                highlightthickness= 2,
                highlightbackground= colors['div'],
                highlightcolor='#0059ff',
                insertbackground= colors['txt'],
                bg=colors['bg'],
                fg=colors['txt'],
                textvariable=value['textvariable'],
                width=100,
                relief = FLAT
            )
            # widgets.append(entry_list[key])
            entry_list[key].pack(fill=BOTH, padx= (0,pad))

    # endregion

    # region Entry Footer

    entry_footer = Frame(master=entry_form, height=70)
    entry_footer.pack(side='bottom', fill=X, padx=pad, pady=pad)
    entry_footer.propagate(False)
    widgets.append(entry_footer)

    def back():
        entry_form.quit()
        entry_form.destroy()
        # form.deiconify()

    btn_back = Button(
        text='BACK',
        image=theme['back_btn_image'],
        font=theme['btn_font'],
        master=entry_footer,
        command=back, 
        bg='#ff002b',
        activebackground='#dd0327',
        foreground='#ffffff',
        compound=LEFT,
        relief=FLAT,
        width=140
    )
    btn_back.pack(side=LEFT, padx=pad, pady= pad)

    # confirm_image = PhotoImage(file=r'icons\btn_confirm.png')

    def confirm(student = student, new_student = new_student if mode == 'edit' else None, mode = mode):
        
        # function_result = {
        #     'SUCCESS': True,
        #     'ERR_MSG': {},
        #     'SUC_MSG': {},
        #     'RETURN': None
        # }

        student = {
            key : variables[key].get()
            for key in student.keys()
        }

        result = _isvalid(student=student)

        if not result['SUCCESS']:
            for key, value in entries.items():
                if key in result['ERR_MSG']:
                    value['textvariable'].set('')
            show_error(result['ERR_MSG'])
            
        elif mode == 'add':
            result = create_std(student=student)
            if not result['SUCCESS']:
                show_error(messages=result['ERR_MSG'])
                return None
            show_success(message=result['SUC_MSG'])

            table.insert('', END, values=list(student.values()))
            for value in entries.values():
                value['textvariable'].set('')
        
        else:
            result = edit_std(student=student)
            if not result['SUCCESS']:
                show_error(messages=result['ERR_MSG'])
                return None
            show_success(message=result['SUC_MSG'])
            
            table.delete(selected)
            table.insert('', END, values=list(student.values()))
            return None
            
            


    btn_confirm = Button(
        text='CONFIRM',
        image=theme['confirm_btn_image'],
        font=theme['btn_font'],
        master=entry_footer,
        command=confirm,
        bg='#0066ff',
        activebackground='#0058dd',
        foreground='#ffffff',
        compound=LEFT,
        relief=FLAT,
        width=170
    )
    
    btn_confirm.pack(side=RIGHT, padx=pad, pady= pad)

    # endregion

    apply_theme()
    entry_form.mainloop()

# endregion

# region Search Bar

def _search_form(dark, theme):

    search_form = Toplevel()
    search_form.title('Search')
    search_form.resizable(width=False, height=False)
    form_width = 400
    form_height = 300
    x_coordinate = int((search_form.winfo_screenwidth()/2) - (form_width/2))
    y_coordinate = int((search_form.winfo_screenheight()/2) - (form_height/2))
    search_form.geometry(f'{form_width}x{form_height}+{x_coordinate}+{y_coordinate}')
    search_form.wm_iconphoto(False, theme['main_image'])

    #region Search Bar Theme

    colors = {
        'dark': dark,
        'bg': '#ffffff',
        'div': '#d3d3d3',
        'txt': '#3a3a3a',
        'btn_bg': '#f7f7f7',
        'btn_active_bg': '#c7c7c7'
    }

    if not colors['dark']:
        colors['dark'] = False
        colors['bg'] = '#ffffff'
        colors['div'] = '#d3d3d3'
        colors['txt'] = '#3a3a3a'
        colors['btn_bg'] = '#f7f7f7'
        colors['btn_active_bg'] = '#c7c7c7'

    else:
        colors['dark'] = True
        colors['bg'] = '#000000'
        colors['div'] = '#303030'
        colors['txt'] = '#ffffff'
        colors['btn_bg'] = '#494949'
        colors['btn_active_bg'] = '#1b1b1b'

    def apply_theme():

        search_form.config(bg=colors['bg'])

        style = ttk.Style(master=search_form)
        style.theme_use('default')

        style.configure(
            'Large.TRadiobutton',
            background=colors['div'],
            foreground=colors['txt'],
            fieldbackground=colors['div'],
            rowheight=25,
            bd=0,
            relief=FLAT
        )

        style.configure(
            'TCombobox',
            background = colors['bg'],
            foreground = colors['txt'],
            fieldbackground=colors['bg'],
            rowheight=25,
            bd=0,
            highlightthickness=0,
            relief=FLAT
        )


        for widget in widgets:
            try:
                widget_type = widget.winfo_class()
                if widget_type == 'Frame':
                    widget.config(bg=colors['div'])
                elif widget_type == 'Label':
                    widget.config(bg=colors['div'], fg=colors['txt'])
                elif widget_type == 'Button':
                    widget.config(bg=colors['btn_bg'],
                                activebackground=colors['btn_active_bg'])
                elif widget_type == 'Toplevel':
                    widget.config(bg=colors['bg'])
                elif widget_type == 'Tk':
                    widget.config(bg=colors['bg'])
                elif widget_type == 'Entry':
                    widget.config(bg=colors['bg'], fg = colors['txt'])
            except TclError:
                pass
    # endregion

    # region Search Bar Header
    
    search_header = Frame(master=search_form, height=100)
    search_header.propagate(False)
    search_header.pack(side=TOP, fill=X, padx = pad, pady= pad)
    widgets.append(search_header)

    search_image = PhotoImage(file=r'icons\search.png')
    entry_pic = Label(master=search_header, image=search_image)
    entry_pic.pack(side=LEFT, padx=pad)
    widgets.append(entry_pic)

    search_title = Label(
        master=search_header,
        text='Search Form',
        font=theme['title_font']
    )
    search_title.pack(side=LEFT, padx=pad)
    widgets.append(search_title)

    #endregion

    #region Search Bar Body

    search_body = Frame(master=search_form)
    search_body.pack(side=TOP, fill=BOTH, padx=pad, pady=pad, expand = True)
    widgets.append(search_body)

    stcode_var = StringVar(value='12 Digits')
    ncode_var = StringVar(value='11 Digits')

    #region Top Body

    top_body = Frame(master=search_body)
    top_body.pack(side=TOP,padx=pad, pady=pad, fill=BOTH, expand=True)
    widgets.append(top_body)

    #region Labels

    label_frame = Frame(master=top_body)
    label_frame.pack(side=LEFT, fill=BOTH, expand=True)
    widgets.append(label_frame)

    stcode_label = Label(
        master=label_frame,
        text=' STUDENT CODE ',
        font=theme['btn_font']
    )
    stcode_label.pack(side=TOP)
    widgets.append(stcode_label)

    ncode_label = Label(
        master=label_frame,
        text='NATIONAL CODE',
        font=theme['btn_font']
    )
    ncode_label.pack(side=TOP)
    widgets.append(ncode_label)
    #endregion

    #region Entries

    entry_frame = Frame(master=top_body)
    entry_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    widgets.append(entry_frame)

    stcode_entry = Entry(
        master=entry_frame,
        font=theme['entry_font'],
        highlightthickness= 2,
        highlightbackground= colors['div'],
        highlightcolor='#0059ff',
        insertbackground= colors['txt'],
        bg=colors['bg'],
        fg=colors['txt'],
        textvariable=stcode_var,
        relief = FLAT
    )
    stcode_entry.pack(side=TOP)
    widgets.append(stcode_entry)
    
    ncode_entry = Entry(
        master=entry_frame,
        font=theme['entry_font'],
        highlightthickness= 2,
        highlightbackground= colors['div'],
        highlightcolor='#0059ff',
        insertbackground= colors['txt'],
        bg=colors['bg'],
        fg=colors['txt'],
        textvariable=ncode_var,
        relief = FLAT
    )
    ncode_entry.pack(side=TOP)
    widgets.append(ncode_entry)

    #endregion
    #endregion
    
    #region Bottom Body
    bottom_body = Frame(master=search_body)
    widgets.append(bottom_body)


    #endregion

    #region Seach Bar Footer
    search_footer = Frame(master=search_form)
    search_footer.pack(side=BOTTOM, fill=X, padx = pad, pady= pad)
    widgets.append(search_footer)


    def back():
        search_form.quit()
        search_form.destroy()

    def confirm():
        result = search_code(stcode = stcode_var.get(), ncode= ncode_var.get())
        if not result['SUCCESS']:
            stcode_var.set('')
            ncode_var.set('')
            show_error(messages=result['ERR_MSG'])
        
        else:
            stcode_var.set('')
            ncode_var.set('')
            form_width = 400
            form_height = 640
            x_coordinate = int((search_form.winfo_screenwidth()/2) - (form_width/2))
            y_coordinate = int((search_form.winfo_screenheight()/2) - (form_height/2))
            search_form.geometry(f'{form_width}x{form_height}+{x_coordinate}+{y_coordinate}')
            student = result['RETURN'][0]

            bottom_body.pack(side=TOP,padx=pad, pady=pad, fill=BOTH, expand=True)
            
            data = {
                'Name': student['name'],
                'Family': student['family'],
                'Age': age(student['birth']),
                'Gender': student['gender'],
                'Student Code': student['stcode'],
                'National Code': student['ncode']
            }
            

            # region Label Frames
            bottom_left = Frame(master=bottom_body)
            bottom_left.pack(side=LEFT,padx=pad, pady=pad, fill=BOTH, expand=True)
            widgets.append(bottom_left)

            bottom_right = Frame(master=bottom_body)
            bottom_right.pack(side=RIGHT,padx=pad, pady=pad, fill=BOTH, expand=True)
            widgets.append(bottom_right)
            #endregion

            for key, value in data.items():
                key_label = Label(
                    master= bottom_left,
                    text= key,
                    font= theme['btn_font']
                )
                widgets.append(key_label)
                apply_theme()
                key_label.pack(side=TOP, pady = pad, padx=pad, anchor=W)

                value_label = Label(
                    master= bottom_right,
                    width= 100,
                    text= value,
                    font= theme['btn_font'],
                    highlightthickness= 3,
                    highlightbackground='#0059ff'
                )
                widgets.append(value_label)
                apply_theme()
                value_label.pack(side=TOP, pady = pad - 3, padx=pad, anchor=W)
        

    btn_width = 120

    btn_back = Button(
        text='BACK',
        image=theme['back_btn_image'],
        font=theme['btn_font'],
        master=search_footer,
        command=back, 
        bg='#ff002b',
        activebackground='#dd0327',
        foreground='#ffffff',
        compound=LEFT,
        relief=FLAT,
        width=btn_width
    )

    btn_back.pack(side=LEFT, padx=pad, pady=pad)  # Added `padx` and `pady` for spacing
    
    btn_cofirm = Button(
        text='CONFIRM',
        image=theme['confirm_btn_image'],
        font=theme['btn_font'],
        master=search_footer,
        command=confirm, 
        bg='#0066ff',
        activebackground='#0058dd',
        foreground='#ffffff',
        compound=LEFT,
        relief=FLAT,
        width=btn_width
    )

    btn_cofirm.pack(side=RIGHT, padx=pad, pady= pad)

    #endregion

    apply_theme()
    search_form.mainloop()

# endregion

# endregion

#endregion

# region Main Form Initializaton

def main_form():

    # region Initialize
    form = Tk()
    form.title('Student Managemer')
    form.overrideredirect()

    # style = ttk.Style(master=form)
    # style.theme_use(themename='default')  # classic alt default clam
    # style.configure('TreeView', background='#000000',
    #                 fieldbackground='#000000')

    # Size And Coordinate
    form_width = 800
    form_height = 515
    form.resizable(width=False, height=False)
    x_coordinate = int((form.winfo_screenwidth()/2) - (form_width/2))
    y_coordinate = int((form.winfo_screenheight()/2) - (form_height/2))
    form.geometry(f'{form_width}x{form_height}+{x_coordinate}+{y_coordinate}')
    main_image = PhotoImage(name='main', file=r'icons\SMP.png')
    form.wm_iconphoto(False, main_image)
    widgets.append(form)

    #endregion

    #region Theme Switch Button

    colors = {
        'dark': False,
        'bg': '#ffffff',
        'div': '#d3d3d3',
        'txt': '#3a3a3a',
        'btn_bg': '#f7f7f7',
        'btn_active_bg': '#c7c7c7'
    }

    theme = {
        'exit_btn_image' : PhotoImage(file=r'icons\btn_exit.png'),
        'remove_btn_image' : PhotoImage(file=r'icons\btn_remove.png'),
        'edit_btn_image' : PhotoImage(file=r'icons\btn_edit.png'),
        'add_btn_image' : PhotoImage(file=r'icons\btn_add.png'),
        'search_btn_image' : PhotoImage(file=r'icons\btn_search.png'),
        'back_btn_image' : PhotoImage(file=r'icons\btn_back.png'),
        'confirm_btn_image' : PhotoImage(file=r'icons\btn_confirm.png'),
        'main_image' : PhotoImage(name='main', file=r'icons\SMP.png'),
        'title_font' : font.Font(family='EB Garamond', size=30, weight='bold'),
        'entry_font' : ("tahoma", 11, "normal"),
        'btn_font' : font.Font(family='Cambria', size='15', weight='bold')
    }

    switch_light = PhotoImage(file=r'icons\btn_sun.png')
    switch_dark = PhotoImage(file=r'icons\btn_moon.png')

    burger_light = PhotoImage(file=r'icons\btn_burger_light.png')
    burger_dark = PhotoImage(file=r'icons\btn_burger_dark.png')


    def toggle():

        # global switch_image, burger_image

        if colors['dark']:
            colors['dark'] = False
            colors['bg'] = '#ffffff'
            colors['div'] = '#d3d3d3'
            colors['txt'] = '#3a3a3a'
            colors['btn_bg'] = '#f7f7f7'
            colors['btn_active_bg'] = '#c7c7c7'
            switch_image = switch_light
            burger_image = burger_light

        else:
            colors['dark'] = True
            colors['bg'] = '#000000'
            colors['div'] = '#303030'
            colors['txt'] = '#ffffff'
            colors['btn_bg'] = '#494949'
            colors['btn_active_bg'] = '#1b1b1b'
            switch_image = switch_dark
            burger_image = burger_dark

        apply_theme(switch_image=switch_image, burger_image=burger_image)

    # endregion

    # region Burger Functionality

    # Function to create a backup of the current database
    def create_backup_ui():
        """
        Creates a backup of the current data through a user interface.
        This function opens a file dialog to allow the user to specify the location
        and name of the backup file. The backup file will be saved with a .txt extension.
        If the user provides a valid file path, the function will attempt to create a backup
        using the `create_backup` function. Upon successful backup creation, a success message
        is displayed to the user. If the backup creation fails, an error message is shown.
        Returns:
            None
        Raises:
            None
        """        

        backup_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if backup_path:
            result = create_backup(backup_path = backup_path)
            if result['SUCCESS']:
                show_success("Backup created successfully.")
            else:
                show_error({"ERROR": result['ERR_MSG']})

    # Function to clear the current database (clear data)
    def drop_database_ui():
        """
        Clears the database and updates the UI accordingly.
        This function calls the `clear_database` function to clear the database.
        If the operation is successful, it displays a success message and reloads
        the data in the TreeView. If the operation fails, it displays an error message
        with the error details.
        Returns:
            None
        Raises:
            None
        """

        result = clear_database()
        if result['SUCCESS']:
            show_success("Database cleared successfully.")
            reload_data()  # Refresh the TreeView
        else:
            show_error({"ERROR": result['ERR_MSG']})

    # Function to reload data from the source file
    def reload_data():
        """
        Reloads the data in the table widget.
        This function clears all existing entries in the table widget and 
        repopulates it with fresh data retrieved from the `get_data` function. 
        The data is expected to be a dictionary with a key 'RETURN' that holds 
        a list of student records. Each student record is a dictionary, and 
        the values of these dictionaries are inserted into the table.
        Steps:
        1. Delete all current entries in the table.
        2. Retrieve new data using the `get_data` function.
        3. Insert each student's data into the table.
        Note:
        - The `table` widget and `get_data` function must be defined in the 
          scope where this function is used.
        - The `table` widget should support `delete` and `insert` methods, 
          and `get_children` method to retrieve current entries.
        Raises:
        - KeyError: If the 'RETURN' key is not found in the data returned by `get_data`.
        Example:
            reload_data()
        """

        table.delete(*table.get_children())
        data = get_data()['RETURN']
        for student in data:
            table.insert('', END, values=list(student.values()))

        

    #endregion

    # region Apply Theme


    def apply_theme(switch_image = 0, burger_image = 0):

        # global switch_image, burger_image

        form.config(bg=colors['bg'])
        
        if switch_image:
            switch.config(image=switch_image)
            burger.config(image=burger_image)
        
        style = ttk.Style(master=form)
        style.theme_use('default')
        style.configure('Treeview',
                        background=colors['div'],
                        foreground=colors['txt'],
                        fieldbackground=colors['div'],
                        rowheight=25,
                        bd=0,
                        highlightthickness=0,
                        relief=FLAT

                        )
        style.configure('Treeview.Heading',
                        background=colors['btn_bg'],
                        foreground=colors['txt'],
                        rowheight=25,
                        bd=0,
                        highlightthickness=0,
                        relief=FLAT

                        )
        
        for widget in widgets:
            try:
                widget_type = widget.winfo_class()
                if widget_type == 'Frame':
                    widget.config(bg=colors['div'])
                elif widget_type == 'Label':
                    widget.config(bg=colors['div'], fg=colors['txt'])
                elif widget_type == 'Button' or 'Menubutton':
                    widget.config(bg=colors['btn_bg'],
                                activebackground=colors['btn_active_bg'])
                elif widget_type == 'Toplevel':
                    widget.config(bg=colors['bg'])
                elif widget_type == 'Tk':
                    widget.config(bg=colors['bg'])
            except TclError:
                pass

    # endregion

    # region Frames Initialization


    header = Frame(master=form, highlightthickness=0, relief=FLAT)
    header.pack(side=TOP, fill=X, padx=pad, pady=pad)
    header.update()
    widgets.append(header)

    button_bar = Frame(master=header, highlightthickness=0, relief=FLAT)
    button_bar.pack(side=RIGHT, fill=X, padx=pad, pady=pad)
    button_bar.update()
    widgets.append(button_bar)
    # widgets.append(button_bar)

    body = Frame(master=form, highlightthickness=0, relief=FLAT)
    body.pack(side=TOP, fill=X, padx=pad, pady=pad)
    body.update()
    widgets.append(body)

    footer = Frame(master=form, highlightthickness=0, relief=FLAT)
    footer.pack(side=BOTTOM, fill=X, padx=pad, pady=pad)
    footer.update()
    widgets.append(footer)


    # endregion

    # region Header

    # main_image = PhotoImage(name='main', file=r'icons\main_light.png')

    title = Label(
        master=header,
        text='Student Manager',
        font=theme['title_font'],
        compound=LEFT
    )
    title.pack(anchor=W, padx=pad, pady=pad, side=LEFT)
    widgets.append(title)

    # region Header Button Bar

    # Theme Button

    switch = Button(
        master=button_bar,
        command=toggle,
        relief=FLAT,
    )
    widgets.append(switch)
    switch.pack(padx=0, pady=3, side=TOP)

    # Hamburger Button

    burger = Menubutton(
        master=button_bar,
        text='Menu',
        relief=FLAT
    )
    burger.menu = Menu(master= burger, tearoff=0)
    burger['menu'] = burger.menu
    burger.menu.add_command(label='Create Back Up', command=create_backup_ui)
    burger.menu.add_command(label='Drop Current Table', command=drop_database_ui)



    widgets.append(burger)
    burger.pack(padx=0, pady=5, side=BOTTOM)

    switch.config(image=switch_light)
    burger.config(image=burger_light)

    # endregion

    #endregion

    # region Body

    # Create Scrollbar
    scroll = Scrollbar(master=body, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y, padx=pad, pady=pad)

    # Create Treeview
    columns = ('name', 'family', 'gender', 'birth', 'ncode', 'stcode')
    table = Treeview(
        master=body,
        columns=columns,
        show='headings',selectmode='extended',
        yscrollcommand=scroll.set
    )

    # Configure Scrollbar
    scroll.config(command=table.yview)

    # Pack Treeview
    table.pack(side=LEFT, fill=BOTH, expand=True, padx=pad, pady=pad)

    column_widths = {
        'name': 100,
        'family': 100,
        'birth': 120,
        'gender': 50,
        'ncode': 100,
        'stcode': 100
    }
    for column in columns:
        table.heading(column=column, text=column)
        table.column(column, width=column_widths[column], anchor=CENTER)

    # Insert data into Treeview
    data = get_data()['RETURN']
    for student in data:
        table.insert('', END, values=list(student.values()))
    # column_width = table.winfo_width()


    # endregion
    
    # region Footer

    btn_height = 30
    btn_width = 110

    # region Button Functions
    def _add():
        form.withdraw()
        _entry_form(table= table, dark= colors['dark'], theme=theme)
        form.deiconify()

    def _edit():

        if not table.selection():
            show_error({'SELECTION': 'Please select an item to edit'})
            return None
        
        form.withdraw()
        _entry_form(table=table, dark=colors['dark'], theme=theme, mode= 'edit', selected=table.selection())
        form.deiconify()
        
    def _search():
        form.withdraw()
        _search_form(dark= colors['dark'], theme=theme)
        form.deiconify()

    def _delete():
        selected_item = table.selection()
        if not selected_item:
            show_error({'SELECTION': 'Please select an item to delete'})
            return None
        
        
        student = Student(table.item(selected_item[0])['values'])
        result = delete_std(student=student)
        if not result['SUCCESS']:
            show_error(result['ERR_MSG'])
        else:
            #Show a yes-no question here
            table.delete(selected_item)

    def _exit_program():
        form.quit()
        form.destroy()

    
    #endregion

    buttons = {
        'EXIT': {'background': '#222222',
                'active_background': '#000000',
                'image': theme['exit_btn_image'],
                'command': _exit_program
                },

        'DELETE': {'background': '#ff0000',
                'active_background': '#df3a3a',
                'image': theme['remove_btn_image'],
                'command': _delete
                },

        'EDIT': {'background': '#ffbf00',
                'active_background': '#f1b910',
                'image': theme['edit_btn_image'],
                'command': _edit
                },

        'ADD': {'background': '#0066ff',
                'active_background': '#2d81ff',
                'image': theme['add_btn_image'],
                'command': _add
                },

        'SEARCH': {'background': '#5d00ff',
                'active_background': '#4500bd',
                'image': theme['search_btn_image'],
                'command': _search
                }
    }

    lpadx = (footer.winfo_width() - len(buttons)
                    * btn_width) / (len(buttons) + 2)
    
    for key, value in buttons.items():
        Button(master=footer,
            command=value['command'],
            relief=FLAT,
            font=theme['btn_font'],
            text=f'{key}',
            image=value['image'],
            compound=LEFT,
            height=btn_height,
            width=btn_width,
            background=value['background'],
            activebackground=value['active_background'],
            foreground='#ffffff',
            activeforeground='#ffffff'
            ).pack(side='left', padx=(lpadx,0), pady=pad)


    # endregion

# endregion

    apply_theme()
    form.mainloop()