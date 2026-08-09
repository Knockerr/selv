<script>
  // TODO : remove compo

  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";

  const { login = true } = $props();
  let email = $state();
  let password = $state();
  let visible = $state(false);

  onMount(() => {
    visible = true;
    goto("/core/dashboard");
  });
</script>

{#if visible}
  <div class="component" transition:fly={{ y: 30, duration: 750 }}>
    {#if login}
      <h2>Connexion</h2>
    {/if}

    <div class="inputContainer">
      <input type="text" bind:value={email} placeholder="Email" />
      <input type="password" bind:value={password} placeholder="Password" />
    </div>
    <button id="logInButton" onclick={() => goto("/core/serverList")}>
      Se connecter
    </button>
  </div>
{/if}

<style>
  .component {
    height: 45%;
    width: 20%;
    background-color: rgb(52, 58, 77);
    border: 2px solid rgb(97, 97, 97);
    border-radius: 30px;
    box-shadow: 0 0 5px rgba(128, 128, 128, 0.363);
    padding: 5px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: Arial, Helvetica, sans-serif;
    gap: 20px;
    color: #ddd;
  }

  .inputContainer {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }

  input {
    padding: 10px;
    outline: none;
    border: 0.5px #858586 solid;
    background-color: rgb(31, 31, 104);
    color: white;
    border-radius: 10px;
    box-shadow: 0 0 5px #8585867a;
  }

  #logInButton {
    padding: 10px;
    outline: none;
    border: none;
    background: rgb(31, 31, 104);
    color: white;
    font-size: 0.9rem;
    text-decoration: none;
    cursor: crosshair;
  }
</style>
