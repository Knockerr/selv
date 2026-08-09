<script>
  import {
    Chart,
    Tooltip,
    defaultChartPadding,
    Layer,
    Axis,
    Spline,
  } from "layerchart";
  import { format } from "@layerstack/utils";
  import { scaleLinear } from "d3-scale";
  import { range } from "d3-array";

  const { datas, labelName } = $props();

  $inspect(datas).with(() => {
    console.info("datas: > " + datas);
  });
</script>

<Chart
  data={datas}
  x="time"
  y="cpu"
  y1="ram"
  yDomain={[0, 1200]}
  y1Range={({ yScale }) => yScale.domain()}
  padding={defaultChartPadding({ right: 10 })}
  height={350}
  tooltipContext={{ mode: "quadtree-x" }}
>
  {#snippet children({ context })}
    <Layer>
      <Axis
        placement="left"
        rule
        label="Utilisation CPU"
        labelPlacement="start"
        labelProps={{ class: "fill-primary" }}
      />
      <Axis
        placement="right"
        scale={scaleLinear(context.y1Scale?.domain() ?? [], [
          context.height,
          0,
        ])}
        ticks={context.y1Scale?.ticks?.()}
        rule
        label="Utilisation RAM"
        labelPlacement="start"
        labelProps={{ class: "fill-secondary" }}
      />
      <Axis placement="bottom" format="none" rule />
      <Spline class="stroke-2 stroke-primary" />
      <Spline
        y={(d) => context.y1Scale?.(d.efficiency)}
        class="stroke-2 stroke-secondary"
      />

    </Layer>
    <Tooltip.Root
      anchor="left"
      xOffset={20}
      contained={"container"}
      variant="none"
      class="text-2 bg-background/90 text-primary mt-[2px] p-2 border border-primary rounded-sm whitespace-nowrap"
    >
      {#snippet children({ data })}
        <Tooltip.Header value={data.label} />
        <Tooltip.List>
          {#each datas as s}
            <Tooltip.Item
              label={s.key}
              value={s.data.find((d) => d.label === data.label).value}
              color={s.color}
            />
          {/each}
        </Tooltip.List>
      {/snippet}
    </Tooltip.Root>
  {/snippet}
</Chart>
