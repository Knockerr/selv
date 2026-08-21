<script>
  import { goto } from "$app/navigation";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import {
    startServer,
    stopServer,
  } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { onMount } from "svelte";

  const { uuid = "" } = $props();

  let name = $state("");

  onMount(() => {
    fetch(`http://127.0.0.1:8000/api/servers/${uuid}/serverListDatas`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        name = data.name ?? "";
      })
      .catch((err) => console.error("fetch error:", err));
  });
</script>

<button
  class="component"
  onclick={() => {
    goto("/panel/console?uuid=" + uuid);
  }}
>
  <div class="left">
    <Icon path={pathDb.folder} size="23" />
    <span>
      {name}
    </span>
  </div>
  <div class="right">
    <IconButton
      iconPath={pathDb.playCircle}
      color="#79c"
      onclick={(e) => {
        e.stopPropagation();
        startServer(uuid);
      }}
    />
    <IconButton
      iconPath={pathDb.stopCircle}
      color="#d55"
      onclick={(e) => {
        e.stopPropagation();
        stopServer(uuid);
      }}
    />
    <IconButton
      iconPath={pathDb.console}
      color="#ccc"
      onclick={() => {
        e.stopPropagation();
        goto("/panel/console?uuid=" + uuid);
      }}
    />
  </div>
</button>

<style>
  .component {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: white;
    font-family: "Open Sans", sans-serif;
    width: 90%;
    height: 43px;
    font-size: 14px;
    padding: 8px 16px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .component:hover {
    background-color: rgba(255, 255, 255, 0.14);
  }

  .left,
  .right {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
  }

  .left {
    flex: 1;
  }

  .right {
    gap: 0;
    width: fit-content;
  }

  span {
    font-family: var(--robotoFont);
    font-weight: 400;
    font-size: 1rem;
    width: 100%;
    max-width: 100%;
    text-align: left;
  }
</style>
