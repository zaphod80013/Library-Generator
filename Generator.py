import base64
import os
import sys
import re
import sys
import urllib.parse

class Generator:

    def __init__(self):
        self.program            =  os.path.basename(sys.argv[0])              # program name
        self.version            = '1.0.0'                                     # program version
        self.debug              =   True                                      # Debug indentation etc.
        self.recursionDepth     =   0                                         # Recursion Depth  
        self.divDepth           =   0                                         # <div> nesting Depth 
        self.indentation        =   0                                         # Indentation level for readable html
        self.id                 =   0                                         # Entity identifer used to uniquly reference element

        #
        # Script must be run from the directory to be indexed
        #
        self.prefix = os.getcwd()
        if not os.path.exists(os.path.join(self.prefix,"Library")):
            sys.exit("Invalid Directroy Structure: No 'Library' folder")
        #
        # Browser Tab Title
        #
        if len(sys.argv) > 1:
            self.title = sys.argv[1]
        else:
            self.title = os.path.basename(self.prefix)    
        #
        # CSS Borders do not support percentages and you can't easily 
        # mix relative and absolute measurements, therefore we use margins
        # which support percentage values as a percentage of their enclosing 
        # container to emulate borders
        #
        self.outerBorderTop     =   0.4
        self.outerBorderRight   =   0.4
        self.outerBorderBottom  =   0.2
        self.outerBorderLeft    =   0.2
        #
        # Background colours
        #
        self.htmlBgColor        = "green"      #"#0000ff"                 
        self.bodyBgColor        = "green"      #"#aaeeaa"  
        self.northBgColor       = "#aaeeaa"               
        self.westBgColor        = "#aaddaa" 
        self.eastBgColor        = "#e0e0e8"               
        self.frameBgColor       = "%23aaddaa"               
        #
        # Pre-defined Height & Width of various components
        #
        self.bodyHeight         = 100
        self.bodyWidth          = 100
        self.westWidth          =  25.0
        self.frameHeight        =  99.5 #99.79
        self.frameWidth         =  99.5 #99.79
        #
        # Derived  Height & Width of various components
        #
        self.innerBorderRight   =  self.outerBorderRight / 2
        self.innerBorderLeft    =  self.outerBorderLeft  / 2

        self.containerHeight    =  self.bodyHeight - self.outerBorderTop - self.outerBorderBottom  
        self.containerWidth     =  self.bodyWidth  - self.outerBorderLeft - self.outerBorderRight 
        self.eastWidth          =  self.containerWidth 
        self.northWidth         =  self.containerWidth 
        self.eastHeight         =  self.containerHeight 
        self.westHeight         =  self.containerHeight 
        #
        # Tree Open/Close gif - Base 64 encoded binary data
        #
        self.treeOpenGif        = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAElBMVEWAgIAkJCQkJCQmJiYkJCT///+DTqfbAAAABHRSTlMCeICB4kS8BAAAAAFiS0dEBfhv6ccAAAAjSURBVAjXY2AgDzC6AIECiCXi4uIEE1KASIo4QVUxG5BqLgDx6QNC/tG5xQAAAABJRU5ErkJggg=="
        self.treeClosedGif      = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAElBMVEWAgIAkJCQmJiYlJSUkJCT///+1BnEDAAAABHRSTlMCgIGJTlMnHwAAAAFiS0dEBfhv6ccAAAArSURBVAjXY2DACwxgDGcYwwUm5AITcoEJubgIQBmOMCmoAANMgEEBv30MACTRA/k4/oFrAAAAAElFTkSuQmCC"
        #
        # Run the  Generator 
        #
        self.run(self.prefix)

    #------------------------------------------------------------------------------------------------------------------
    #   Utiity Functions
    #------------------------------------------------------------------------------------------------------------------

    def recursiveEnter(self,path):
        if self.debug:
            print(f"Recursive Enter Level: {self.recursionDepth} -->  {path}")
            self.recursionDepth  += 1

    def recursiveExit(self,path):    
        if self.debug:
            self.recursionDepth  -= 1
            print(f"Recursion Exit  Level: {self.recursionDepth} --> {path}")


    def getSortedDirectoryContent(self,path):
        """sort directory entries"""
        files = os.listdir(path)
        files.sort(key=str.casefold)
        return files


    #------------------------------------------------------------------------------------------------------------------
    #   Output Routines
    #------------------------------------------------------------------------------------------------------------------
 
    def getID(self):
        self.id += 1
        return ("0000" + str(self.id))[-4:]

    def indent(self):

        self.indentation += 1

    def outdent(self):
        self.indentation -= 1  if self.indentation > 0 else 0

    def write(self, text):
        indent = "   " * self.indentation
        self.file.write(f"{indent}{text}\n")
        if self.debug:
            print(f"{indent}{text}")

    def writeTreeOpen(self, path):
        dir = os.path.join(path,"images")
        if not os.path.exists(dir):
            os.mkdir(dir)

        file = os.path.join(dir,"tree_open.gif")
        if not os.path.exists(file):
            with open(file, 'wb') as f:
                f.write(base64.b64decode(self.treeOpenGif))

    def writeTreeClosed(self,path):
        dir = os.path.join(path,"images")
        if not os.path.exists(dir):
            os.mkdir(dir)

    def openDiv(self, content):
        if self.debug:
            self.write(f"<!-- Start {self.divDepth} {self.indentation} -->")
  
        self.write(content)      
        self.divDepth += 1
        self.indent()        

    def closeDiv(self):
        self.divDepth -= 1
        self.outdent()
        self.write("</div>")
        if self.debug:
            self.write(f"<!-- End   {self.divDepth} {self.indentation} -->")

    def openBrace(self):
        self.write("{")
        self.indent()

    def closeBrace(self,extra=''):
        self.outdent()
        self.write("}" + extra)

    def writeConfigFunction(self):
        self.write("function config()")
        self.openBrace()
        self.write("x = document.getElementById('0001');")
        self.write("var y = x.id+'B';")
        self.write("var z = x.id+'A';")
        self.write("y = document.getElementById(y);")
        self.write("z = document.getElementById(z);")
        self.write("y.style.display='block';")
        self.write("z.src='images/tree_open.gif';")
        self.write("for(let i=0; i < x.childNodes.length; i++)")
        self.openBrace()
        self.write("y = x.childNodes[i];")
        self.write("if(y.nodeName == 'SPAN')")
        self.openBrace()
        self.write("y.click();")
        self.closeBrace()
        self.closeBrace()
        self.write("return false;")
        self.closeBrace()

    def writeToggleDisplayFunction(self):
        self.write("function toggleDisplay(x)")
        self.openBrace()
        self.write("if(!(x.id == undefined))")
        self.openBrace()
        self.write("var y = x.id+'B';")
        self.write("var z = x.id+'A';")
        self.write("if(event.target.id == z)")
        self.openBrace()
        self.write("y = document.getElementById(y);")
        self.write("z = document.getElementById(z);")
        self.write("if(y.style.display == 'none')")
        self.openBrace()
        self.write("y.style.display='block';")
        self.write("z.src='images/tree_open.gif';")
        self.closeBrace()
        self.write("else")
        self.openBrace()
        self.write("y.style.display='none';")
        self.write("z.src='images/tree_closed.gif';")
        self.closeBrace()
        self.closeBrace()
        self.closeBrace()
        self.write("return false;")
        self.closeBrace()

    def writeDisplayFunction(self):
        self.write("function display(x)")
        self.openBrace()
        self.write("document.getElementById('page').src=atob(x);")  
        self.closeBrace()

    def writeDisplayMarkdownFunction(self):
        self.write("function displayMarkdown(x)")
        self.openBrace()
        head = '<html>\n<body>\n'\
               '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/base16/hardcore.min.css"></link>\n'\
               '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>\n'\
               '<script>\nhljs.highlightAll();\n</script>'\
               '</head>\n<body>\n'        
        head = base64.b64encode(head.encode("utf-8")).decode()
        self.write(f"head  = '{head}'")
        tail = '\n</body>\n</html>\n'
        tail = base64.b64encode(tail.encode("utf-8")).decode()
        self.write(f"tail = '{tail}'")   

        self.write( 'showdown.extension("codehighlight", ')
        self.openBrace()
        self.write( 'type: "output",')
        self.write( 'filter: function (text, converter, options)')
        self.openBrace()
        self.write( "// use shodown's regexp engine to conditionally parse codeblocks")
        self.write( 'var left = "<pre><code\\b[^>]*>",')
        self.write( 'right    = "</code></pre>",')
        self.write( 'flags    = "g",')
        self.write( 'replacement = function (wholeMatch, match, left, right)')
        self.openBrace()
        self.write( '// unescape match to prevent double escaping')
        self.write( 'match = match.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");')
        self.write( 'return left + hljs.highlightAuto(match).value + right;')
        self.closeBrace(';')
        self.write( 'return showdown.helper.replaceRecursiveRegExp(text, replacement, left, right, flags);')
        self.closeBrace()
        self.closeBrace(');')
        self.write( "md = atob(x);")
        self.write( "console.log(decodeURI(md));")
        self.write( "var converter = new showdown.Converter();")
        self.write( "var html = converter.makeHtml(md).substring(0);")
        self.write( "html = atob(head) + html + atob(tail);")
        self.write( "console.log(html);")
        self.write( "document.getElementById('page').src='data:text/html;charset=utf-8,' + html;")
        self.closeBrace()

    def openStyle(self,style):
        self.indent()
        self.write(style + " {")
        self.indent()   

    def closeStyle(self):
        self.outdent()
        self.write( "}")
        self.outdent()

    def defaultBox(self):
        self.write( "margin:            0%;")
        self.write( "border:            0%;")
        self.write( "padding:           0%;")
    
    def writeHtmlStyle(self):
        self.openStyle('html')       
        self.write( "height:            100%;")
        self.write( "width:             100%;")
        self.defaultBox()
        self.write(f"background-color:  {self.htmlBgColor};")
        self.closeStyle()

    def writeBodyStyle(self):
        self.openStyle('body')       
        self.write(f"height:            {self.bodyHeight}%;")
        self.write(f"width:             {self.bodyWidth}%;")
        self.defaultBox()
        self.write(f"background-color:  {self.bodyBgColor};")
        self.write( "display:           flex;")
        self.write( "flex-flow:         column;")
        self.write( "font-size:         100%;")
        self.closeStyle()

    def writeContainerStyle(self):
        self.openStyle('.container')       
        self.write(f"height:            {self.containerHeight}%;")  
        self.write(f"width:             {self.containerWidth}%;")
        self.write( "padding:           0%;")
        self.write(f"margin-top:        {self.outerBorderTop}%;")
        self.write(f"margin-right:      {self.outerBorderRight}%;")
        self.write(f"margin-bottom:     {self.outerBorderLeft}%;")
        self.write(f"margin-left:       {self.outerBorderLeft}%;")
        self.write( "display:           flex;")
        self.write( "flex-flow:         row;")
        self.closeStyle()

    def writeWestStyle(self):
        self.openStyle('.west')       
        self.write(f"height:            {self.westHeight}%;")
        self.write(f"width:             {self.westWidth}%;")
        self.write( "margin-top:        0%;")
        self.write(f"margin-right:      {self.innerBorderRight}%;")
        self.write( "margin-bottom:     0%;")
        self.write( "margin-left:       0%;")
        self.write( "overflow-x:        hidden;")
        self.write(f"background-color:  {self.westBgColor};")
        self.closeStyle()

    def writeEastStyle(self):
        self.openStyle('.east')       
        self.write(f"height:            {self.eastHeight}%;")
        self.write(f"width:             {self.eastWidth}%;")
        self.write( "border:            0%;")
        self.write( "margin-top:        0%;")
        self.write( "margin-right:      0%;")
        self.write( "margin-bottom:     0%;")
        self.write(f"margin-left:       {self.innerBorderLeft}%;")
        self.write( "object-fit:        contain;")
        self.write(f"background-color: {self.eastBgColor};")
        self.closeStyle()

    def writeSubSectionStyle(self):
        self.openStyle('.subSection')       
        self.write( "margin-left:       3%;")
        self.closeStyle()
        self.openStyle('.subSection span')       
        self.write( "font-size:         0.95em;")
        self.write( "padding-left:       3.2%;")
        self.closeStyle()

    def writeEntryStyle(self):
        self.openStyle('.entry')       
        self.write( "font-size:         0.95em;")
        self.write( "margin-left:       3.2%;")
        self.write( "overflow-x:        hidden;")
        self.write( "white-space:       nowrap;")
        self.write( "text-overflow:     ellipsis;")
        self.closeStyle()
        self.openStyle('.entry span')       
        self.write( "font-size:         0.95em;")
        self.write( "margin-left:       3.2%;")
        self.closeStyle()
 
    def seperator(self):
        self.write( "")

    def writePrologue(self,title):
        self.write( "<!DOCTYPE HTML>")
        self.write( "<html lang='en'>")
        self.indent()
        self.write( "<head>")
        self.indent()
        self.write(f'<!-- This file generated by {self.program} Version {self.version}: Do Not Edit -->')
        self.write( "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
        self.write(f"<title>{title}</title>")
        #self.write( '<link rel="stylesheet" href="https://jmblog.github.io/color-themes-for-highlightjs/css/themes/tomorrow-night.css">')
        self.write( '<script src="https://cdn.jsdelivr.net/npm/showdown/dist/showdown.min.js"></script>')
        self.write( '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>')
        self.write( "<script type='text/javascript' language='JavaScript'> // <![CDATA[")
        self.indent()
        self.seperator()
        self.writeConfigFunction()
        self.seperator()
        self.writeToggleDisplayFunction()
        self.writeDisplayMarkdownFunction()
        self.seperator()
        self.writeDisplayFunction()
        self.seperator()
        self.outdent()
        self.write( "// ]]>")
        self.write( "</script>")
        self.write( "")
        self.write( "<style>")
        self.indent()
        self.writeHtmlStyle()
        self.writeBodyStyle()
        self.writeContainerStyle()
        self.writeEastStyle()
        self.writeWestStyle()
        self.writeSubSectionStyle()
        self.writeEntryStyle()
        self.outdent()
        self.write( "</style>")
        self.outdent()
        self.write( "</head>")
        self.seperator()
        self.write( "<body onload='config();'>")
        self.indent()
        self.openDiv("<div class='container'>")
        self.openDiv("<div class='west'>")                                                                  

    def writeEpilogue(self):
        self.closeDiv()                                                                              # 1        
        self.openDiv("<div class='east'>")                                                                 
        self.write( "<iframe id='page' name='page' width='100%' height='100%' frameBorder='0'></iframe>")        
        self.closeDiv()
        self.write( "<body>")
        self.outdent()
        self.write( "<html>")

    def sanitizePath(self, path):
        path = "." + path[len(self.prefix):]
        return base64.b64encode(urllib.parse.quote(path).encode("utf-8")).decode()

    def sanatizeMarkdown(self,path):
        with open(path,'r') as f:
            path = ''.join(f.readlines())
        return base64.b64encode(path.encode("utf-8")).decode()  

    def sanitizeName(self,name):
        name = name[4:] if re.match('[0-9a-zA-Z]\d{2}-',name) else name
        name = name[:-(name[::-1].index('.') + 1)]  if '.' in name else name
        name = name.title()
        name = name.replace(' _ ',', ')
        name = name.replace(' - ',', ')
        name = name.replace(u' – ',', ')
        return name

    def directorySection(self,id,path):
        name = self.sanitizeName(os.path.basename(path))
        self.openDiv(f"<div id='{id}' onclick='toggleDisplay(this);' class='section' >")
        self.write(f"<img id='{id}A' src='./images/tree_closed.gif'/><span>{name}</span>")
        self.openDiv(f"<div id='{id}B' style='display:none;'>")

    def markdownSection(self,id,path):
        name = self.sanitizeName(os.path.basename(path))
        path = self.sanatizeMarkdown(path)
        self.openDiv(f"<div id='{id}' onclick='toggleDisplay(this);' class='section' >")
        self.write(f"<img id='{id}A' src='./images/tree_closed.gif'/><span onclick='displayMarkdown(\"{path}\");'>{name}</span>")
        self.openDiv(f"<div id='{id}B' style='display:none;'>")

    def fileSection(self,id,path):
        name = self.sanitizeName(os.path.basename(path))
        path = self.sanitizePath(path)
        self.openDiv(f"<div id='{id}' onclick='toggleDisplay(this);' class='section' >")
        self.write(f"<img id='{id}A' src='./images/tree_closed.gif'/><span onclick='display(\"{path}\");'>{name}</span>")
        self.openDiv(f"<div id='{id}B' style='display:none;'>")

    def openSection(self,path):
        id = self.getID()
        if os.path.isdir(path):
            self.directorySection(id,path)
        else: 
            path = os.path.realpath(path) if os.path.islink(path) else path
            if path[-3:] == '.md':
               self.markdownSection(id,path)
            else:
               self.fileSection(id,path)     

    def closeSection(self,path):
        self.closeDiv()
        self.closeDiv()
  
    def addEntry(self,path):
        path = os.path.realpath(path) if os.path.islink(path) else path
        name = self.sanitizeName(os.path.basename(path)) 
        path = self.sanitizePath(path)        
        if path[-3:] == '.md':
            path =  self.sanatizeMarkdown(path)
            function = 'displayMarkdown'
        else:        
            path = self.sanitizePath(path)
            function = 'display'

        self.write(f"<div class='entry' onclick='{function}(\"{path}\");'><span>{name}</span></div>")

    #------------------------------------------------------------------------------------------------------------------
    #   Main Program
    #------------------------------------------------------------------------------------------------------------------

    def run(self,path):
        self.writeTreeOpen(path)
        self.writeTreeClosed(path)
        file = os.path.join(path,'index.html')
        with open(file, "w") as self.file:
            self.writePrologue(self.title)
            self.processSection(os.path.join(path,"Library"))
            self.writeEpilogue()
 
    def processSection(self,path):
        self.recursiveEnter(path)
        files = self.getSortedDirectoryContent(path)
        for name in files:
            entry = os.path.join(path,name)           
            if re.match('[0-9a-zA-Z]00-',name) or os.path.isdir(entry):
                self.openSection(entry)
                if os.path.isdir(entry):
                    self.processSection(entry)
            else:  
                self.addEntry(entry)
        
        self.closeSection(path)
        self.recursiveExit(path)
                
Generator()