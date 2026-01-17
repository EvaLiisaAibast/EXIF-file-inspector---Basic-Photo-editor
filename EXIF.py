from PIL import Image, ExifTags, ImageTk, ImageEnhance, ImageFilter, ImageDraw
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser, simpledialog
import datetime
import shutil

import os
import sys
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller/Auto PY to EXE."""
    try:

        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


LOG_FILE = resource_path("scan_log.txt")


def view_log():
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Info", "No log yet.")
        return
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()
    messagebox.showinfo("Log", log_contents)


languages = {
    "English": {
        "select_folder": "Select Source Folder",
        "run_scan": "Run Scan",
        "view_log": "View Log",
        "scan_complete": "Scan complete!",
        "flagged_images": "images flagged.",
        "error_no_source": "Please select a folder or drop files first!",
        "folder": "Source: ",
        "none": "Not selected",
        "search_exif": "Search EXIF or Filename:",
        "search_button": "Search",
        "real_images": "Real images: {real_images}",
        "ai_images": "AI images: {ai_images}",
        "edit_tools": "Photo Editing Tools",
        "open_image": "Open Image",
        "save_image": "Save Image",
        "rotate_left": "Rotate Left",
        "rotate_right": "Rotate Right",
        "flip_h": "Flip Horizontal",
        "flip_v": "Flip Vertical",
        "grayscale": "Grayscale",
        "brightness": "Brightness",
        "contrast": "Contrast",
        "blur": "Blur",
        "sharpen": "Sharpen",
        "sepia": "Sepia",
        "draw": "Draw/Edit Overlay",
        "undo": "Undo",
        "reset": "Reset",
        "language": "Language"
    },
    "Estonian": {
        "select_folder": "Vali lähtekaust",
        "run_scan": "Alusta skaneerimist",
        "view_log": "Vaata logi",
        "scan_complete": "Skaneerimine lõpetatud!",
        "flagged_images": "pilti märgistatud.",
        "error_no_source": "Palun vali kaust või lohista failid!",
        "folder": "Lähtekaust: ",
        "none": "Pole valitud",
        "search_exif": "Otsi EXIF-i või faili nime:",
        "search_button": "Otsi",
        "real_images": "Tegelikud pildid: {real_images}",
        "ai_images": "AI pildid: {ai_images}",
        "edit_tools": "Fototöötluse tööriistad",
        "open_image": "Ava pilt",
        "save_image": "Salvesta pilt",
        "rotate_left": "Pööra vasakule",
        "rotate_right": "Pööra paremale",
        "flip_h": "Peegelda horisontaalselt",
        "flip_v": "Peegelda vertikaalselt",
        "grayscale": "Halltoonides",
        "brightness": "Heledus",
        "contrast": "Kontrast",
        "blur": "Hägusta",
        "sharpen": "Teravda",
        "sepia": "Sepia",
        "draw": "Joonista / kleebised",
        "undo": "Võta tagasi",
        "reset": "Lähtesta",
        "language": "Keel"
    },
    "German": {
        "select_folder": "Quellordner auswählen",
        "run_scan": "Scan starten",
        "view_log": "Protokoll anzeigen",
        "scan_complete": "Scan abgeschlossen!",
        "flagged_images": "Bilder markiert.",
        "error_no_source": "Bitte wählen Sie zuerst einen Ordner aus!",
        "folder": "Quelle: ",
        "none": "Nicht ausgewählt",
        "search_exif": "EXIF oder Dateiname suchen:",
        "search_button": "Suchen",
        "real_images": "Echte Bilder: {real_images}",
        "ai_images": "KI Bilder: {ai_images}",
        "edit_tools": "Bildbearbeitung",
        "open_image": "Bild öffnen",
        "save_image": "Bild speichern",
        "rotate_left": "Nach links drehen",
        "rotate_right": "Nach rechts drehen",
        "flip_h": "Horizontal spiegeln",
        "flip_v": "Vertikal spiegeln",
        "grayscale": "Graustufen",
        "brightness": "Helligkeit",
        "contrast": "Kontrast",
        "blur": "Weichzeichnen",
        "sharpen": "Schärfen",
        "sepia": "Sepia",
        "draw": "Zeichenmodus / Sticker",
        "undo": "Rückgängig",
        "reset": "Zurücksetzen",
        "language": "Sprache"
    },
    "Russian": {
        "select_folder": "Выберите папку-источник",
        "run_scan": "Запустить сканирование",
        "view_log": "Просмотр журнала",
        "scan_complete": "Сканирование завершено!",
        "flagged_images": "изображений помечено.",
        "error_no_source": "Пожалуйста, выберите папку!",
        "folder": "Папка: ",
        "none": "Не выбрано",
        "search_exif": "Искать EXIF или имя файла:",
        "search_button": "Поиск",
        "real_images": "Настоящие изображения: {real_images}",
        "ai_images": "AI изображения: {ai_images}",
        "edit_tools": "Редактирование фото",
        "open_image": "Открыть",
        "save_image": "Сохранить",
        "rotate_left": "Повернуть влево",
        "rotate_right": "Повернуть вправо",
        "flip_h": "Отразить по горизонтали",
        "flip_v": "Отразить по вертикали",
        "grayscale": "Черно-белый",
        "brightness": "Яркость",
        "contrast": "Контраст",
        "blur": "Размытие",
        "sharpen": "Резкость",
        "sepia": "Сепия",
        "draw": "Рисование / Наклейки",
        "undo": "Отменить",
        "reset": "Сброс",
        "language": "Язык"
    }
}

current_lang = "English"
SOURCE_FOLDER = ""
FLAGGED_FOLDER = "flagged_images"
LOG_FILE = "scan_log.txt"
os.makedirs(FLAGGED_FOLDER, exist_ok=True)

def run_scan():
    if not SOURCE_FOLDER:
        messagebox.showerror("Error", languages[current_lang]["error_no_source"])
        return
    imgs = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith((".jpg",".jpeg",".png"))]
    if not imgs:
        messagebox.showinfo("Info","No images found.")
        log("No images found in folder: " + SOURCE_FOLDER, "WARN")
        return
    real, ai = 0, 0
    real_dir = os.path.join(SOURCE_FOLDER, "Real Images")
    ai_dir = os.path.join(SOURCE_FOLDER, "AI Images")
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(ai_dir, exist_ok=True)
    progress['value']=0
    progress['maximum']=len(imgs)
    
    log(f"Starting scan in folder: {SOURCE_FOLDER}")
    
    for i,f in enumerate(imgs, start=1):
        p=os.path.join(SOURCE_FOLDER,f)
        exif,_=read_exif(p)
        if exif:
            shutil.copy(p, os.path.join(real_dir,f))
            real+=1
            log(f"Real image: {f}")
        else:
            shutil.copy(p, os.path.join(ai_dir,f))
            ai+=1
            log(f"AI image: {f}")
      
        if i==1:
            img_preview=Image.open(p)
            img_preview.thumbnail((400,400))
            tk_img=ImageTk.PhotoImage(img_preview)
            image_label.config(image=tk_img)
            image_label.image=tk_img
        progress['value']=i
        root.update_idletasks()
    count_label.config(text=f"AI: {ai} | Real: {real}")
    messagebox.showinfo("Done",f"{languages[current_lang]['scan_complete']}\nAI: {ai}, Real: {real}")
    log(f"Scan complete. Real: {real}, AI: {ai}")


def read_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return {}, False
        return {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}, True
    except Exception:
        return {}, False

root = tk.Tk()
root.title("Image Analyzer + Photo Editor")
root.geometry("1200x850")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="Image Analyzer")
notebook.add(tab2, text="Photo Editor")

frame_left = tk.Frame(tab1)
frame_left.pack(side="left", padx=20, pady=20, anchor="nw")
frame_right = tk.Frame(tab1)
frame_right.pack(side="right", padx=20, pady=20, anchor="ne")

folder_label = tk.Label(frame_left, text=f"{languages[current_lang]['folder']} {languages[current_lang]['none']}")
folder_label.grid(row=0, column=0, pady=5)

search_label = tk.Label(frame_left, text=languages[current_lang]['search_exif'])
search_label.grid(row=1, column=0, pady=5)
search_entry = tk.Entry(frame_left, width=30)
search_entry.grid(row=2, column=0, pady=5)
search_btn = tk.Button(frame_left, text=languages[current_lang]["search_button"])
search_btn.grid(row=3, column=0, pady=5)

btn_select = tk.Button(frame_left, text=languages[current_lang]["select_folder"])
btn_select.grid(row=4, column=0, pady=5)
btn_scan = tk.Button(frame_left, text=languages[current_lang]["run_scan"])
btn_scan.grid(row=5, column=0, pady=5)
btn_log = tk.Button(frame_left, text=languages[current_lang]["view_log"])
btn_log.grid(row=6, column=0, pady=5)

count_label = tk.Label(frame_left, text="")
count_label.grid(row=7, column=0, pady=10)


progress = ttk.Progressbar(frame_right, length=300, mode='determinate')
progress.pack(pady=5)
image_label = tk.Label(frame_right)
image_label.pack(pady=10)

def select_folder():
    global SOURCE_FOLDER
    SOURCE_FOLDER = filedialog.askdirectory()
    if SOURCE_FOLDER:
        folder_label.config(text=f"{languages[current_lang]['folder']} {SOURCE_FOLDER}")

def view_log():
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Info", "No log yet.")
        return
    win = tk.Toplevel(root)
    win.title("Log Viewer")
    text = tk.Text(win)
    text.pack(fill="both", expand=True)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        text.insert("1.0", f.read())
    text.config(state="disabled")

def run_scan():
    if not SOURCE_FOLDER:
        messagebox.showerror("Error", languages[current_lang]["error_no_source"])
        return
    imgs = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith((".jpg",".jpeg",".png"))]
    if not imgs:
        messagebox.showinfo("Info","No images found.")
        return
    real, ai = 0, 0
    real_dir = os.path.join(SOURCE_FOLDER, "Real Images")
    ai_dir = os.path.join(SOURCE_FOLDER, "AI Images")
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(ai_dir, exist_ok=True)
    progress['value']=0
    progress['maximum']=len(imgs)
    for i,f in enumerate(imgs, start=1):
        p=os.path.join(SOURCE_FOLDER,f)
        exif,_=read_exif(p)
        if exif:
            shutil.copy(p, os.path.join(real_dir,f)); real+=1
        else:
            shutil.copy(p, os.path.join(ai_dir,f)); ai+=1
        if i==1:
            img_preview=Image.open(p)
            img_preview.thumbnail((400,400))
            tk_img=ImageTk.PhotoImage(img_preview)
            image_label.config(image=tk_img)
            image_label.image=tk_img
        progress['value']=i
        root.update_idletasks()
    count_label.config(text=f"AI: {ai} | Real: {real}")
    messagebox.showinfo("Done",f"{languages[current_lang]['scan_complete']}\nAI: {ai}, Real: {real}")

def search_exif():
    term = search_entry.get().lower()
    if not SOURCE_FOLDER:
        messagebox.showerror("Error", languages[current_lang]["error_no_source"])
        return
    result_images=[]
    for f in os.listdir(SOURCE_FOLDER):
        if f.lower().endswith((".jpg",".jpeg",".png")):
            p=os.path.join(SOURCE_FOLDER,f)
            exif,_=read_exif(p)
            if term in f.lower() or any(term in str(v).lower() for v in exif.values()):
                result_images.append(f)
    if result_images:
        messagebox.showinfo("Search Results", f"Found {len(result_images)} image(s):\n"+"\n".join(result_images))
    else:
        messagebox.showinfo("Search Results", "No images matched.")

btn_select.config(command=select_folder)
btn_scan.config(command=run_scan)
btn_log.config(command=view_log)
search_btn.config(command=search_exif)

def set_language(lang):
    global current_lang
    current_lang = lang
    # Tab1
    folder_label.config(text=f"{languages[current_lang]['folder']} {SOURCE_FOLDER or languages[current_lang]['none']}")
    search_label.config(text=languages[current_lang]['search_exif'])
    search_btn.config(text=languages[current_lang]["search_button"])
    btn_select.config(text=languages[current_lang]["select_folder"])
    btn_scan.config(text=languages[current_lang]["run_scan"])
    btn_log.config(text=languages[current_lang]["view_log"])
    # Tab2
    toolbar_btns = [
        ("open_image", open_image_tab2),
        ("save_image", save_image_tab2),
        ("rotate_left", rotate_left),
        ("rotate_right", rotate_right),
        ("flip_h", flip_h),
        ("flip_v", flip_v),
        ("grayscale", grayscale),
        ("sepia", sepia),
        ("blur", blur),
        ("sharpen", sharpen),
        ("draw", open_drawing_window),
        ("undo", undo),
        ("reset", reset)
    ]
    for btn, (key, _) in zip(toolbar.winfo_children(), toolbar_btns):
        btn.config(text=languages[current_lang][key])
    brightness_label.config(text=languages[current_lang]["brightness"])
    contrast_label.config(text=languages[current_lang]["contrast"])

lang_frame=tk.Frame(root)
lang_frame.pack(side="top", pady=5)
for lang in languages:
    tk.Button(lang_frame,text=languages[lang]["language"],command=lambda l=lang:set_language(l)).pack(side="left", padx=5)

original_image=None
edited_image=None
undo_stack=[]

def open_image_tab2():
    global original_image,edited_image
    path=filedialog.askopenfilename(filetypes=[("Images","*.jpg *.png *.jpeg")])
    if not path: return
    original_image=Image.open(path).convert("RGB")
    edited_image=original_image.copy()
    undo_stack.clear()
    show_preview_tab2(edited_image)

def save_image_tab2():
    global edited_image
    if not edited_image: return
    path=filedialog.asksaveasfilename(defaultextension=".jpg")
    if path:
        edited_image.save(path)
        messagebox.showinfo("Saved","Image saved successfully!")

def show_preview_tab2(img):
    img_copy=img.copy()
    max_width, max_height = 1000, 600
    img_copy.thumbnail((max_width,max_height))
    tk_img=ImageTk.PhotoImage(img_copy)
    preview_label.config(image=tk_img)
    preview_label.image=tk_img

def apply_edit(fn):
    global edited_image
    if edited_image:
        undo_stack.append(edited_image.copy())
        edited_image=fn(edited_image)
        show_preview_tab2(edited_image)

def rotate_left(): apply_edit(lambda img: img.rotate(90,expand=True))
def rotate_right(): apply_edit(lambda img: img.rotate(-90,expand=True))
def flip_h(): apply_edit(lambda img: img.transpose(Image.FLIP_LEFT_RIGHT))
def flip_v(): apply_edit(lambda img: img.transpose(Image.FLIP_TOP_BOTTOM))
def grayscale(): apply_edit(lambda img: img.convert("L").convert("RGB"))
def blur(): apply_edit(lambda img: img.filter(ImageFilter.GaussianBlur(3)))
def sharpen(): apply_edit(lambda img: img.filter(ImageFilter.SHARPEN))

def sepia():
    def fn(img):
        px=img.load()
        for y in range(img.height):
            for x in range(img.width):
                r,g,b=px[x,y]
                tr=int(0.393*r+0.769*g+0.189*b)
                tg=int(0.349*r+0.686*g+0.168*b)
                tb=int(0.272*r+0.534*g+0.131*b)
                px[x,y]=(min(255,tr),min(255,tg),min(255,tb))
        return img
    apply_edit(fn)

def adjust_brightness(v):
    if edited_image:
        img=ImageEnhance.Brightness(edited_image).enhance(float(v))
        show_preview_tab2(img)

def adjust_contrast(v):
    if edited_image:
        img=ImageEnhance.Contrast(edited_image).enhance(float(v))
        show_preview_tab2(img)

def undo():
    global edited_image
    if undo_stack:
        edited_image=undo_stack.pop()
        show_preview_tab2(edited_image)

def reset():
    global edited_image
    if original_image:
        edited_image=original_image.copy()
        undo_stack.clear()
        show_preview_tab2(edited_image)

def open_drawing_window():
    if not edited_image:
        messagebox.showerror("Error","Open an image first.")
        return
    draw_win=tk.Toplevel(root)
    draw_win.title("Drawing Overlay")
    draw_img=edited_image.copy()
    tk_img=ImageTk.PhotoImage(draw_img)
    canvas=tk.Canvas(draw_win,width=tk_img.width(),height=tk_img.height())
    canvas.pack()
    canvas.create_image(0,0,anchor="nw",image=tk_img)
    canvas.image=tk_img
    color="#ff0000"
    brush_size=tk.IntVar(value=5)
    def choose_color():
        nonlocal color
        c=colorchooser.askcolor()[1]
        if c: color=c
    def draw(event):
        x,y=event.x,event.y
        r=brush_size.get()
        canvas.create_oval(x-r,y-r,x+r,y+r,fill=color,outline=color)
    def place_sticker(shape):
        x=simpledialog.askinteger("X","X position:",minvalue=0,maxvalue=draw_img.width)
        y=simpledialog.askinteger("Y","Y position:",minvalue=0,maxvalue=draw_img.height)
        draw=ImageDraw.Draw(draw_img)
        if shape=="heart": draw.text((x,y),"❤️",fill=color)
        elif shape=="star": draw.text((x,y),"⭐",fill=color)
        elif shape=="smile": draw.text((x,y),"😊",fill=color)
        update_canvas()
    def update_canvas():
        tk_new=ImageTk.PhotoImage(draw_img)
        canvas.create_image(0,0,anchor="nw",image=tk_new)
        canvas.image=tk_new
    canvas.bind("<B1-Motion>",draw)
    tk.Button(draw_win,text="Color",command=choose_color).pack(side="left")
    tk.Scale(draw_win,label="Brush",variable=brush_size,from_=1,to=50,orient="horizontal").pack(side="left")
    for s in ["heart","star","smile"]:
        tk.Button(draw_win,text=s,command=lambda sh=s:place_sticker(sh)).pack(side="left")
    tk.Button(draw_win,text="Done",command=lambda:[apply_edit(lambda img: draw_img.copy()),draw_win.destroy()]).pack(side="right")

# Toolbar
toolbar=tk.Frame(tab2)
toolbar.pack(side="top",fill="x")
for key,fn in [
    ("open_image", open_image_tab2),
    ("save_image", save_image_tab2),
    ("rotate_left", rotate_left),
    ("rotate_right", rotate_right),
    ("flip_h", flip_h),
    ("flip_v", flip_v),
    ("grayscale", grayscale),
    ("sepia", sepia),
    ("blur", blur),
    ("sharpen", sharpen),
    ("draw", open_drawing_window),
    ("undo", undo),
    ("reset", reset)
]:
    tk.Button(toolbar,text=languages[current_lang][key],command=fn).pack(side="left", padx=2)

slider_frame=tk.Frame(tab2)
slider_frame.pack(side="top", pady=5)
brightness_label=tk.Label(slider_frame,text=languages[current_lang]["brightness"])
brightness_label.pack(side="left")
tk.Scale(slider_frame,from_=0.1,to=2,resolution=0.1,orient="horizontal",command=adjust_brightness).pack(side="left")
contrast_label=tk.Label(slider_frame,text=languages[current_lang]["contrast"])
contrast_label.pack(side="left")
tk.Scale(slider_frame,from_=0.1,to=2,resolution=0.1,orient="horizontal",command=adjust_contrast).pack(side="left")

preview_label=tk.Label(tab2)
preview_label.pack(pady=10)

root.mainloop()
