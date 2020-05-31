/// Unpersisted object used to serialize to JSON a resource along with its tags
Class Tagit.FullResource Extends (%RegisteredObject, %JSON.Adaptor)
{

Property uri As %Library.String;

Property title As %Library.String;

Property type As %Library.String;

Property views As %Library.Integer;

Property tags As list Of Tagit.Tag;

// Property tags As list Of %Library.String;

Method LoadFullResource(resid As %Integer) As %Status
{
    try {
        do ..LoadResource(resid)

        set mq = "SELECT tagid FROM Tagit.TagMap WHERE resourceid = ?"
        set sqlst = ##class(%SQL.Statement).%New()
        set qStatus = sqlst.%Prepare(.mq)
            if qStatus'=1 {WRITE "%Prepare failed:" DO $System.Status.DisplayError(qStatus) QUIT}

        set result = sqlst.%Execute(resid)
        if result.SQLCODE<0 {
            write !,"SQLCODE: "_result.SQLCODE
            throw ##class(%Exception.SQL).CreateFromSQLCODE(result.%SQLCODE, result.%Message)
        }

        while result.%Next()
        {
            set tagid = result.%Get("tagid")
            do ..LoadTag(tagid)
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
}

}
