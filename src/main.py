from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
import json
from  haralyzer import HarParser, HarPage
## TODO 
# 1. 창 크기가 변해도 위의 텍스트 부분은 변하면 안된다. 이거 수정 할 것
# 2. 트리뷰는  
## nameing convention
# Nm = Name
# Tt = Title
# Lbl = Label
# Frm = Frame
# Sz = Size
# Lt = Load Time
# Ls = List

#FILE="/Users/jason/project/harparser/tkdocs.com_Archive [25-02-14 14-28-10].har"

#harData = HarParser.from_file(FILE)   
pageLsUrls = list()
pageLsPageId = list()
pageLsUrls = list()
pageLsPageId = list()
pageEntries = dict() 
pageSize = list()  
pageLoadTime = list()
pageSize.append(0)
pageLoadTime.append(0)
entries = list()
fileName = "" 
harData = dict()  

def openfile(): 
    pageLsUrls.clear()
    pageLsUrls.append("<select>")
    pageLsPageId.clear()
    pageLsPageId.append("none")
    fileName = filedialog.askopenfilename()
    harData = HarParser.from_file(fileName) 
    pageSizeText.set(0)
    pageLoadTimeText.set(0)
    tree.delete(*tree.get_children()) 
    
    brwsrNmText.set(harData.creator['name'])
    brwsrVerText.set(harData.creator['version'])  
    for page in harData.pages:
        pageLsUrls.append(page.url)
        pageLsPageId.append(page.page_id)
        pageSize.append(str(page.page_size))
        pageLoadTime.append(page.page_load_time)
        pageEntries[page.page_id] = page.entries
    
    pageListComboBox['values'] = pageLsUrls   
 
def selectedPageId(event):  
    tree.delete(*tree.get_children()) 
    id = pageListComboBox.current()
    if id == 0:
        pageSizeText.set(0)
        pageLoadTimeText.set(0)
        tree.delete(*tree.get_children()) 
    else:
        pageSizeText.set(pageSize[id])
        pageLoadTimeText.set(pageLoadTime[id])
        getEntries(pageLsPageId[id])


def getEntries(page_id): 
    if "page_" in page_id:
        i=0 
        for entry in pageEntries[page_id]:  
            elapsed = 0 
            entries.append(entry)
            for k,v in (entry.timings).items(): 
                elapsed = elapsed + v  
                
            tree.insert('','end',text=i, values=(entry.response.status, entry.request.method, entry.request.host, entry.request.url, entry.response.bodySize, elapsed))
            i = i+1 
            
            
def getTabContent(event):    
    id = tree.item(tree.focus())['text'] 
    #requestHeaders= entries[id].request.headers
    #responseHeaders = entries[id].response.headers   
    i = 0 
    headerBoxtv.delete(*headerBoxtv.get_children())
    cookieBoxtv.delete(*cookieBoxtv.get_children())
    reqHeaderId = headerBoxtv.insert('',"end", values=('RequestHeader'), open=True)
    resHeaderId = headerBoxtv.insert('',"end", values=('ResponseHeader'), open=True)
    for item in entries[id].request.headers: 
        headerBoxtv.insert(reqHeaderId,"end", values=(item['name'],item['value']))
    for item in entries[id].response.headers: 
        headerBoxtv.insert(resHeaderId,"end", values=(item['name'],item['value']))
   
    reqCookiesId = cookieBoxtv.insert('','end', values=('Cookies'), open=True)
    for item in entries[id].request.cookies:
        cookieBoxtv.insert(reqCookiesId,"end", values=(item['name'],item['value']))
    
    
   
root = Tk()
root.title("Har Parser")
#root.minsize(500,400)
root.resizable(True, True) 
root.grid_columnconfigure(2, weight=1) 
root.grid_rowconfigure(3, weight=1) 

fileFrm = ttk.Frame(root, relief="groove", border=2)
fileFrm.grid(column=0, row=0, sticky="WN")  
fileBtn = ttk.Button(fileFrm, text="Har choose", command=openfile) 
fileBtn.grid(column=0, row=0)

infoFrm = ttk.Frame(root, relief="solid", border="2")
infoFrm.grid(column=0, row=1, sticky="WN", ipadx=2, ipady=2, padx=2, pady=2)
infoFrm.grid_columnconfigure(4, weight=1)
infoFrm.grid_rowconfigure(4, weight=1)
## inside infoFrm 
brwsrNmLabel = ttk.Label(infoFrm , text="browser :")
brwsrNmLabel.grid(column=0, row=0, sticky="NW")
brwsrNmText = StringVar()
brwsrNmTextLabel=ttk.Label(infoFrm, textvariable=brwsrNmText)
brwsrNmTextLabel.grid(column=1, row=0, sticky="NW")
#brwsrNmText.set(harData.browser['name'])

