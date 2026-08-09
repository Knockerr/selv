<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import GridElem from "./gridElem.svelte";
</script>

<GridElem>
  <div class="card">
    <div class="pp"></div>
    <div class="name">John Smith</div>
    <div class="mail">johnsmith@gmail.com</div>
    <Button iconPath={pathDb.arrowRight} emphasize className="mt-2">Mon compte</Button>
  </div>
</GridElem>

<style>
  .card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    gap: 10px;
  }

  .pp {
    background-image: url("https://cdn.pixabay.com/photo/2015/11/16/14/43/cat-1045782_640.jpg");
    background-size: cover;
    border-radius: 50%;
    height: 70px;
    width: 70px;
  }

  .mail {
    font-size: 1rem;
  }
</style>
