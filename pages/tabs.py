import flet as ft
import state, csv, math, os, logging, logging.config
from utils.statusButton import statusButton
from utils import banner
from sendtls import sendmail

def tab1(page: ft.Page, nextTab):

    # Table data (list of dictionaries to store email and validity status)
    table_data = []

    # Function to populate the table from file data
    def load_table_from_file(file_path):
        nonlocal table_data
        table_data.clear()
        try:
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        email = row[0]
                        table_data.append({"email": email, "valid": "Not Checked"})
            refresh_table()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error loading file: {e}"))
            page.snack_bar.open = True

    # Function to handle file pick event
    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            load_table_from_file(file_path)
            selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Select File"
        )
        page.update()

    # Removes data from the file present in the table
    def removeFile(e):
        table_data.clear()
        selected_files.value = 'Select File'
        refresh_table()
        

    # Function to update the validity column after validation
    def validate_emails(e):
        for row in table_data:
            # Replace this with a real email validation logic
            row["valid"] = "valid" if "@" in row["email"] else "invalid"

        
        refresh_table()

    # Function to open the email editor for a specific row
    def edit_email(e, row_index):
        current_email = table_data[row_index]["email"]
        email_field.value = current_email
        save_button.data = row_index  # Store the row index in the button data
        edit_dialog.open = True
        page.update()

    # Function to save the edited email
    def save_email(e):
        row_index = save_button.data
        table_data[row_index]["email"] = email_field.value
        table_data[row_index]["valid"] = 'Not checked'
        edit_dialog.open = False
        refresh_table()

    # Function to check if all emails in the DataTable are valid.
    # To be checked before going to next.
    def checkStatus(e):
        allValid = 1
        noOfEmails = 0
        for index, row in enumerate(table_data):
            noOfEmails += 1
            if row['valid'] != 'valid':
                allValid = 0
                break
        
        if allValid == 1 and noOfEmails != 0:
            nextTab(lambda e:e)
        elif noOfEmails == 0:
            page.open(banner.errorBanner('You have not selected any recipients', page))
        else:
            page.open(banner.errorBanner('Check all emails and validate them before proceeding', page))

    # Function to refresh the table
    def refresh_table():
        table.rows.clear()
        state.recipientList = []
        for index, row in enumerate(table_data):
            if row['valid'] == 'valid':
                status = ft.TextButton(content=statusButton(ft.icons.CHECK_CIRCLE, 'green', 'VALID', 'white', 'transparent'))
            elif row['valid'] == 'invalid':
                status = ft.TextButton(content=statusButton(ft.icons.CANCEL, 'red', 'INVALID', 'white', 'transparent'))
            else:
                status = ft.TextButton(content=statusButton(ft.icons.WARNING, 'amber', 'VALIDATE', 'white', 'transparent'))
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["email"])),
                        
                        ft.DataCell(status),
                        ft.DataCell(
                            ft.ElevatedButton(
                                "Edit",icon=ft.icons.EDIT, icon_color='white', color='white',
                                on_click=lambda e, i=index: edit_email(e, i),
                            )
                        ),
                    ]
                )
            )
            state.recipientList.append(row['email'])
        page.update()


    # Dialog for editing email
    email_field = ft.TextField(label="Edit Email")
    save_button = ft.ElevatedButton("Save", on_click=save_email)
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit Email"),
        content=email_field,
        actions=[
            save_button,
            ft.TextButton("Cancel", on_click=lambda e: setattr(edit_dialog, "open", False)),
        ],
    )

    # File picker to upload a CSV file
    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    selected_files = ft.Text('Select File')
    fileTitle = ft.Row(controls=[
        ft.Icon(ft.icons.FOLDER, color='white'), selected_files, ft.IconButton(ft.icons.CLOSE, icon_color='red', on_click=removeFile)
    ], alignment=ft.MainAxisAlignment.CENTER, width=250)

    # Button to open file picker
    upload_button = ft.OutlinedButton("Upload CSV File",
    on_click=lambda e: file_picker.pick_files(allow_multiple=False, allowed_extensions=['csv']),
    icon=ft.icons.FILE_UPLOAD, icon_color='white', width=250,)

    # DataTable definition
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Valid or Not")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],
        
        border_radius=15,
        width=650,
        
        horizontal_lines=ft.BorderSide(1, "#a8a8a8"),
        vertical_lines=ft.BorderSide(2, "#a8a8a8"),
        border=ft.border.all('1', 'white'),
    )

    # Button to validate emails
    validate_button = ft.OutlinedButton("Validate Emails",
    on_click=validate_emails, icon=ft.icons.TASK, icon_color='white', width=250)
    page.add(edit_dialog)
    # Add components to the page
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[fileTitle, upload_button,
                    ft.Row(height=150),
                    validate_button,],

                    width=300, alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                ft.Column(
                    controls=[table],
                    scroll='auto',
                    height=550
                ),
                
                ft.Row([ft.ElevatedButton('Next', on_click=checkStatus,
                icon=ft.icons.NAVIGATE_NEXT,icon_color='white')],
                vertical_alignment="end", alignment="end", height=600, width=250)
            ],
            alignment="center",
            vertical_alignment="center"
        ),
        
        border_radius=15,
        border=ft.border.all('1', 'white'),
        margin=ft.Margin(10,20,10,10),
        padding=ft.Padding(0,0,0,15),
        alignment=ft.alignment.center,
    )

