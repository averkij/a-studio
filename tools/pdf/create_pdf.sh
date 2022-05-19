#!/bin/bash
html="$1.html"
img=$(echo "$4" | sed 's/\//\\\//g')

echo "Replacing image in xslt"

sed -e "s/\$COVER_IMG/$img/" $2 > _temp.xslt

echo "Generating html file $html"

saxonb-xslt -s:$1 -xsl:_temp.xslt -o:$html

echo "Creating PDF $5"

weasyprint -s $3 $html $5

echo "Removing temp files"

rm $html
rm _temp.xslt

echo "Done."