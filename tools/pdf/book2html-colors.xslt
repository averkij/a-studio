<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="html" indent="yes"
              xslt:indent-amount="2" xmlns:xslt="http://xml.apache.org/xalan" />
	
	<!-- number of colors to rotate for sentences -->
	<xsl:variable name="gNumColors">4</xsl:variable>

	<!-- main  -->
	<xsl:template match="/book">
	<html>
	<title>Lingtrain Magic Book - <xsl:value-of select="head/title/s" separator=" / "/></title>
	<head>
		<meta charset="utf-8" />
	</head>
	<section class="fullpage">
	  <img src="../img/cover.jpg" />
	</section>
	
<section class="title">
  <p class="book-title"><xsl:value-of select="head/title/s[1]"/></p>
  <p class="book-author"><xsl:value-of select="head/author/s[1]"/></p>
</section>

<section class="title">
  <p class="book-title"><xsl:value-of select="head/title/s[2]"/></p>
  <p class="book-author"><xsl:value-of select="head/author/s[2]"/></p>
</section>

<section id="authors">
  <img class="logo" src="https://hsto.org/webt/q9/1t/cy/q91tcypgjnrrsmrfcviyzzdvfsk.png" />
  <p>
    Lingtrain Books
  </p>
</section>

<!-- TODO Conditional contents generation -->

<!-- <section class="contents"> -->
  <!-- <p><xsl:value-of select="head/contents/s[1]"/></p> -->
  <!-- <ul> -->
    <!-- <li><a href="#part-1-h2"></a></li> -->
  <!-- </ul> -->
<!-- </section> -->

		<xsl:apply-templates select="body/p"/>

	</html>
	</xsl:template>

	<!-- Book header with some stats -->
	<xsl:template match="lang">
		<xsl:value-of select="sentences"/>sent. [<xsl:value-of select="@id"/>]<xsl:if test="position()!=last()"> • </xsl:if>
	</xsl:template>

	<!-- Title -->
	<xsl:template match="title">
		<xsl:variable name="current" select="."/>
		<div class='dt-row header title-cell'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('title-cell dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<h1 class='lt-title'>
						<xsl:value-of select="$current/s[@lang = current()]"/>
					</h1>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- Author -->
	<xsl:template match="author">
		<xsl:variable name="current" select="."/>
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('author-cell dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<h1 class='lt-author'>
						<xsl:value-of select="$current/s[@lang = current()]"/>
					</h1>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- Generic paragraph -->
	<xsl:template match="p[@type='text']">
		<xsl:variable name="p" select="."/>
		<div class='dt-row'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<!-- <div class='book-par-id' aria-hidden='true'> -->
						<!-- <xsl:value-of select="$p/@id"/> -->
					<!-- </div> -->
					<xsl:apply-templates select="$p/sentence/su[@lang = current()]"/>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>
	
	<!-- Sentence inside the paragraph cell -->
	<xsl:template match="su">
		<!-- I don't know how it works, really -->
		<xsl:variable name="scount">
			<xsl:number count="sentence"/>
		</xsl:variable>
		<xsl:variable name="highlight">s<xsl:value-of select="(($scount - 1) mod $gNumColors)"/></xsl:variable>
		<span>
			<xsl:attribute name="class">s <xsl:value-of select="$highlight"/></xsl:attribute>
			<xsl:value-of select="."/><xsl:text> </xsl:text> <!-- For some reason MS Edge's read-aloud ignores punctuation if it is directly followed by any closing tag -->
		</span>
	</xsl:template>
	
	<!-- Header -->
	<xsl:template match="p[matches(@type,'h\d')]">
		<xsl:variable name="level"><xsl:value-of select="@type"/></xsl:variable>
		<xsl:variable name="p" select="."/>
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<xsl:element name="{$level}">
						<!-- No alignment on headers.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]"/>
					</xsl:element>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>
	
	<!-- Image -->
	<xsl:template match="p[@type='image']">
		<xsl:variable name="p" select="."/>
		<div class='dt-row header' aria-hidden="true">
			<xsl:for-each select="/book/head/langs/lang/@id">
			<div>
				<xsl:attribute name="class" select="concat('par dt-cell text-center',' dt-w', position() )"/>
				<img class='lt-image'>
					<xsl:attribute name="src"><xsl:value-of select="normalize-space($p/sentence/su[@lang = current()])"/></xsl:attribute>
				</img>
			</div>
			</xsl:for-each>
		</div>

	</xsl:template>

	<!-- QText -->
	<xsl:template match="p[matches(@type,'qtext')]">
		<xsl:variable name="p" select="."/>
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<div class="lt-quote lt-quote-text">
						<!-- No alignment on quote.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]"/>
					</div>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- QName -->
	<xsl:template match="p[matches(@type,'qname')]">
		<xsl:variable name="p" select="."/>
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )"/>
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<div class="lt-quote lt-quote-name">
						<!-- No alignment on quote.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]"/>
					</div>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

</xsl:stylesheet>
