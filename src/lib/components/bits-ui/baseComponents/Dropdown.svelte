<script>
  import Icon from "$lib/components/Icon.svelte";
  import { DropdownMenu } from "bits-ui";
  import Separator from "./Separator.svelte";
  import { pathDb } from "$lib/icons/pathDb";

  let { triggerSnippet, items } = $props();
  /* items should follow the following format: 
  [{ icon, label, type, onclick?, value?, childItems?, dangerous? }] with type in ["item", "checkItem", "subContent", "separator"]
  value concerns only checkItem, and childItems is for subContent type (childItems follow items pattern but only supports "item" type)
  */
  const itemsClass =
    "flex h-fit rounded-[8px] select-none items-center py-3 pl-3 pr-1.5 text-sm font-medium hover:bg-muted hover:cursor-pointer";

  function getLabelColor(dangerous) {
    if (!dangerous) return "var(--text-foreground)";
    else return "var(--dangerous)";
  }

  const iconSize = "17";
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger class="bg-transparent w-fit h-fit border-0">
    {@render triggerSnippet?.()}
  </DropdownMenu.Trigger>

  <DropdownMenu.Portal>
    <DropdownMenu.Content
      class="bg-background border-solid border-[1.5px] border text-foreground rounded-xl text-sm w-53 px-1 py-1.5 overflow-hidden"
      style="border-color: var(--muted) !important;"
    >
      {#each items as item}
        {#if item.type == "separator"}
          <Separator />
        {:else if item.type == "item" || !item.type}
          <DropdownMenu.Item
            onclick={item.onclick || (() => {})}
            class={itemsClass}
          >
            {#if item.icon}
              <div class="flex items-center justify-center relative -top-px">
                <Icon
                  path={item.icon}
                  size={iconSize}
                  color="var(--foreground-alt)"
                />
              </div>
            {/if}
            <span
              class="ml-2 font-medium flex items-center"
              style:color={getLabelColor(item.dangerous)}
            >
              {item.label}
            </span>
          </DropdownMenu.Item>
        {:else if item.type == "checkItem"}
          <DropdownMenu.CheckboxItem
            bind:checked={item.value}
            class={itemsClass}
            onclick={(() => {
              // TODO : This function could be made better
              item.onclick(!item.value);
            }) || (() => {})}
          >
            <div class="flex flex-row justify-between w-full">
              <div class="flex items-center justify-center">
                {#if item.icon}
                  <div
                    class="flex items-center justify-center relative -top-px"
                  >
                    <Icon
                      path={item.icon}
                      size={iconSize}
                      color="var(--foreground-alt)"
                    />
                  </div>
                {/if}
                <span
                  class="ml-2 font-medium flex items-center"
                  style:color={getLabelColor(item.dangerous)}
                >
                  {item.label}
                </span>
              </div>
              {#if item.value}
                <Icon
                  path={pathDb.check}
                  color="var(--foreground)"
                  size="15"
                  className="mr-4"
                />
              {/if}
            </div>
          </DropdownMenu.CheckboxItem>
        {:else if item.type == "subContent"}
          <DropdownMenu.Sub>
            <DropdownMenu.SubTrigger class={itemsClass}>
              <div class="flex flex-row justify-between w-full">
                <div class="flex items-center justify-center">
                  {#if item.icon}
                    <div
                      class="flex items-center justify-center relative -top-px"
                    >
                      <Icon
                        path={item.icon}
                        size={iconSize}
                        color="var(--foreground-alt)"
                      />
                    </div>
                  {/if}
                  <span
                    class="ml-2 font-medium flex items-center"
                    style:color={getLabelColor(item.dangerous)}
                  >
                    {item.label}
                  </span>
                </div>
                <Icon
                  path={pathDb.caretRight}
                  color="var(--foreground)"
                  size="15"
                  className="mr-2"
                />
              </div>
            </DropdownMenu.SubTrigger>
            <DropdownMenu.Portal>
              <DropdownMenu.SubContent
                class="bg-background overflow-hidden border-solid border-[1.5px] border text-foreground rounded-xl text-sm w-53 px-1 py-1.5"
                style="border-color: var(--muted) !important;"
                sideOffset={10}
              >
                {#each item.childItems as item}
                  <DropdownMenu.Item
                    onclick={item.onclick || (() => {})}
                    class={itemsClass}
                  >
                    {#if item.icon}
                      <div
                        class="flex items-center justify-center relative -top-px"
                      >
                        <Icon
                          path={item.icon}
                          size={iconSize}
                          color="var(--foreground-alt)"
                        />
                      </div>
                    {/if}
                    <span
                      class="ml-2 font-medium flex items-center"
                      style:color={getLabelColor(item.dangerous)}
                    >
                      {item.label}
                    </span>
                  </DropdownMenu.Item>
                {/each}
              </DropdownMenu.SubContent>
            </DropdownMenu.Portal>
          </DropdownMenu.Sub>
        {/if}
      {/each}
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
