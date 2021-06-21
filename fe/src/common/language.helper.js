export const LANGUAGES = {
    'ru': {
        langCode: "ru",
        name: "Russian",
        icon: "⚽️"
    },
    'ba': {
        langCode: "ba",
        name: "Bashkir",
        icon: "🌹"
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
    'de': {
        langCode: "de",
        name: "German",
        icon: "🍺"
    },
    'en': {
        langCode: "en",
        name: "English",
        icon: "🧸"
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
    'tr': {
        langCode: "tr",
        name: "Turkish",
        icon: "☕️"
    },
    'pl': {
        langCode: "pl",
        name: "Polish",
        icon: "🍬"
    },
    'pt': {
        langCode: "pt",
        name: "Portugal",
        icon: "🍊"
    },
    'hu': {
        langCode: "hu",
        name: "Hungarian",
        icon: "🎄"
    },
    'cz': {
        langCode: "cz",
        name: "Czech",
        icon: "🍻"
    }
};
export const DEFAULT_FROM = 'ru';
export const DEFAULT_TO = 'zh';

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
            res[x] = {};
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
