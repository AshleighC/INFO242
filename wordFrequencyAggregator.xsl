<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output method="html" version="4.0"
        encoding="iso-8859-1" indent="yes"/>
    <xsl:template match="/">
      <html>
          <head>
                
          </head>
        <body>
        <h2>5 Most Commonly Used Words</h2>
        <ul>
            <xsl:for-each-group group-by="." select="
                for $w in //repository/description/tokenize(., '\W+') return $w">
                <xsl:sort select="count(current-group())" order="descending" />
                <xsl:if test="position() lt 6">
                    <li>
                        <xsl:value-of select="current-grouping-key()"/>
                        <xsl:text> - </xsl:text>
                        <xsl:value-of select="count(current-group())"/>
                    </li>
                </xsl:if>
            </xsl:for-each-group>
        </ul>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>