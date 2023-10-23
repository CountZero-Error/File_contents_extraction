# File_contents_extraction
This script is aim to extract contents from file with a target list.

# installation
```pip install -r requirements.txt```

# usage:  
<pre>
target_contents_extraction.py [-h] -C CATALOG_FILE  
                                   -I INPUT_FILE  
                                   -O OUTPUT_FILE  
                                   -R REGEX  
                                  [-TR TARGET_REGEX]  
                                  [-CSEP CATALOG_SEPRATE]  
                                  [-CN COL_NUMBER]  
                                  [-CH CATALOG_HEADER]
</pre>

# options:  
<pre>
  -h, --help            show this help message and exit  
  -C CATALOG_FILE, --CATALOG_FILE CATALOG_FILE  
                   File contains the list of targets that you want to extract.  
  -I INPUT_FILE, --INPUT_FILE  
                   INPUT_FILE File to be extracted.  
  -O OUTPUT_FILE, --OUTPUT_FILE OUTPUT_FILE  
                   Output file path.  
  -R REGEX, --REGEX REGEX  
                   Regulation expression, format: 'ex(target)pression', the ' is needed and you need include your target inside the () as the program will read group 1 as result.  
                   Regulation expression reference site: https://c.runoob.com/front-end/854/  
  -TR TARGET_REGEX, --TARGET_REGEX TARGET_REGEX  
                   The regex that extract the part of the content instead the whole line, default is extract whole line.  
  -CSEP CATALOG_SEPRATE, --CATALOG_SEPRATE CATALOG_SEPRATE  
                   The sepration of the catalog file, default if tab.  
  -CN COL_NUMBER, --COL_NUMBER COL_NUMBER  
                   Target column number of the catalog file, default is 0.  
  -CH CATALOG_HEADER, --CATALOG_HEADER CATALOG_HEADER  
                   Choose a line as the header line of the catalog file, default is None.  
</pre>
  
# Example
aim to extract the id from example.csv
```target_contents_extraction.py -C catalog.txt -I example.csv -O extraction.csv -R '\d*(\w*)\d*' -TR 'id=(\d*);'```  
<pre>
- catalog.txt:
  targetA
  targetB
  ...

- example.csv:
  Line_1  abc  123targetA456  id=123;
  Line_2  def  456targetB789  id=456
  ...

- extraction.csv
  123
  456
  ...
</pre>
