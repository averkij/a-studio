export const SettingsHelper = {
    getShowProxyTo() {
        return localStorage.showProxyTo ? localStorage.showProxyTo : defaultClientSettings.showProxyTo;
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
}

const defaultClientSettings = {
    showProxyTo: true,
    showAllTo: false,
    showAllFrom: false,
    candidatesSorting: CANDIDATES_SORTING_NEAREST,
    splittedPanelPageCount: 20,
    isMarksInRow: false
}

export const CANDIDATES_SORTING_NEAREST = 'nearest'
export const CANDIDATES_SORTING_SIMILAR = 'similar'
