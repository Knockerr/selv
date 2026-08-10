<script>
  import {
    Chart,
    Tooltip,
    defaultChartPadding,
    Layer,
    Axis,
    Spline,
    Highlight,
  } from "layerchart";
  import { format } from "@layerstack/utils";
  import { scaleLinear } from "d3-scale";
  import { range } from "d3-array";

  const { datas, labelName } = $props();

  const maxRam = $derived(Math.max(...datas.map((data) => data.ram)) + 1);
  // Little padding top limited to 5% because of huge values
  const maxCpu = 100;

  const color = {
    ram: "#5f69cbc0",
    cpu: "#5fb0cbc0",
    ramRaw: "#5f69cb",
    cpuRaw: "#5fb0cb",
  };

  // TODO : Implement pan zoom as in LayerChart doc
</script>

<Chart
  data={datas}
  x="time"
  y="cpu"
  y1="ram"
  yNice
  yDomain={[0, maxCpu]}
  y1Domain={[0, maxRam]}
  y1Range={({ yScale }) => yScale.domain()}
  padding={defaultChartPadding({ right: 10, top: 20, left: 40 })}
  height={350}
  tooltipContext={{ mode: "quadtree-x" }}
>
  {#snippet children({ context })}
    <Layer>
      <Axis
        placement="left"
        rule
        label="CPU"
        labelPlacement="middle"
        labelProps={{ dx: 10 }}
        stroke={color.cpuRaw}
      />
      <Axis
        placement="left"
        scale={scaleLinear(context.y1Scale?.domain() ?? [], [
          context.height + 1,
          0,
        ])}
        ticks={context.y1Scale?.ticks?.()}
        tickSpacing={500}
        rule
        label="RAM"
        labelPlacement="middle"
        labelProps={{
          dx: 10,
        }}
        x={-50}
        stroke={color.ramRaw}
      />
      <Axis placement="bottom" format="none" rule />
      <Spline class="stroke-2" stroke={color.cpu} />
      <Spline
        y={(d) => context.y1Scale?.(d.ram)}
        class="stroke-2"
        stroke={color.ram}
      />
      <Highlight lines points={{ style: `fill: ${color.cpu} !important;` }} />
      <Highlight
        points={{ style: `fill: ${color.ram} !important;` }}
        y={(d) => context.y1Scale?.(d.ram)}
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
        <Tooltip.Header value={data.time} />
        <Tooltip.List>
          <Tooltip.Item label="CPU" value={data.cpu} color={color.cpuRaw} />
          <Tooltip.Item label="RAM" value={data.ram} color={color.ramRaw} />
        </Tooltip.List>
      {/snippet}
    </Tooltip.Root>
  {/snippet}
</Chart>
