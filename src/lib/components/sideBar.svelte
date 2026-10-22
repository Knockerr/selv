<script>
  import SideBarButton from "$lib/components/sideBarButton.svelte";
  import { pathDb } from "$lib/icons/pathDb.js";
  import logoProvisoire from "$lib/assets/logo-provisoire.png";
  import { openUrl } from "@tauri-apps/plugin-opener";
</script>

<div class="container">
  <img src={logoProvisoire} alt="LOGO" id="logo" />

  <ul id="topOptions">
    <SideBarButton
      href="/core/dashboard"
      title="Dashboard"
      path={pathDb.treeStructure}
      classes="topOptions"
      id="dashboard"
      num="0"
    />

    <SideBarButton
      href="/core/serverList"
      title="Servers"
      path={pathDb.hardDrives}
      classes="topOptions"
      id="servers"
      num="1"
    />

    <SideBarButton
      href="/core/settings/account"
      title="Paramètres"
      path={pathDb.wrench}
      classes="topOptions"
      id="parameters"
      num="2"
    />

    <!--
		<SideBarButton
			href="TODO"
			title="Extensions"
			path={pathDb.puzzlePiece}
			classes="topOptions"
			id="parameters"
			num=3
		/>
-->
  </ul>

  <ul id="bottomOptions">
    <SideBarButton
      title="Support"
      onclick={() => {
        openUrl("https://discord.selvmc.com");
      }}
      path={pathDb.question}
      classes="bottomOptions"
      id="help"
      num="3"
      noSelect
    />

    <SideBarButton
      title="Site"
      onclick={() => {
        openUrl("https://selvmc.com");
      }}
      path={pathDb.web}
      classes="bottomOptions"
      id="doc"
      num="4"
      noSelect
    />
  </ul>
</div>

<style>
  #logo {
    padding: 0;
    height: auto;
    width: 40px;
    margin-top: 10px;
  }

  .container {
    background-color: #111825;
    border-right: #1f2937 1px solid;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    width: 90px;
  }

  /* .container a.selected {
		background-color: #1f2937;
		color: #674dbd;
	} */

  #topOptions {
    list-style-type: none;
    padding: 0;
    background-color: #111825;
  }

  #bottomOptions {
    list-style-type: none;
    padding: 0;
    position: absolute;
    bottom: 0;
  }
</style>
