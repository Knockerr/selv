<script>
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { Checkbox, Label } from "bits-ui";

  let { checked = $bindable(false), label, labelSnippet, id } = $props();
</script>

<div class="flex items-center space-x-3">
  <Checkbox.Root
    id={id}
    aria-labelledby={`${id}-label`}
    class="border-muted bg-foreground data-[state=unchecked]:border-border-input data-[state=unchecked]:bg-background data-[state=unchecked]:hover:border-dark-40 peer inline-flex size-4.75 items-center justify-center rounded-md border transition-all duration-150 ease-in-out active:scale-[0.98]"
    name="hello"
    bind:checked
  >
    {#snippet children({ checked })}
      <div class=" inline-flex items-center justify-center">
        {#if checked}
          <Icon size="12px" path={pathDb.check} color="#000" />
        {/if}
      </div>
    {/snippet}
  </Checkbox.Root>
  {#if label}
    <Label.Root
      id={`${id}-label`}
      for={id}
      class="text-[0.8rem] font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    >
      {#if labelSnippet}
        {@render labelSnippet?.()}
      {:else}
        {label}
      {/if}
    </Label.Root>
  {/if}
</div>
