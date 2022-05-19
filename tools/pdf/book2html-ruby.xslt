<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="html" indent="yes" xslt:indent-amount="2" xmlns:xslt="http://xml.apache.org/xalan" />

	<!-- number of colors to rotate for sentences -->
	<xsl:variable name="gNumColors">4</xsl:variable>

	<!-- main  -->
	<xsl:template match="/book">
		<html>
		<title>Lingtrain Magic Book -
			<xsl:value-of select="head/title/s" separator=" / " />
		</title>

		<head>
			<meta charset="utf-8" />
		</head>
		<section class="fullpage">
			<img src="$COVER_IMG" />
		</section>

		<section class="title">
			<p class="book-title">
				<xsl:value-of select="head/title/s[1]" />
			</p>
			<p class="book-author">
				<xsl:value-of select="head/author/s[1]" />
			</p>
		</section>

		<section class="title">
			<p class="book-title">
				<xsl:value-of select="head/title/s[2]" />
			</p>
			<p class="book-author">
				<xsl:value-of select="head/author/s[2]" />
			</p>
		</section>

		<section id="authors">
			<img class="logo" src="https://hsto.org/webt/q9/1t/cy/q91tcypgjnrrsmrfcviyzzdvfsk.png" />
			<p>
				Lingtrain Books
			</p>
		</section>

		<xsl:if test="/book/body/section[@type='h2']">
			<section class="contents">
				<p>
					<xsl:value-of select="head/contents/s[1]" />
				</p>
				<ul>
					<xsl:for-each select="/book/body/section[@type='h2']">
						<li>
							<a>
								<xsl:attribute name="href" select="concat('#part-', position(), '-h2')" />
							</a>
						</li>
					</xsl:for-each>
				</ul>
			</section>

			<section class="contents">
				<p>
					<xsl:value-of select="head/contents/s[2]" />
				</p>
				<ul>
					<xsl:for-each select="/book/body/section[@type='h2']">
						<li>
							<a>
								<xsl:attribute name="href" select="concat('#hpart-', position(), '-h2')" />
							</a>
						</li>
					</xsl:for-each>
				</ul>
			</section>
		</xsl:if>

		<xsl:apply-templates select="body/section" />

		</html>
	</xsl:template>

	<!-- Section -->
	<xsl:template match="section[@type='h2'] | section[@type='default']">
		<xsl:variable name="sect" select="." />
		<xsl:variable name="section_id">
			<xsl:number count="section" />
		</xsl:variable>
		<section class="part">
			<!-- <xsl:attribute name="class"><xsl:text>part</xsl:text></xsl:attribute> -->
			<xsl:attribute name="id">
				<xsl:value-of select="$section_id" />
			</xsl:attribute>

			<h2>
				<xsl:attribute name="id" select="concat('part-', $section_id, '-h2')" />
				<xsl:value-of select="$sect/header/su[1]" />
			</h2>
			<div class="sub-h2">
				<xsl:attribute name="id" select="concat('hpart-', $section_id, '-h2')" />
				<xsl:value-of select="$sect/header/su[2]" />
			</div>

			<xsl:apply-templates select="$sect/p" />
		</section>
	</xsl:template>

	<!-- Generic paragraph -->
	<xsl:template match="p[@type='text']">
		<xsl:variable name="p" select="." />
		<div class='dt-row'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )" />

					<!-- <div class='book-par-id' aria-hidden='true'> -->
					<!-- <xsl:value-of select="$p/@id"/> -->
					<!-- </div> -->
					<xsl:apply-templates select="$p/sentence/su[@lang = current()]" />
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- Sentence inside the paragraph cell -->
	<xsl:template match="su">
		<!-- I don't know how it works, really -->
		<xsl:variable name="scount">
			<xsl:number count="sentence" />
		</xsl:variable>
		<xsl:variable name="highlight">s
			<xsl:value-of select="(($scount - 1) mod $gNumColors)" />
		</xsl:variable>
		<xsl:value-of select="." />
		<xsl:text> </xsl:text>
	</xsl:template>
	
	<!-- Header -->
	<xsl:template match="p[matches(@type,'h\d')]">
		<xsl:variable name="level">
			<xsl:value-of select="@type" />
		</xsl:variable>
		<xsl:variable name="p" select="." />
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )" />
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<xsl:element name="{$level}">
						<!-- No alignment on headers.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]" />
					</xsl:element>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- Image -->
	<xsl:template match="p[@type='image']">
		<xsl:variable name="p" select="." />
		<div class='dt-row header' aria-hidden="true">
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell text-center',' dt-w', position() )" />
					<img class='lt-image'>
					<xsl:attribute name="src">
						<xsl:value-of select="normalize-space($p/sentence/su[@lang = current()])" />
					</xsl:attribute>
					</img>
				</div>
			</xsl:for-each>
		</div>

	</xsl:template>

	<!-- QText -->
	<xsl:template match="p[matches(@type,'qtext')]">
		<xsl:variable name="p" select="." />
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )" />
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<div class="lt-quote lt-quote-text">
						<!-- No alignment on quote.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]" />
					</div>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

	<!-- QName -->
	<xsl:template match="p[matches(@type,'qname')]">
		<xsl:variable name="p" select="." />
		<div class='dt-row header'>
			<xsl:for-each select="/book/head/langs/lang/@id">
				<div>
					<xsl:attribute name="class" select="concat('par dt-cell',' dt-w', position() )" />
					<xsl:if test="position() = 2">
						<xsl:attribute name="aria-hidden">true</xsl:attribute>
					</xsl:if>
					<div class="lt-quote lt-quote-name">
						<!-- No alignment on quote.... -->
						<xsl:value-of select="$p/sentence/su[@lang = current()]" />
					</div>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>

</xsl:stylesheet>