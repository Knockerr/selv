<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { onMount } from "svelte";
  import GridElem from "./gridElem.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { goto } from "$app/navigation";
  import ProfilePicture from "$lib/components/bits-ui/baseComponents/ProfilePicture.svelte";

  let userPicture = $state("");
  let username = $state("");
  let userMail = $state("");

  onMount(async () => {
    const { data, error } = await supabase.auth.getUser();
    if (error) return;
    username = data.user.user_metadata.username || "";
    userPicture = data.user.user_metadata.profilePicture;
    userMail = data.user.email;
  });
</script>

<GridElem>
  <div class="card">
    <ProfilePicture size="70px" />
    <div class="name">{username}</div>
    <div class="mail">{userMail}</div>
    <Button
      iconPath={pathDb.arrowRight}
      emphasize
      className="mt-2"
      onclick={() => goto("/core/settings/account")}>Mon compte</Button
    >
  </div>
</GridElem>

<style>
  .card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    gap: 10px;
  }

  .mail {
    font-size: 1rem;
  }
</style>
