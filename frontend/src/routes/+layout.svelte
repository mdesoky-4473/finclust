<script lang="ts">
	import '../app.css';
	import { logout } from '$lib/auth';
	import { isAuthenticated } from '$lib/stores/auth';
</script>

<nav class="bg-gray-900 text-white px-6 py-4 shadow flex justify-between items-center">
	<h1 class="text-xl font-bold">
		<a href="/">FinClust</a>
	</h1>

	<div class="space-x-4">
		{#if $isAuthenticated}
			<a href="/" class="hover:underline">Dashboard</a>
			<button on:click={logout} class="hover:underline">Logout</button>
		{:else}
			<a href="/register" class="hover:underline">Register</a>
			<a href="/login" class="hover:underline">Login</a>
		{/if}
	</div>
</nav>

<main class="p-6">
	<slot />
</main>
