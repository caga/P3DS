# P3DS
Project Design, Development and Documentation Server

Based on python, markdown, plantuml and pandoc. 

## What does it do?
Basicly it looks and searchs markdown files under "markdown/" folder, it allows using plantuml statements in these files, generates html files from them into "web/" folder. Also it adds list of the files into index.html. You can also find and use Bulma.css under "web/" folder.
### How to make it go.
First of all you need to found a virtual python environment, source it and install packages in "requirements.txt". You also need to have "pandoc" installed system wide and also need to have "plantuml.jar" in your path. Make a script file like the following and put it in path (dont forget to make it executable - chmod +x)

    #!/bin/bash
    java -jar /path/to/plantuml.jar ${@}


Project basicly consists of four python script: "server.py", "createDesignDocs.py", "watch.py", "dosya.py".

In a terminal window:

    python server.py

In a seperate terminal:

    python watch.py

You are now good to go. Just add or edit markdown files and they will be automatically converted and added to index.html.

### Important
watch.py script, at start (on purpose) , deletes all files under "web/" directory except index.html and files named like pattern: "filename.onyuz.html". So be careful!!!

