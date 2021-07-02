def crossref_mime_type(jats_mime_type):
    """
    Dictionary of lower case JATS mime type to crossRef schema mime type
    """
    mime_types = {}

    mime_types["application/eps"] = "application/eps"
    mime_types["application/gz"] = "application/gzip"
    mime_types["application/tar.gz"] = "application/gzip"
    mime_types["application/doc"] = "application/msword"
    mime_types["application/pdf"] = "application/pdf"
    mime_types["application/rtf"] = "application/rtf"
    mime_types["application/xls"] = "application/vnd.ms-excel"
    mime_types[
        "application/pptx"
    ] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    mime_types[
        "application/xlsx"
    ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    mime_types[
        "application/docx"
    ] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    mime_types["application/xml"] = "application/xml"

    mime_types["chemical/pdb"] = "chemical/x-pdb"

    mime_types["image/tif"] = "image/tiff"
    mime_types["image/tiff"] = "image/tiff"
    mime_types["application/png"] = "image/png"

    mime_types["text/plain"] = "text/plain"
    mime_types["application/csv"] = "text/plain"
    mime_types["application/txt"] = "text/plain"
    mime_types["text/pl"] = "text/plain"
    mime_types["text/py"] = "text/plain"
    mime_types["text/txt"] = "text/plain"
    mime_types["text/rtf"] = "text/rtf"

    mime_types["video/avi"] = "video/avi"
    mime_types["video/mp4"] = "video/mp4"
    mime_types["video/mpeg"] = "video/mpeg"
    mime_types["video/mpg"] = "video/mpeg"
    mime_types["video/mov"] = "video/quicktime"
    mime_types["video/wmv"] = "video/x-ms-wmv"
    mime_types["video/gif"] = "image/gif"

    return mime_types.get(jats_mime_type.lower())
