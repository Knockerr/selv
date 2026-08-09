function createUiComponentStore() {
    let store = $state({
        openDialogs: [],
        currentEditedFolder: "",
    });

    return {
        openDialog(dialogName) {
            store.openDialogs.push(dialogName);
            console.info("Opening dialog " + dialogName);
        },
        closeDialog(dialogName) {
            store.openDialogs.splice(store.openDialogs.indexOf(dialogName));
        },
        isDialogOpen(dialogName) {
            return store.openDialogs.includes(dialogName);
        },
        setCurrentEditedFolder(folderName) {
            store.currentEditedFolder = folderName;
        },
        get currentEditedFolder() {
            return store.currentEditedFolder;
        },
    }
}

export const uiStore = createUiComponentStore();