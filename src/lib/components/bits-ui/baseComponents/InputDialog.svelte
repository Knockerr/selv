<script>
  import { uiStore } from "../uiComponentsStore.svelte";
  import Confirm from "./Confirm.svelte";
  import Input from "./Input.svelte";

  let {
    value = $bindable(),
    title,
    description,
    placeholder,
    onConfirm,
    name,
  } = $props();
</script>

<Confirm {title} {description} onConfirm={() => onConfirm(value)} {name}>
  <Input
    {placeholder}
    bind:value
    confirmLabel="Valider"
    className="mt-0 mb-3 relative -top-2"
  />
</Confirm>
