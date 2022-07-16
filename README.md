# Library-Generator
## Overview
This program, when run from the command line insode a directory that contains a sub-directory called `Library` will generate a static, wiki-like, filesystem based single page application to display the contents of `Library` in a browser. 

## Library Structure
Lnitially the root of the library (directory name is the default page title) nee only contain the Library folder, if nit already defined the image directory will be created and populated along with the index.html file. After execution the top level structure will look like this:

```
<root dir>
┃
┣━ images ━┓
┃          ┣━ tree_closed.gif 
┃          ┃  
┃          ┗━ tree_open.gif
┃ 
┣━ Library ━┓
┃           ┃           
┃           …
┃ 
┗━ index.html
```

Where … represents the displayable content.

## Displayable content
The underlying directory structure is presented as an expanding tree view to the left of the display area. The same item can appear at multiple points in the tree by means of synbolic links, The display area supports several types of content explicitly (PDF, Markdown, Text files) but can display any content that the browser supports and can display in an IFrame.

## Organization
While not strictly necessary the application support name prefixing to control the order of presentation, this is of the form ***xnn-*** where ***x*** is in the range **0-9 A-Z a-z**, and ***n*** in the range **0-9**. This prefix is striped before using the File/Directory as the anchor for the item.

The prefix ***x00*** is special and trated differently, it represent a link to a file that is used to replace it's parent directory in the tree view. When the anchor is clicked in the tree view in addition to opening the sub-tree the content if the file is displayed. This allow for an overview of the contents to be presented. The content remains until another entity is clicked, closing the sub-tree does not clear this content. 

## Name Mangling
To provide a fairly consistent look and feel to the tree view the entity (file/directory) name is edited before display. The following operations occur, **▿** represents a space character:

* The collating prefix is removed.
* Any file extension is removed.
* The name is conveted to Title case.
* The sequence **▿_▿**, is replaced with **,▿**.  
* The sequence **▿-▿**, is replaced with **,▿**.   
* The sequence **▿–▿**, is replaced with **,▿**, the – character is U2013 (EN DASH)

Additional edits will be added as needed.