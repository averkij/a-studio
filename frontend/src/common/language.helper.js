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
    'hy': {
        langCode: "hy",
        name: "Armenian",
        icon: "🍷"
    },
    'ba': {
        langCode: "ba",
        name: "Bashkir",
        icon: "🌹"
    },
    'cv': {
        langCode: "cv",
        name: "Chuvash",
        icon: "🌞"
    },
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
    'bu': {
        langCode: "bu",
        name: "Belorussian",
        icon: "🌼"
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
    'xx': {
        langCode: "xx",
        name: "General",
        icon: "👽"
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
        let res = {
            'left': {},
            'right': {}
        }
        Object.keys(LANGUAGES).forEach(x => {
            res['left'][x] = {
                lines: [],
                meta: {}
            };
            res['right'][x] = {
                lines: [],
                meta: {}
            };
        })
        return res;
    },
    initMarks() {
        let res = {
            'left': {},
            'right': {}
        }
        Object.keys(LANGUAGES).forEach(x => {
            res['left'][x] = [];
            res['right'][x] = [];
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
    initGeneralVars2Sides() {
        let res = {
            'left': {},
            'right': {}
        }
        Object.keys(LANGUAGES).forEach(x => {
            res['left'][x] = null;
            res['right'][x] = null;
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