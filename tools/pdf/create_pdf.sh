#!/bin/bash

#usage
show_help() {
cat << EOF
Parameters:
-----------------------------------------------------------------------------------------------------
    -h                          Display this help and exit.
    -i  [INPUT]                 XML file exported from Lingtrain Studio.
    -o  [OUTPUT]                Output PDF file.
    -x  [./book2html.xslt]      XSLT transformation file, which will transform XML input data to HTML
    -s  [./book.css]            CSS style file.
    -p  [./covers/default.jpg]  Image (3/4 ratio), which will be used as book cover.
                                (!) Image Path should be relative to XML input data path.
    -c  [false]                 Add color highlighting.
    -f  [false]                 Add furigana-style tips for Chinese and Japanese texts.
    -t  [0]                     Layout type. 0 is for two cols, 1 is for one.
    -d  [false]                 Apply indentation for paragraphs.
    -j  [false]                 Justify text.
    -m  [10]                    Horizontal page margins in mm.
    -l  [10]                    Left text font size in pt.
    -r  [10]                    Right text font size in pt.
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

text_indent="0"
text_align="left"
margin_l_mm="10"
margin_r_mm="10"
font_size_left="10"
font_size_right="10"

while getopts hi:s:x:p:o:t:cfl:r:m:dj opt; do
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
        f)  cjk_tips="true"
            ;;
        c)  show_colors="true"
            ;;
        t)  layout_type=$OPTARG
            ;;
        m)  margin_l_mm=$OPTARG
            margin_r_mm=$OPTARG
            ;;
        l)  font_size_left=$OPTARG
            ;;
        r)  font_size_right=$OPTARG
            ;;
        d)  text_indent="30"
            ;;
        j)  text_align="justify"
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
    - Layout type:          $layout_type
    - Indentation:          $text_indent px
    - Text alignment:       $text_align
    - Horizontal margins:   $margin_l_mm mm
    - Left text font size:  $font_size_left
    - Right text font size: $font_size_right
-----------------------------------------------------------------------------------------------------
EOF

### generate book

html="$data.html"
img=$(echo "$cover" | sed 's/\//\\\//g')

echo "Replacing parameters in xslt..."

sed -e "s/\$COVER_IMG/$img/; s/\$SHOW_COLORS/$show_colors/; s/\$CJK_TIPS/$cjk_tips/; s/\$LAYOUT_TYPE/$layout_type/" $xslt > _temp.xslt
sed -e "s/\$TEXT_ALIGN/$text_align/; s/\$TEXT_INDENT/$text_indent/; s/\$FONT_SIZE_LEFT/$font_size_left/; s/\$FONT_SIZE_RIGHT/$font_size_right/; s/\$LEFT_MARGIN/$margin_l_mm/; s/\$RIGHT_MARGIN/$margin_r_mm/;" $css > _temp.css

echo "Generating html file $html..."

saxonb-xslt -s:$data -xsl:_temp.xslt -o:$html

echo "Creating PDF $output_path..."

weasyprint -s _temp.css $html $output_path

echo "Removing temp files..."

rm $html
rm _temp.xslt
rm _temp.css

echo "Done."