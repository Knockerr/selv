<script>
  import Window from "../../Window.svelte";
  import WindowAligned from "../../WindowAligned.svelte";
  import WindowButton from "../../WindowButton.svelte";
  import WindowLabel from "../../WindowLabel.svelte";
  import { windowsManager } from "../../windowsManager.svelte";

  const { serverUuid } = $props();

  let windowId = $derived("MinecraftEula-" + serverUuid);

  function acceptEula() {
    fetch("http://localhost:8000/api/servers/" + serverUuid + "/acceptEula", {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => console.log("data -> ", data))
      .catch((error) => console.error(error));
    windowsManager.close(windowId);
  }

  function cancelEula() {
    windowsManager.close(windowId);
  }

  const isOpen = $derived(windowsManager.openWindows.has(windowId));
</script>

{#if isOpen}
  <Window height="20%" width="25%" title={"EULA"} windowId={"windowId"}>
    <WindowLabel>
      En cliquant sur "Accepter", vous confirmez accepter l'<a
        href="https://account.mojang.com/documents/minecraft_eula">EULA</a
      >.
    </WindowLabel>
    <WindowAligned>
      <WindowButton onclick={acceptEula}>Accepter</WindowButton>
      <WindowButton onclick={cancelEula}>Annuler</WindowButton>
    </WindowAligned>
  </Window>
{/if}
