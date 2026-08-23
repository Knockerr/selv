<script>
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount } from "svelte";

  const { size } = $props();

  let profilePicture = $state("");

  onMount(async () => {
    const { data, error } = await supabase.auth.getUser();
    if (error) return;
    profilePicture = data.user.user_metadata.profilePicture;
  });
</script>

<img
  src={profilePicture}
  style:width={size}
  style:height={size}
  class="pp"
  alt="Your profile"
/>

<style>
  img {
    object-fit: cover;
    border-radius: 50%;
  }
</style>
