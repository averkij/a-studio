export const Helper = {
    trim(str) {
        return (str || '').replace(/^\s+|\s+$/g, '');
    },
    getMarksByType(type, marksFrom, marksTo) {
        let res = {
            from: marksFrom.filter(function (x) {
                return x[2] == type;
            }),
            to: marksTo.filter(function (x) {
                return x[2] == type;
            }),
        };
        return res;
    },
    mergeMarksGroup(marksGroup) {
        let res = [],
            lenFrom = 0,
            lenTo = 0;
        if (marksGroup["from"]) {
            lenFrom = marksGroup["from"].length;
        }
        if (marksGroup["to"]) {
            lenTo = marksGroup["to"].length;
        }
        let maxLen = Math.max(lenFrom, lenTo);
        for (let i = 0; i < maxLen; i++) {
            let a = {},
                b = {};
            if (marksGroup["from"].length >= i + 1) {
                a = marksGroup["from"][i];
            }
            if (marksGroup["to"].length >= i + 1) {
                b = marksGroup["to"][i];
            }
            res.push([a, b]);
        }
        return res;
    },
    mergeMarks(marksFrom, marksTo) {
        let res = [];
        MARK_NAMES.forEach(type => {
            let marksGroup = this.getMarksByType(type, marksFrom, marksTo);
            let merged = this.mergeMarksGroup(marksGroup);
            if (merged) {
                res.push(...merged)
            }
        });
        return res;
    },
}

export const TXT_EXTENSION = "txt"
export const CONVERT_EXTENSIONS = ["epub", "fb2", "rtf"]
export const SUPPORTED_EXTENSIONS = CONVERT_EXTENSIONS + [TXT_EXTENSION]

export const BOOK_STYLES = ["simple", "pastel_fill", "pastel_start"]
export const MARK_NAMES_DICT = [{
        name: "Image",
        type: "image"
    },
    {
        name: "Divider",
        type: "divider"
    },
    // {name:"H1", type:"h1"},
    // {name:"H2", type:"h2"},
    // {name:"H3", type:"h3"},
    // {name:"H4", type:"h4"},
    // {name:"H5", type:"h5"},
    {
        name: "Quote",
        type: "qtext"
    },
    {
        name: "Quote author",
        type: "qname"
    },
]

//for marks grouping, order is important here
export const MARK_NAMES = ["author", "title", "translator", "h1", "h2", "h3", "h4", "h5", "qname", "qtext", "image", "divider"]