<script>
  import CoreSettingsSidebar from "$lib/components/core/settings/coreSettingsSidebar.svelte";

  const { children } = $props();
</script>

<div class="page">
  <h1 class="titleBar">Paramètres</h1>
  <div class="content">
    <CoreSettingsSidebar />
    <div class="childContainer">
      <div class="child">
        {@render children?.()}
      </div>
    </div>
  </div>
</div>

<style>
  .page {
    display: flex;
    flex-direction: column;
    height: 95%;
    margin: 20px 65px;
    padding: 30px 40px;
    box-sizing: border-box;
    overflow-y: scroll;
  }

  .titleBar {
    background-color: var(--mainBackgroundColor);
    margin: 0;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    color: white;
    font-family: "Roboto", sans-serif;
    font-optical-sizing: auto;
    font-weight: 600;
    font-size: 2.5rem;
    margin-bottom: 30px;
    font-style: normal;
    justify-self: flex-start;
  }

  .content {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 70px;
    flex: 1;
  }

  .childContainer {
    height: 100%;
    flex: 1;
    display: flex;
    flex-direction: row;
    justify-content: center;
  }

  .child{
    width: 85%;
    height: 500%;
  }
</style>
