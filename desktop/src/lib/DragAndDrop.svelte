<script lang="ts">
  import { readTextFile } from "@tauri-apps/api/fs";
  import { createEventDispatcher } from "svelte";
  import { listen } from "@tauri-apps/api/event";
  import { invoke } from "@tauri-apps/api";

  let beingDragged = false;
  let message = "Drag and drop files here";

  interface Item {
    id: string;
    image: string;
    title: string;
  }

  const dispatch = createEventDispatcher();

  listen("tauri://file-drop", async (event) => {
    if (beingDragged === true) {
      message = "Loading";
      const text = await readTextFile(event.payload[0] as string);

      const items: Item[] = await invoke("parse_content", { document: text });
      dispatch("datasubmit", { data: items });

      message = "Drag and drop files here";
    }
  });
</script>

<div
  class="drag-drop-container"
  on:mouseenter={() => {
    beingDragged = true;
  }}
  on:mouseleave={() => {
    beingDragged = false;
  }}
>
  <p>{@html message}</p>
</div>

<style>
  .drag-drop-container {
    border: 2px dashed #ccc;
    display: flex;
    padding: 20px;
    justify-content: center;
    cursor: pointer;
  }
</style>
