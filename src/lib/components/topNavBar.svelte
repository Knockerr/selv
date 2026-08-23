<script>
  import { pathDb } from "$lib/icons/pathDb";
  import Button from "./bits-ui/baseComponents/Button.svelte";
  import ProfilePicture from "./bits-ui/baseComponents/ProfilePicture.svelte";
</script>

<div class="container">
  <div class="topBar">
    <div class="leftSide">
      <select name="profil" id="profil-input" class="profilSelector" disabled>
        <option value="Pierre">Profil de SOON</option>
        <option value="Jean">Profil de Jean</option>
      </select>
    </div>
    <div class="rightSide">
      <div class="rightSideButtons">
        <Button iconPath="{pathDb.bug}," color="#ddd" height="40px">
          Signaler un bug
        </Button>
        <Button iconPath="{pathDb.share}," color="#ddd" height="40px">
          Partager le logiciel
        </Button>
        <Button iconPath="{pathDb.git}," color="#ddd" height="40px">
          Code source
        </Button>
      </div>
      <ProfilePicture size="40px" button />
    </div>
  </div>
</div>

<style>
  .container {
    background-color: #030712;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .topBar {
    height: 50px;
    margin: 20px;
    margin-top: 10px;
    justify-content: right;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border-bottom: #1f2937 1.5px solid;
    height: 60px;
    padding: 5px 0;
    align-items: center;
  }

  .leftSide,
  .rightSide {
    display: flex;
    align-items: center;
    flex-direction: row;
    gap: 30px;
  }

  .leftSide select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    /**/
    box-sizing: border-box;
    width: 180px;
    height: 38px;
    line-height: 38px;

    padding: 0 12px;

    /* */
    background-color: #030712;
    border: 1px solid #1f2937;
    border-radius: 7px;
    color: white;
    font-family: "Open Sans", sans-serif;
    font-size: 14px;
  }

  .leftSide option {
    /* */
    background-color: transparent;
    border-radius: 7px;
    color: white;
    font-family: "Open Sans", sans-serif;
    font-size: 14px;
  }

  .rightSide{
    margin-right: 20px;
  }

  .rightSideButtons {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
</style>
