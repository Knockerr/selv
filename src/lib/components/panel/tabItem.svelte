<script>
  import { pathDb } from "$lib/icons/pathDb";
  import Icon from "../Icon.svelte";

  const { tabName, tabIconPath, onclick } = $props();
</script>

<button class="component" onclick={async () => await onclick()}>
  <Icon path={tabIconPath} size={"35"} />
  <h1 id="tabName">{tabName}</h1>
</button>

<style>
  button:hover {
    cursor: pointer;
  }

  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0;
    padding-left: 15px;
    height: 55px;
    gap: 15px;
    border: 0;
    border-radius: 15px;
    background-color: rgba(255, 255, 255, 0.05);;
    width: 95%;
    box-sizing: border-box;
    color: #ddd;
    border-radius: 15px;
    transition: background-color 0.3s ease;
  }

  .component:hover {
    background-color: rgba(255, 255, 255, 0.151);
  }

  .component:active {
    background-color: rgba(255, 255, 255, 0.2);
  }

  #tabName {
    font-size: 1.4rem;
    font-weight: 600;
  }
</style>
