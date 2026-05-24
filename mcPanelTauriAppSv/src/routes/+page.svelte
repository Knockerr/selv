<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
  	import AuthCard from '$lib/components/authCard.svelte';
</script>

<div class="container">
	<AuthCard />
</div>

<style>
	.container{
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}
</style>
