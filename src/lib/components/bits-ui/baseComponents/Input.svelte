<script>
  import Icon from "$lib/components/Icon.svelte";
  import { defineEnvVars } from "@sveltejs/kit/env";
  import { Label } from "bits-ui";
  import { onMount } from "svelte";

  let {
    placeholder,
    iconPath,
    label,
    className,
    style,
    width = "100%",
    value = $bindable(),
    password = false,
    labelProps,
    color = "",
    defaultValue = "",
    requirements,
    onblur = () => {},
    ...others
  } = $props();

  // If given, requirements is an array

  onMount(() => {
    if (defaultValue) value = defaultValue;
  });

  // TODO : Make password inputs able to switch display (dots to text yk)
</script>

<div class="flex flex-col items-start gap-1 box-border" style:width {...others}>
  {#if label}
    <Label.Root
      for={`input-${label}`}
      class="text-sm font-medium"
      {...labelProps}>{label}</Label.Root
    >
  {/if}
  <div class="relative w-full">
    <input
      id={`input-${label}`}
      class={`h-[40px] rounded-card-sm box-border border-border-input bg-background-dark placeholder:text-foreground-alt/50 hover:border-dark-40 focus:ring-foreground focus:ring-offset-background focus:outline-hidden inline-flex w-full items-center border px-4 text-base focus:ring-2 focus:ring-offset-2 sm:text-sm text-white font-medium ${className}`}
      style:border-color={color || "var(--muted)"}
      {placeholder}
      {style}
      type={password ? "password" : "text"}
      bind:value
      {onblur}
    />
    <Icon
      className="absolute right-3 top-3"
      color="hsla(0, 0%, 96%, 0.3)"
      size="1.45rem"
      path={iconPath}
    />
  </div>
  <div class="flex flex-col gap-0">
    {#if requirements}
      {#each requirements as req}
        <p class="requirements">{req}</p>
      {/each}
    {/if}
  </div>
</div>

<style>
  .requirements {
    color: var(--color-foreground-alt);
    font-size: 0.8rem;
    margin: 0;
  }
</style>
