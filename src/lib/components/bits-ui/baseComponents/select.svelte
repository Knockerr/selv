<script>
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { path } from "@tauri-apps/api";
  import { Label, Select } from "bits-ui";
  import { untrack } from "svelte";

  let {
    value = $bindable(""),
    items,
    label,
    contentProps,
    iconPath = pathDb.cross,
    onchange = (v) => {},
    placeholder,
    className,
    style,
    width = "100%",
    ...others
  } = $props();
</script>

<div class="flex flex-col items-start gap-1 box-border" {...others}>
  {#if label}
    <p class="text-sm font-medium my-0">{label}</p>
  {/if}
  <Select.Root bind:value type="single">
    <Select.Trigger
      style={`width: ${width}; ${style}`}
      class={`h-input capitalize rounded-9px border-border-input bg-background-dark data-placeholder:text-foreground-alt/50 text-white inline-flex touch-none select-none items-center border px-2.75 text-sm transition-colors ${className}`}
    >
      <Icon path={iconPath} size="22px" />
      <Select.Value {placeholder} class="pl-1">
        {items.find((i) => i.value === value)?.label ?? placeholder}
      </Select.Value>
    </Select.Trigger>
    <Select.Portal>
      <Select.Content
        class="border-muted bg-background-dark shadow-popover data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 outline-hidden z-50 h-fit w-(--bits-select-anchor-width) min-w-(--bits-select-anchor-width) select-none rounded-xl border px-1 py-3 data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1 max-h-100 flex gap-0"
        {...contentProps}
      >
        <Select.Viewport>
          {#each items as { value, label, disabled } (value)}
            <Select.Item
              class="rounded-button data-highlighted:bg-muted outline-hidden data-disabled:opacity-50 flex w-full select-none items-center h-fit py-3 pl-5 pr-1.5 box-border text-sm capitalize"
              {value}
              {label}
              {disabled}
            >
              {#snippet children({ selected })}
                {label}
                {#if selected}
                  <div class="ml-auto flex items-center content-center">
                    <Icon path={pathDb.check} size="20px" />
                  </div>
                {/if}
              {/snippet}
            </Select.Item>
          {/each}
        </Select.Viewport>
      </Select.Content>
    </Select.Portal>
  </Select.Root>
</div>
