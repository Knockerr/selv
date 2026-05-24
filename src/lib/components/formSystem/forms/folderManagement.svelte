<script>
  // @ts-nocheck

  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { onMount } from "svelte";
  import Form from "../form.svelte";
  import CheckboxField from "../mods/checkboxField.svelte";
  import checkboxField from "../mods/checkboxField.svelte";
  import SubTitle from "../mods/subTitle.svelte";
  import Title from "../mods/title.svelte";
  import TxtInput from "../mods/txtInput.svelte";

  let { folderName } = $props();

  let inputs = $derived([folderName]);

  let formRef;

  export const showForm = () => {
    formRef.showForm();
  }
</script>

<Form bind:this={formRef}>
  <Title title={`Gestion du dossier ${folderName}`} />
  <SubTitle content="Favori?" />
  <CheckboxField
    onChangeFn={folderSystem.toggleFavorite}
    {inputs}
    valueGetter={() => folderSystem.getFavoriteValue}
  />
  
</Form>
