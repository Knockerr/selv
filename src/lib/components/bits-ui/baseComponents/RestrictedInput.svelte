<script>
  import Icon from "$lib/components/Icon.svelte";
  import { Label } from "bits-ui";
  import { untrack } from "svelte";

  let {
    placeholder,
    iconPath,
    label,
    className,
    style,
    width = "100%",
    value = $bindable(""),
    password = false,
    labelProps,
    color = "",
    ending,
    onchange = () => {},
    realInputWidth = "100%",
    includeEnding = false,
    ...others
  } = $props();

  let inputValue = $state("");

  $effect(() => {
    inputValue;
    untrack(() => onchange());

    untrack(() => {
      if (!includeEnding) value = inputValue;
      else value = inputValue + ending;
    });
  });
</script>

<div
  class={`flex flex-col items-start gap-1 box-border ${className}`}
  style:width
  {...others}
>
  {#if label}
    <Label.Root
      for={`input-${label}`}
      class="text-sm font-medium"
      {...labelProps}>{label}</Label.Root
    >
  {/if}
  <div
    class="h-[40px] overflow-hidden rounded-card-sm box-border border-border-input bg-background-dark placeholder:text-foreground-alt/50 hover:border-dark-40 focus:ring-foreground focus:ring-offset-background focus:outline-hidden inline-flex items-center border px-4 text-base focus:ring-2 focus:ring-offset-2 sm:text-sm text-white font-sm"
    style:width
  >
    <input
      id={`input-${label}`}
      class="bg-background-dark h-full border-0 outline-0 text-white"
      style:width={realInputWidth}
      style:border-color={color || "var(--muted)"}
      {placeholder}
      {style}
      type={password ? "password" : "text"}
      bind:value={inputValue}
      autocomplete="off"
    />
    <span class="flex-1 border-px border-red text-white">{ending}</span>
    <Icon
      className="absolute right-3 top-3"
      color="hsla(0, 0%, 96%, 0.3)"
      size="1.45rem"
      path={iconPath}
    />
  </div>
</div>
