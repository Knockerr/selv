<script>
  import { pathDb } from "$lib/icons/pathDb";
  import Icon from "../Icon.svelte";

  const { tabName, tabIconPath, onclick } = $props();
</script>

<button class="component" onclick={async () => await onclick()}>
  <h1 id="tabName">{tabName}</h1>
  <Icon path={tabIconPath} size={"27"} />
</button>

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0;
    padding-left: 15px;
    padding-right: 15px;
    height: 55px;
    gap: 15px;
    border: 0;
    border-radius: 15px;
    background-color: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.08);
    width: 95%;
    box-sizing: border-box;
    color: #ddd;
    border-radius: 12px;
    transition: background-color 0.3s ease;
  }

  .component:hover {
    background-color: rgba(255, 255, 255, 0.08);
  }

  .component:active {
    transition: all 0s ease;
    background-color: rgba(255, 255, 255, 0.1);
  }

  button:hover {
    cursor: pointer;
  }

  #tabName {
    font-size: 1.4rem;
    font-weight: 600;
  }
</style>
