<script>
  import { fly } from "svelte/transition";
  import Button from "./Button.svelte";

  const {
    label,
    width,
    oncancel,
    onsave,
    className = "",
    visible = $bindable(true),
  } = $props();
</script>

{#if visible}
  <div
    class={`component ${className}`}
    transition:fly={{ duration: 150, y: 10 }}
  >
    <span class="text-base">{label}</span>
    <div class="flex flex-row gap-1">
      <Button onclick={oncancel}>Annuler</Button>
      <Button emphasize={true} onclick={onsave}>Sauvegarder</Button>
    </div>
  </div>
{/if}

<style>
  .component {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid #dddddd13;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
  }
</style>
