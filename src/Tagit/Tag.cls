/// 
Class Tagit.Tag Extends (%Persistent, %JSON.Adaptor) [ ClassType = persistent, DdlAllowed, Final, Owner = {_SYSTEM}, ProcedureBlock, Not SqlRowIdPrivate, SqlTableName = Tag ]
{

Property name As %Library.String(MAXLEN = 128) [ SqlColumnNumber = 2 ];

Property description As %Library.String(MAXLEN = 4096) [ SqlColumnNumber = 3 ];

Parameter USEEXTENTSET = 1;

/// Bitmap Extent Index auto-generated by DDL CREATE TABLE statement.  Do not edit the SqlName of this index.
Index DDLBEIndex [ Extent, SqlName = "%%DDLBEIndex", Type = bitmap ];

/// DDL Unique Key Specification
Index TAGSUNIQUE1 On name [ SqlName = TAGS_UNIQUE1, Unique ];

Storage Default
{
<Data name="TagDefaultData">
<Value name="1">
<Value>name</Value>
</Value>
<Value name="2">
<Value>description</Value>
</Value>
</Data>
<DataLocation>^i9v3.B5rU.1</DataLocation>
<DefaultData>TagDefaultData</DefaultData>
<ExtentLocation>^i9v3.B5rU</ExtentLocation>
<IdLocation>^i9v3.B5rU.1</IdLocation>
<Index name="DDLBEIndex">
<Location>^i9v3.B5rU.2</Location>
</Index>
<Index name="IDKEY">
<Location>^i9v3.B5rU.1</Location>
</Index>
<Index name="TAGSUNIQUE1">
<Location>^i9v3.B5rU.3</Location>
</Index>
<IndexLocation>^i9v3.B5rU.I</IndexLocation>
<StreamLocation>^i9v3.B5rU.S</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}