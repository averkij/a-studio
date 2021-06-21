export const Helper = {
    trim(str){ 
        return ( str || '' ).replace( /^\s+|\s+$/g, '' ); 
    }
}

export const BOOK_STYLES = ["simple", "pastel_fill", "pastel_start"]