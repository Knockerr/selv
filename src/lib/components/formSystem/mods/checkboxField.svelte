<script>
  // @ts-nocheck
  let { inputs = [], onChangeFn, valueGetter = (x) => x } = $props();

  function changeHandler(e, input) {
    console.log('Click detected!')
    onChangeFn(input);
  }

  const currentValues = $derived.by(() => {
    const obj = {};
    for (const input of inputs) {
      obj[input] = valueGetter(input);
    }
    return obj;
  });
</script>

<div class="component">
  {#each inputs as input}
    <div class="flexRow" style="display:flex; flex-direction:row;">
      <p>{input}</p>
      <input
        type="checkbox"
        onchange={(e) => {changeHandler(e, input)}}
        value={currentValues[input]}
      />
    </div>
  {/each}
</div>

<style>
  .component {
    display: flex;
    flex-direction: row;
  }
  input {
    color: #ddd;
  }
</style>
