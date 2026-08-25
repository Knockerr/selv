function createUiComponentStore() {
    let store = $state({
        openDialogs: [],
        currentEditedFolder: "",
        currentUuid: "",
        loaderTitle: "",
        currentError: "",
    });

    return {
        openDialog(dialogName) {
            store.openDialogs.push(dialogName);
            console.info("Opening dialog " + dialogName);
        },
        closeDialog(dialogName) {
            const index = store.openDialogs.indexOf(dialogName);

            if (index !== -1) {
                store.openDialogs.splice(index, 1);
            }
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
        setCurrentUuid(uuid) {
            store.currentUuid = uuid;
        },
        get currentUuid() {
            return store.currentUuid;
        },
        load(title) {
            if (title) store.loaderTitle = title;
            store.openDialogs.push("loader");
        },
        stopLoad() {
            const index = store.openDialogs.indexOf("loader");

            if (index !== -1) {
                store.openDialogs.splice(index, 1);
            }
            store.loaderTitle = "";
        },
        get loaderTitle() {
            return store.loaderTitle;
        },
        reportError(error) {
            if (error) store.currentError = error;
            store.openDialogs.push("errorReportDialog");
        },
        get currentError() {
            return store.currentError;
        }
    }
}

export const uiStore = createUiComponentStore();