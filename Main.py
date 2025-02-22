from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
from pygments import lex
from pygments.lexers import PythonLexer

main = Tk()
main.title("Pithon")

image = PhotoImage(file = "/Users/dog/Documents/pithon-logo.png")
main.iconphoto(True, image)

TAG_STYLES = {
    'error':                {'background': '#ffddbb'},
    'Token.Comment':        {'foreground': '#009999'},
    'Token.Constant':       {'foreground': '#FF00FF'},
    'Token.Special':        {'foreground': '#ff8080'},
    'Token.Identifier':     {'foreground': '#00FFFF'},
    'Token.Statement':      {'foreground': '#FFFF00'},
    'Token.PreProc':        {'foreground': '#add8e6'},
    'Token.Type':           {'foreground': '#00FF00'},
    'Token.Keyword':        {'foreground': '#FFA500'},
    'Token.Name':           {'foreground': 'black'},
    'Token.Name.Builtin':   {'foreground': '#0033EE'},
    'Token.Name.Function':  {'foreground': '#00EEFF'},
    'Token':                {'foreground': 'black'},
    'Token.Literal.Number': {'foreground': 'red'},
    'Token.Literal.String': {'foreground': 'darkred'},
    'Token.Literal.String.Escape': {'foreground': '#ff00ff'},
    'Token.Delimiter':      {'foreground': '#add8e6'},
    'Token.Punctuation':    {'foreground': 'green'},
    'Token.Operator':       {'foreground': 'darkgreen'},
}

l2 = Label(text='')
l2.grid(row=1, column=0)

def run_code():
    code = text.get("1.0", "end")
    scope = {}
    scope = {}
    exec('from tkinter import *', scope, scope)
    exec('from tkinter.filedialog import *', scope, scope)
    try:
        exec(code, scope, scope)
        l2.config(text=' ')
    except Exception as e:
        l2.config(text=e)
        lineno, offset = find_error_pos(e, scope)
        if lineno is not None:
            text.tag_add('error', f'{lineno}.0', f'{lineno+1}.0')
            text.mark_set('insert', f'{lineno}.{offset}')
            text.see('insert')

def find_error_pos(e, scope):
    if isinstance(e, SyntaxError):
        return e.lineno, e.offset - 1
    frame_list = get_frame_list(e)
    error_lineno = None
    for frame, lineno in frame_list:
        if frame.f_globals is scope:
            error_lineno = lineno
            print(f'lineno={lineno}')
    return error_lineno, 0

def get_frame_list(e):
    tb = e.__traceback__
    frame_list = []
    while tb:
        frame_list.append((tb.tb_frame, tb.tb_lineno))
        tb = tb.tb_next
    return frame_list

def key_event_handler(key):
    highlight()

text = ScrolledText(main)
text.grid(row=0, column=0)
text.bind("<KeyRelease>", key_event_handler)


def highlight():
    for tag in text.tag_names():
        text.tag_delete(tag)

    for tag_name, tag_style in TAG_STYLES.items():
        text.tag_configure(tag_name, tag_style)

    text.mark_set("range_start", "1.0")
    textg = text.get("1.0", "end-1c")
    for token, content in lex(textg, PythonLexer(stripnl=False)):
        token_name = str(token)
        while token_name not in TAG_STYLES:
            token_name = token_name.rsplit('.', 1)[0]
        text.mark_set("range_end", "range_start + %dc" % len(content))
        text.tag_add(token_name, "range_start", "range_end")
        text.mark_set("range_start", "range_end")

entry = Entry(main)
entry.grid(row=4, column=0)

def open_file():

    aof = askopenfile()
    deaof = aof.read()
    text.delete("1.0", "end")
    text.insert("1.0", deaof)
    aof.delete(0, END)
    aof.insert(0, aof.name)
    highlight()

def save_file():

    eg = entry.get()
    with open(eg, "w") as f:
        tg = text.get("1.0", "end")
        f.write(tg)

b1 = Button(main, text="Run the code", command=run_code)
b1.grid(row=0, column=1)

b2 = Button(main, text="Open file", command=open_file)
b2.grid(row=2, column=0)

b3 = Button(main, text="Save file", command=save_file)
b3.grid(row=3, column=0)

l1 = Label(main, text="Modules already installed:\ntkinter,\n tkinter.filedialog,\n pygments.lex,\nfrom pygments.lexer PythonLexer")
l1.grid(row=0, column=2)

highlight()
main.mainloop()
