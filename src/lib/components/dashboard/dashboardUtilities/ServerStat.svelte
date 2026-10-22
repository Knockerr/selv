<script>
  import { PieChart, Tooltip } from "layerchart";
  const {
    graphType = "pie",
    title,
    description,
    data,
    width = "300px",
    height = "100%",
    tooltipLabel = "LABEL",
  } = $props();
</script>

<div class="component" style:height style:width>
  <div class="graph">
    {#if graphType == "pie"}
      <PieChart
        {data}
        key="key"
        value="value"
        label="key"
        innerRadius={-30}
        height={80}
      >
        {#snippet tooltip({ context })}
          <Tooltip.Root
            anchor="left"
            xOffset={20}
            contained={"container"}
            variant="none"
            class="text-2 bg-background/90 text-primary mt-[2px] p-2 border border-primary rounded-sm whitespace-nowrap"
          >
            {#snippet children({ data })}
              <Tooltip.Header
                value={data.key}
                style="text-transform: capitalize;"
              />
              <Tooltip.List>
                <Tooltip.Item
                  label={tooltipLabel}
                  value={data.valueFormatted ?? data.value}
                  color=""
                />
              </Tooltip.List>
            {/snippet}
          </Tooltip.Root>
        {/snippet}
      </PieChart>
    {/if}
  </div>
  <div class="infos">
    <span class="title">{title}</span>
    <span class="desc">{description}</span>
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: row;
    position: relative;
  }

  .graph {
    flex: 1;
  }

  .infos {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 80%;
    gap: 5px;
    max-width: 180px;
  }

  .title {
    font-size: 1.2rem;
    color: var(--foreground);
  }

  .desc {
    font-size: 0.9rem;
    color: var(--foreground-alt);
  }
</style>
