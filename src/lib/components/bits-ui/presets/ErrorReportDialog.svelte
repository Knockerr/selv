<script>
  import { onMount } from "svelte";
  import Button from "../baseComponents/Button.svelte";
  import Dialog from "../baseComponents/dialog.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";
  import { appLocalDataDir, join, localDataDir } from "@tauri-apps/api/path";
  import { readTextFile, writeFile } from "@tauri-apps/plugin-fs";
  import { save } from "@tauri-apps/plugin-dialog";
  import JSZip from "jszip";

  const error = $derived(uiStore.currentError);

  let logDir;
  let logPath;

  onMount(async () => {
    const baseDir = await localDataDir();
    logDir = await join(baseDir, "Knocker", "mcPanel-DEV", "logs", "frontend");
    logPath = await join(logDir, "frontend.log");
  });

  async function getReport() {
    const zip = new JSZip();

    const content = await readTextFile(logPath);
    zip.file(`frontend/frontend.log`, content);

    const backendLogsResponse = await fetch(
      "http://localhost:8000/logs/download",
    );
    const backendLogsBlob = await backendLogsResponse.blob();
    const backendLogsBuffer = new Uint8Array(
      await backendLogsBlob.arrayBuffer(),
    );
    zip.file("backend/backend.log", backendLogsBuffer);

    const zipContent = await zip.generateAsync({ type: "uint8array" });

    return zipContent;
  }

  async function downloadReport() {
    const zipContent = await getReport();

    const savePath = await save({
      defaultPath: `mcpanel_logs_${Date.now()}.zip`,
      filters: [{ name: "Zip", extensions: ["zip"] }],
    });

    if (savePath) {
      await writeFile(savePath, zipContent);
    }
  }

  async function sendReport() {
    // TODO
    alert("Bientot disponible. Contacter le support par discord.");
  }
</script>

<Dialog
  title="Rapport d'erreur"
  description="Nous avons rencontré une erreur inattendue. Nous nous excusons pour ce désagrément. Contactez le support ou envoyez un rapport d'erreur"
  name="errorReportDialog"
>
  <div class="codeFieldContainer">
    <span class="codeFieldTitle"> Erreur: </span>
    <code>
      {error}
    </code>
  </div>
  <div class="buttonsContainer">
    <h3>Rapport d'erreur:</h3>
    <div class="optionsContainer">
      <Button onclick={downloadReport}>Télécharger</Button>
      <Button onclick={sendReport}>Envoyer</Button>
    </div>
    <div class="closeButtonContainer">
      <Button onclick={() => uiStore.closeDialog("errorReportDialog")} emphasize
        >Fermer</Button
      >
    </div>
  </div>
</Dialog>

<style>
  h3 {
    margin: 0;
    margin-bottom: 10px;
  }

  .codeFieldContainer{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .codeFieldTitle {
    margin: 0;
    font-size: 1rem;
    color: var(--color-foreground);
  }

  code {
    display: block;
    background-color: #111;
    width: 100%;
    height: 100px;
    box-sizing: border-box;
    padding: 7px;
    overflow: hidden;
    margin: 0;
  }

  .optionsContainer {
    display: flex;
    flex-direction: row;
    gap: 5px;
  }

  .closeButtonContainer {
    margin-top: 10px;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: end;
  }
</style>
