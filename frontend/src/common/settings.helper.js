import {
    DEFAULT_FROM,
    DEFAULT_TO
} from "@/common/language.helper";

export const SettingsHelper = {
    getShowProxyTo() {
        if (localStorage.showProxyTo && localStorage.showProxyTo == "true") {
            return true;
        } else {
            return false;
        }
    },
    getShowAllTo() {
        return localStorage.showAllTo ? localStorage.showAllTo : defaultClientSettings.showAllTo;
    },
    getShowAllFrom() {
        return localStorage.showAllFrom ? localStorage.showAllFrom : defaultClientSettings.showAllFrom;
    },
    getSplittedPanelPageCount() {
        return localStorage.splittedPanelPageCount ? localStorage.splittedPanelPageCount : defaultClientSettings.splittedPanelPageCount;
    },
    setSplittedPanelPageCount(value) {
        localStorage.splittedPanelPageCount = value;
    },
    getIsMarksInRow() {
        return localStorage.isMarksInRow ? localStorage.isMarksInRow : defaultClientSettings.isMarksInRow;
    },
    getUseAdditionalPreprocessingFrom() {
        if (localStorage.useAdditionalPreprocessingFrom && localStorage.useAdditionalPreprocessingFrom == "true") {
            return true;
        } else {
            return false;
        }
    },
    getUseAdditionalPreprocessingTo() {
        if (localStorage.useAdditionalPreprocessingTo && localStorage.useAdditionalPreprocessingTo == "true") {
            return true;
        } else {
            return false;
        }
    },
    getLastLanguageFrom() {
        return localStorage.lastLanguageFrom ? localStorage.lastLanguageFrom : defaultClientSettings.lastLanguageFrom;
    },
    getLastLanguageTo() {
        return localStorage.lastLanguageTo ? localStorage.lastLanguageTo : defaultClientSettings.lastLanguageTo;
    },
    setLastLanguageFrom(value) {
        localStorage.lastLanguageFrom = value;
    },
    setLastLanguageTo(value) {
        localStorage.lastLanguageTo = value;
    }
}

export const CANDIDATES_SORTING_NEAREST = 'nearest'
export const CANDIDATES_SORTING_SIMILAR = 'similar'

const defaultClientSettings = {
    showProxyTo: true,
    showAllTo: false,
    showAllFrom: false,
    candidatesSorting: CANDIDATES_SORTING_NEAREST,
    splittedPanelPageCount: 20,
    isMarksInRow: false,
    useAdditionalPreprocessingFrom: true,
    useAdditionalPreprocessingTo: true,
    lastLanguageFrom: DEFAULT_FROM,
    lastLanguageTo: DEFAULT_TO
}