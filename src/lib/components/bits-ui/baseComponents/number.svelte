<script>
  import Icon from "$lib/components/Icon.svelte";
  import { Label } from "bits-ui";

  let {
    placeholder,
    iconPath,
    label,
    className,
    width="100%",
    value = $bindable(""),
    ...others
  } = $props();
</script>

<div
  class={"flex flex-col items-start gap-1 relative -left-8 " + className}
  style:width
  {...others}
>
  {#if label}
    <Label.Root for={`input-${label}`} class="text-sm font-medium"
      >{label}</Label.Root
    >
  {/if}
  <div class="relative w-full">
    <input
      id={`input-${label}`}
      class="h-input rounded-card-sm border-border-input bg-background placeholder:text-foreground-alt/50 hover:border-dark-40 focus:ring-foreground focus:ring-offset-background focus:outline-hidden inline-flex w-full items-center border px-4 text-base focus:ring-2 focus:ring-offset-2 sm:text-sm text-white font-medium"
      {placeholder}
      bind:value
      type="number"
    />
  </div>
</div>

<style>
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input[type="number"] {
    -moz-appearance: textfield;
  }
</style>
