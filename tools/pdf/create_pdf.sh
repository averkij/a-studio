#!/bin/bash
html="$1.html"

echo "Generating html file $html"

saxonb-xslt -s:$1 -xsl:$2 -o:$html

echo "Creating PDF $4"

weasyprint -s $3 $html $4

rm $html