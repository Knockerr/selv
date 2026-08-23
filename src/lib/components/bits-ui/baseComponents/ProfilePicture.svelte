<script>
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount } from "svelte";
  import Dropdown from "./Dropdown.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { goto } from "$app/navigation";

  const { size, button = false } = $props();

  let profilePicture = $state("");
  let items = [
    {
      icon: pathDb.user,
      label: "Mon compte",
      type: "item",
      onclick: () => {
        goto("/core/settings/account");
      },
    },
    {
      icon: pathDb.gears,
      label: "Paramètre",
      type: "item",
      onclick: () => {
        goto("/core/settings/account");
      },
    },
    {
      type: "separator",
    },
    {
      icon: pathDb.logout,
      label: "Déconnexion",
      type: "item",
    },
  ];

  onMount(async () => {
    const { data, error } = await supabase.auth.getUser();
    if (error) return;
    profilePicture = data.user.user_metadata.profilePicture;
  });
</script>

{#if button}
  <Dropdown {items}>
    {#snippet triggerSnippet()}
      <img
        src={profilePicture}
        style:width={size}
        style:height={size}
        class:button
        class="pp"
        alt="Your profile"
      />
    {/snippet}
  </Dropdown>
{:else}
  <img
    src={profilePicture}
    style:width={size}
    style:height={size}
    class="pp"
    alt="Your profile"
  />
{/if}

<style>
  img {
    object-fit: cover;
    border-radius: 50%;
  }

  img.button:hover {
    cursor: pointer;
  }
</style>
