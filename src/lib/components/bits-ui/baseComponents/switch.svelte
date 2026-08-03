<script>
  import { Switch, Label, useId } from "bits-ui";

  let {
    id = useId(),
    checked = $bindable(false),
    ref = $bindable(null),
    onchange = () => {},
    label,
    ...restProps
  } = $props();

  export function toggle() {
    checked = !checked;
  }
</script>

<Switch.Root
  bind:checked
  bind:ref
  {id}
  {...restProps}
  class="focus-visible:ring-foreground focus-visible:ring-offset-background bg-dark-10 data-[state=unchecked]:shadow-mini-inset focus-visible:outline-hidden peer inline-flex h-7.5 w-12.5 shrink-0 cursor-pointer items-center rounded-full px-0.75 transition-colors focus-visible:ring-2 focus-visible:ring-offset-2"
  onclick={() => {
    onchange(checked);
  }}
>
  <Switch.Thumb
    class="bg-background data-[state=unchecked]:shadow-miniborder-background/30 data-[state=checked]:bg-white/60 shadow-popover pointer-events-none block size-6 shrink-0 rounded-full transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0 border"
  />
</Switch.Root>
{#if label}
  <Label.Root for={id}>{label}</Label.Root>
{/if}