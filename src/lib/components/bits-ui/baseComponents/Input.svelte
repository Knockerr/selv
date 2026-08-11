<script>
  import Icon from "$lib/components/Icon.svelte";
  import { Label } from "bits-ui";

  let {
    placeholder,
    iconPath,
    label,
    className,
    style,
    width = "100%",
    value = $bindable(""),
    ...others
  } = $props();
</script>

<div class="flex flex-col items-start gap-1 box-border" style:width {...others}>
  {#if label}
    <Label.Root for={`input-${label}`} class="text-sm font-medium"
      >{label}</Label.Root
    >
  {/if}
  <div class="relative w-full">
    <input
      id={`input-${label}`}
      class={`h-input rounded-card-sm box-border border-border-input bg-background-dark placeholder:text-foreground-alt/50 hover:border-dark-40 focus:ring-foreground focus:ring-offset-background focus:outline-hidden inline-flex w-full items-center border px-4 text-base focus:ring-2 focus:ring-offset-2 sm:text-sm text-white font-medium ${className}`}
      {placeholder}
      {style}
      bind:value
    />
    <Icon
      className="absolute right-3 top-3"
      color="hsla(0, 0%, 96%, 0.3)"
      
      size="1.45rem"
      path={iconPath}
    />
  </div>
</div>
