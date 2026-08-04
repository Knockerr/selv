function createSidebarsStore() {
    let currentTabsState = $state({
        main: "Servers",
        panel: "console"
    })

    return {
        setCurrentTab(sidebar, tab) {
            currentTabsState[sidebar] = tab;
        },
        currentTab(sidebar) {
            return currentTabsState[sidebar]
        }
    }
}

export const sidebarStore = createSidebarsStore()