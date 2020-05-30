/// Unpersisted object used to serialize to JSON a resource along with its tags
Class Tagit.FullResource Extends (%RegisteredObject, %JSON.Adaptor)
{

Property uri As %Library.String;

Property title As %Library.String;

Property type As %Library.String;

Property views As %Library.Integer;

Property tags As list Of Tagit.Tag;

// Property tags As list Of %Library.String;

Method LoadFullResource(resourceId As %Integer) As %Status
{
    try {
        do ..LoadResource(resourceId)

        set sqlst = ##class(%SQL.Statement).%New()
        do sqlst.prepare("SELECT tagid FROM Tagit.TagMap WHERE resourceid = :resourceId")
        set result = sqlst.execute()
        while result.%Next(.sc)
        {
            write !,"HERE"
            set tagid = result.%Get("tagid")
            write !,"tagid: "_tagid
            do ..LoadTag(tagid)
        }
        if result.SQLCODE<0 {
            write "SQLCODE: "_result.SQLCODE
            throw ##class(%Exception.SQL).CreateFromSQLCODE(result.%SQLCODE, result.%Message)
        }
    } catch (oException) {
        write !,"EXCEPTION: "_oException
        throw oException
    }
}

Method LoadResource(resid As %Integer) As %Status
{
    set res = ##class(Tagit.Resource).%OpenId(resid)
    set ..uri = res.uri
    set ..title = res.title
    set ..type = res.type
    set ..views = res.views
}

Method LoadTag(tagid As %Integer) As %Status
{
    set tag = ##class(Tagit.Tag).%OpenId(tagid)
    do ..tags.Insert(tag)
    write !,"tag count: "_..tags.Count()
}

}
