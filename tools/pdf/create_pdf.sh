#!/bin/bash

#usage
show_help() {
cat << EOF
Parameters:
-----------------------------------------------------------------------------------------------------
    -h                          Display this help and exit.
    -i  [INPUT]                 XML file exported from Lingtrain Studio.
    -x  [./book2html.xslt]      XSLT transformation file, which will transform XML input data to HTML
    -s  [./book.css]            CSS style file.
    -p  [./covers/default.jpg]  Image (3/4 ratio), which will be used as book cover.
                                (!) Image Path should be relative to XML input data path.
    -c  [false]                 Add color highlighting.
    -t  [false]                 Add furigana-style tips for Chinese and Japanese texts.
    -o  [OUTPUT]                Output PDF file.
-----------------------------------------------------------------------------------------------------
EOF
}

#default parameters
xslt="./book2html.xslt"
cover="./covers/default.jpg"
css="./book.css"
data="./book.xml"
output_path="./result.pdf"
show_colors="false"
cjk_tips="false"
layout_type="0"

while getopts hi:s:x:p:o:l:ct opt; do
    case $opt in
        h)  show_help
            exit 0
            ;;
        i)  data=$OPTARG
            ;;
        s)  css=$OPTARG
            ;;
        x)  xslt=$OPTARG
            ;;
        p)  cover=$OPTARG
            ;;
        o)  output_path=$OPTARG
            ;;
        t)  cjk_tips="true"
            ;;
        c)  show_colors="true"
            ;;
        l)  layout_type=$OPTARG
            ;;
        *)  show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"

### check parameters
cat << EOF
-----------------------------------------------------------------------------------------------------
Book parameters:

    - Input file:           $data
    - Output file:          $output_path
    
    - XSLT tranformation:   $xslt
    - CSS styles:           $css
    - Cover image:          $cover (path is relative to input file).
    - Color highlighting:   $show_colors
    - Tips (zh, jp langs):  $cjk_tips
-----------------------------------------------------------------------------------------------------
EOF

### generate book

html="$data.html"
img=$(echo "$cover" | sed 's/\//\\\//g')

echo "Replacing parameters in xslt..."

sed -e "s/\$COVER_IMG/$img/; s/\$SHOW_COLORS/$show_colors/; s/\$CJK_TIPS/$cjk_tips/; s/\$LAYOUT_TYPE/$layout_type/" $xslt > _temp.xslt

echo "Generating html file $html..."

saxonb-xslt -s:$data -xsl:_temp.xslt -o:$html

echo "Creating PDF $output_path..."

weasyprint -s $css $html $output_path

echo "Removing temp files..."

rm $html
# rm _temp.xslt

echo "Done."