def tab2(page: ft.Page, nextTab):

    # Attachment file system logic:
    # 1. Select file
    # 2. Find path and size of files selected.
    # 3. Add file paths to list of state uiData -> attachmentData.
    # 4. Add files with respective icons into datatable.
    # 5. Calculate total size and proceed if size < 25MB else WARN

    # On event of removing a file already selected,
    # 1. Remove file from state uiData -> attachmentData
    # 2. Remove file from datatable.
    # 3. Refresh total size calculation of all attachments.

    totalsizeBytes = 0

    def getTotalSize():
        global totalsizeBytes
        totalsizeBytes = 0
        size = 0
        for path in state.attachmentData:
            size += os.path.getsize(path)
            totalsizeBytes += os.path.getsize(path)
        totalsize.value = f'Total size: {convert_size(size)}'

    def addFileToList(path):
        # Code to add file to email content
        state.attachmentData.append(path)
        refreshTable()

    def deleteAttachment(e, index):
        
        # To delete file from attachments list.
        state.attachmentData.remove(state.attachmentData[index])
        refreshTable()

    def refreshTable():
        attachments.controls.clear()
        
        for index, file in enumerate(state.attachmentData):
            fileName = file.split('\\')[-1]
            extension = fileName.split('.')[-1]
            # table.rows.clear()
            attachments.controls.append(
                ft.ListTile(
                    title=ft.Text(fileName), leading=ft.Image(src=f'icons/{extension}.png', error_content=ft.Image(src=f'icons/file.png', color='white')),
                    subtitle=ft.Text(f'Size: {fileSize(file)}'),width=500, height=70,
                    trailing=ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=index: deleteAttachment(e, i)), data=index),
            )
            
            # table.rows.append(
            # ft.DataRow(cells=[ft.DataCell(
            #     ft.ListTile(bgcolor='#D9571C',
            #     title=ft.Text(fileName), leading=ft.Image(src=f'icons/{extension}.png'),
            #     subtitle=ft.Text(f'Size: {fileSize(file)}'),width=500, height=70),
            # )],)
        getTotalSize()
        page.update()

    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            for each in range(len(e.files)):
                file_path = e.files[each].path
                addFileToList(file_path)
            
        page.update()

    # Function to find size of file
    def fileSize(path):
        size = os.path.getsize(path)
        return convert_size(size)

    # Function to format file to largest file size possible
    # Eg: 10240 bytes returns 10 KB
    def convert_size(byteSize):
        if byteSize == 0 :
            return '0 B'
        sizeName = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        i = int(math.floor(math.log(byteSize, 1024)))
        p = math.pow(1024, i)
        s = round(byteSize / p, 2)
        return f'{s} {sizeName[i]}'

    # Check if any if content is missing
    def checkStatus(e, page):
        if totalsizeBytes > 26214400:
            page.open(banner.warningBanner('Attachment size should not exceed 25 MB', page))
        elif mailContent.value.strip() == '':
            page.open(banner.errorBanner('Email content should not be empty.', page))
        else:
            state.maildata.append(subject.value)
            state.maildata.append(mailContent.value)
            nextTab(e)


    mailContent = ft.TextField(label='Content', multiline=True,
    hint_text='Content of email goes here', height=500,min_lines=20, width=700
    , border_color='white', border_width=1, label_style=ft.TextStyle(color='#8a8a8a'))
    
    subject = ft.TextField(label='Subject', width=500, border_color='white',
    label_style=ft.TextStyle(color='#8a8a8a'), border_width=1)

    attachmentPicker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(attachmentPicker)
     
    attachments = ft.ListView(controls=[], auto_scroll=True, height=375, width=500, expand=1)
    attachmentHeader = ft.Row(controls=[
        ft.Text('Attachments', text_align=ft.TextAlign.LEFT, color='#8a8a8a', size=15), 
        ft.IconButton(icon=ft.icons.ADD, icon_color='#8a8a8a', tooltip='Add attachments',
        alignment=ft.Alignment(x=1, y=0.5), on_click=lambda e:attachmentPicker.pick_files(allow_multiple=True))
    ])

    totalsize = ft.Text(f'Total size: 0 B', color='#8a8a8a', size=15)
    totalRow = ft.Row(controls=[
        totalsize
    ])

    
    return ft.Container(
                    content=ft.Row(
                        controls=[
                        mailContent, 
                        
                        ft.Column(
                            [subject, 
                            attachmentHeader, attachments, totalsize
                        ], height=500, width=500
                        ),

                        ft.Row([ft.ElevatedButton('Next',on_click=lambda e:checkStatus(e, page),
                        icon=ft.icons.NAVIGATE_NEXT,icon_color='white')],
                        vertical_alignment="end", alignment="end", height=500)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                    ),
                    
                    alignment=ft.alignment.center,
                    border_radius=15,
                    border=ft.border.all('1', 'white'),
                    margin=ft.Margin(10,20,10,10),
                    
                )

def tab3(page: ft.Page):
    def sendTLS(e):
        logging.basicConfig(filename="log/logFile.log",
                    format='%(asctime)s %(levelname)s  %(message)s',
                    datefmt="[%d-%m-%Y] [%H:%M:%S]",
                    filemode='a')
        # create logger
        logger = logging.getLogger('MassMAIL')
        logger.setLevel(logging.DEBUG)

        for i in sendmail(state.recipientList,
            state.maildata[0],state.maildata[1],
            state.attachmentData):

            logg.value += f'{i}\n'
            logger.info(f'{i}')
            
            page.update()

    logg = ft.TextField(multiline=True, width=500, min_lines=17, border_color='white',
                        hint_text='LOG autosaved to folder', height=450,
                        border_radius=ft.BorderRadius(0,0,30,30), border_width='1')

    
    return ft.Container(
                    ft.Row(
                    controls=[ft.Container(
                        content=ft.Stack(
                            [
                        ft.Container(ft.Icon(ft.icons.MAIL_LOCK, color='white', size=70),
                        alignment=ft.Alignment(0, -0.25)),
                        ft.TextButton(text='Send emails securely with TLS',width=350, height=500, 
                        style=ft.ButtonStyle(color='white', shape=ft.RoundedRectangleBorder(0)), on_click=sendTLS)],
                        width=350, height=500,
                    ),

                    width=350, height=500,
                    alignment=ft.alignment.center,
                    border_radius=15,
                    border=ft.border.all('1', 'white'),
                    
                    ),
                    ft.Column([ft.Container(
                        ft.Row([ft.Text('LOG', color='white', text_align=ft.TextAlign.CENTER,width=500)]),
                        bgcolor='#636363', height=50,margin=ft.Margin(0,0,0,0),
                        border_radius=ft.BorderRadius(30,30,0,0)),
                    logg],height=500,)

                    ], alignment=ft.alignment.center, width=800),
                    alignment=ft.alignment.center,
                    border_radius=15,
                    border=ft.border.all('1', 'white'),
                    margin=ft.Margin(10,20,10,10),
                    
    )
