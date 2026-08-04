<script>
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { Combobox, mergeProps } from "bits-ui";

  let {
    items = [],
    value = $bindable(),
    open = $bindable(false),
    inputProps,
    contentProps,
    placeholder,
    label,
    iconPath,
    type,
    ...restProps
  } = $props();

  let searchValue = $state("");

  const filteredItems = $derived.by(() => {
    if (searchValue === "") return items;
    return items.filter((item) =>
      item.label.toLowerCase().includes(searchValue.toLowerCase()),
    );
  });

  function handleInput(e, currentTarget) {
    searchValue = e.currentTarget.value;
  }

  function handleOpenChange(newOpen) {
    if (!newOpen) searchValue = "";
  }

  const mergedRootProps = $derived(
    mergeProps(restProps, { onOpenChange: handleOpenChange }),
  );
  const mergedInputProps = $derived(
    mergeProps(inputProps, { oninput: handleInput }),
  );
</script>

<div class="relative flex flex-col gap-1">
  <p class="text-sm font-medium my-0">{label}</p>
  <Combobox.Root {type} {items} bind:value bind:open {...mergedRootProps}>
    <div class="relative w-fit">
      <Icon
        path={iconPath}
        className="text-muted-foreground absolute inset-s-3 top-1/2 size-6 -translate-y-1/2"
        size="20px"
      />
      <Combobox.Input
        {...mergedInputProps}
        class="h-input pl-11 box-border capitalize rounded-9px border-border-input bg-background-dark data-placeholder:text-foreground-alt/50 text-white inline-flex w-74 touch-none select-none items-center border px-2.75 text-sm transition-colors"
        {placeholder}
      />
      <Combobox.Trigger
        class="absolute inset-e-3 top-1/2 size-6 -translate-y-1/2 touch-none outline-none border-none right-4 bg-transparent"
        ><Icon path={pathDb.caretUpAndDown} size="20px" /></Combobox.Trigger
      >
    </div>
    <Combobox.Portal>
      <Combobox.Content
        class="no-scrollbar max-h-100 overflow-y-scroll border-muted bg-background-dark shadow-popover data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 outline-hidden z-50 h-fit min-w-40 select-none rounded-xl border px-1 py-3 data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1 w-full"
        {...contentProps}
      >
        {#each filteredItems as item, i (i + item.value)}
          <Combobox.Item
            {...item}
            class="rounded-button data-highlighted:bg-muted outline-hidden data-disabled:opacity-50 flex w-full select-none items-center h-fit py-3 pl-5 pr-1.5 box-border text-sm capitalize"
          >
            {#snippet children({ selected })}
              {item.label}
              {#if selected}
                <div class="ml-auto flex items-center content-center">
                  <Icon path={pathDb.check} size="20px" />
                </div>
              {/if}
            {/snippet}
          </Combobox.Item>
        {:else}
          <span class="block px-5 py-2 text-sm text-muted-foreground">
            No results found, try again.
          </span>
        {/each}
      </Combobox.Content>
    </Combobox.Portal>
  </Combobox.Root>
</div>
