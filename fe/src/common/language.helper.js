export const LANGUAGES = {
    'ru': {
        langCode: "ru",
        name: "Russian",
        icon: "⚽️"
    },
    'en': {
        langCode: "en",
        name: "English",
        icon: "🧸"
    },
    // 'ba': {
    //     langCode: "ba",
    //     name: "Bashkir",
    //     icon: "🌹"
    // },
    'de': {
        langCode: "de",
        name: "German",
        icon: "🍺"
    },
    'fr': {
        langCode: "fr",
        name: "French",
        icon: "🥖"
    },
    'it': {
        langCode: "it",
        name: "Italian",
        icon: "🍕"
    },
    'es': {
        langCode: "es",
        name: "Spanish",
        icon: "🍅"
    },
    'pt': {
        langCode: "pt",
        name: "Portugal",
        icon: "🍊"
    },
    'tr': {
        langCode: "tr",
        name: "Turkish",
        icon: "☕️"
    },
    'cz': {
        langCode: "cz",
        name: "Czech",
        icon: "🍺"
    },
    'pl': {
        langCode: "pl",
        name: "Polish",
        icon: "🍬"
    },
    'uk': {
        langCode: "uk",
        name: "Ukrainian",
        icon: "🌻"
    },
    'hu': {
        langCode: "hu",
        name: "Hungarian",
        icon: "🎄"
    },
    'nl': {
        langCode: "nl",
        name: "Dutch",
        icon: "🌈"
    },
    'sw': {
        langCode: "sw",
        name: "Sweden",
        icon: "⛄️"
    },
    'ko': {
        langCode: "ko",
        name: "Korean",
        icon: "🐕"
    },
    'zh': {
        langCode: "zh",
        name: "Chinese",
        icon: "🥢",
        noSpaceBetweenSentences: true
    },
    'jp': {
        langCode: "jp",
        name: "Japanese",
        icon: "🍣",
        noSpaceBetweenSentences: true
    },
};
export const DEFAULT_FROM = 'en';
export const DEFAULT_TO = 'ru';

export const LanguageHelper = {
    initItems() {
        let res = {}
        Object.keys(LANGUAGES).forEach(x => {
            res[x] = [];
        })
        return res;
    },
    initSplitted() {
        let res = {}
        Object.keys(LANGUAGES).forEach(x => {
            res[x] = {
                lines: [],
                meta: {}
            };
        })
        return res;
    },
    initMarks() {
        let res = {}
        Object.keys(LANGUAGES).forEach(x => {
            res[x] = [];
        })
        return res;
    },
    initProcessing() {
        return {
            items: [],
            meta: {}
        }
    },
    initGeneralVars() {
        let res = {}
        Object.keys(LANGUAGES).forEach(x => {
            res[x] = null;
        })
        return res;
    },
    initGeneralBools() {
        let res = {}
        Object.keys(LANGUAGES).forEach(x => {
            res[x] = false;
        })
        return res;
    }
}
