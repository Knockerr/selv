<script>
	import favicon from '$lib/assets/favicon.svg';
	import TopNavBar from '$lib/components/topNavBar.svelte';
    import SideBar from '$lib/components/sideBar.svelte'

	let { children } = $props();
</script>

<div class="container">
    <aside><SideBar /></aside>
	<div class="contentContainer">
		<TopNavBar />
		<main>{@render children()}</main>
	</div>
</div>

<style>
    .container{
        display: flex;
        flex-direction: row;
    }

    .contentContainer{
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    main{
        margin: 0;
        height: 100%;
        width: 100%;
        padding: 20px;
        box-sizing: border-box;
    }
</style>