brwsrVerLabel = ttk.Label(infoFrm , text="| version :")
brwsrVerLabel.grid(column=2, row=0)
brwsrVerText = StringVar()
brwsrVerTextLabel=ttk.Label(infoFrm, textvariable=brwsrVerText)
brwsrVerTextLabel.grid(column=3, row=0, sticky="NW")
#brwsrVerText.set(harData.browser['version'])

pageListLabel = ttk.Label(infoFrm, text="url :")
pageListLabel.grid(column=0, row=1, sticky="NW")

pageListText = StringVar()
pageListComboBox = ttk.Combobox(infoFrm)
pageListComboBox.grid(column=1, row=1, columnspan=3)
pageListComboBox.bind('<<ComboboxSelected>>', selectedPageId)


pageSizeLabel = ttk.Label(infoFrm, text="Page size :") 
pageSizeLabel.grid(column=0, row=3, sticky="NW") 
pageSizeText = IntVar() 
pageSizeTextLabel=ttk.Label(infoFrm, textvariable=pageSizeText)
pageSizeTextLabel.grid(column=1, row=3, sticky="NW", rowspan=3)  

pageLoadTimeLabel = ttk.Label(infoFrm, text="Load time :")  
pageLoadTimeLabel.grid(column=0, row=4, sticky="NW")
pageLoadTimeText = IntVar() 
pageLoadTimeTextLabel=ttk.Label(infoFrm, textvariable=pageLoadTimeText)
pageLoadTimeTextLabel.grid(column=1, row=4, sticky="NW", rowspan=3)  


dataFrm = ttk.Frame(root, border=2, relief="ridge")
#dataFrm.grid_columnconfigure(2, weight=1) 
#dataFrm.grid_rowconfigure(2, weight=1)    
dataFrm.columnconfigure(2, weight=1)
dataFrm.grid(column=0, row=2, sticky="WN") 

entryFrm = ttk.Frame(dataFrm,  border="1", relief="solid") 
entryFrm.columnconfigure(2, weight=1)
entryFrm.grid(column=0, row=0, sticky="NSW")

tree = ttk.Treeview(entryFrm, height=20, selectmode="browse")
verticalBar = ttk.Scrollbar(entryFrm, orient="vertical", command=tree.yview)
verticalBar.grid(column=1, row=0 , sticky="ENS")
tree.configure(yscrollcommand=verticalBar.set) 

tree['columns'] = ("0","1","2","3","4","5")
tree.column("#0", width=35)
tree.heading("#0", text="no") 

tree.column("#1", width=50)
tree.heading("#1", text="stauts") 

tree.column("#2", width=50)
tree.heading("#2", text="Method")  

tree.column("#3", width=180, anchor="w")
tree.heading("#3", text="Hostname")  

tree.column("#4", width=250, anchor="w")
tree.heading("#4", text="Url")
 
tree.column("#5", width=50, anchor="e") 
tree.heading("#5", text="size")  

tree.column("#6", width=70 , anchor="e")
tree.heading("#6", text="elapsed") 

#tree.column("#7", width=70)
#tree.heading("#7", text="timings") 

tree.grid(column=0, row=0 , sticky="NSW")
tree.bind("<ButtonRelease-1>", getTabContent)

detailFrm = ttk.Frame(dataFrm, relief="groove", border=2) 
detailFrm.grid(column=1, row=0, sticky="E") 
tabControl = ttk.Notebook(detailFrm)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl) 

tabControl.add(tab1, text="headers") 
tabControl.add(tab2, text="cookies")
tabControl.add(tab3, text="requests")
tabControl.add(tab4, text="response")
tabControl.grid(column=1, row=0) 

headerBoxtv = ttk.Treeview(tab1, columns=("0","1"), height=20)
headerBoxtv.column("#0", width=2)
headerBoxtv.grid(column=0, row=0, sticky="WENS")  
cookieBoxtv= ttk.Treeview(tab2, columns=("0","2"), height=20)
cookieBoxtv.column("#0", width=2)
cookieBoxtv.grid(column=0, row=0, sticky="WENS")  

requestBoxContent = StringVar()
requestBox= ttk.Label(tab3, textvariable=requestBoxContent)
requestBox.grid(column=0, row=0, sticky="WENS")  

responseBoxContent = StringVar()
responseBox= ttk.Label(tab4, textvariable=responseBoxContent)
responseBox.grid(column=0, row=0, sticky="WENS")   
root.mainloop()