export const Helper = {
    trim(str){ 
        return ( str || '' ).replace( /^\s+|\s+$/g, '' ); 
    }
}

export const BOOK_STYLES = ["simple", "pastel_fill", "pastel_start"]
// export const MARK_NAMES = ["H1", "H2", "H3", "H4", "H5", "Image", "Divider", "Quote"]
export const MARK_NAMES = [
    {name:"Image", type:"image"},
    {name:"Divider", type:"divider"},
    // {name:"H1", type:"h1"},
    // {name:"H2", type:"h2"},
    // {name:"H3", type:"h3"},
    // {name:"H4", type:"h4"},
    // {name:"H5", type:"h5"},
    {name:"Quote", type:"qtext"},
    {name:"Quote author", type:"qname"},
]
