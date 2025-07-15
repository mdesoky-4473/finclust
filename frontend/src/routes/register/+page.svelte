<script lang="ts">
	import { goto } from '$app/navigation';
	import { onDestroy } from 'svelte';

	let email = '';
	let password = '';
	let confirm = '';
	let message = '';
	let loading = false;
	let timer: NodeJS.Timeout | undefined;

	async function register() {
		message = '';
		if (password !== confirm) {
			message = '❌ Passwords do not match';
			return;
		}
		loading = true;

		try {
			const res = await fetch('http://localhost:8000/auth/register', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (res.ok) {
				message = '✅ Registered! Redirecting to login…';
				timer = setTimeout(() => goto('/login'), 2000);
			} else {
				const err = await res.json();
				message = `❌ ${err.detail ?? 'Registration failed'}`;
			}
		} catch (e) {
			message = '❌ Could not reach server';
		} finally {
			loading = false;
		}
	}

	onDestroy(() => clearTimeout(timer));
</script>

<main class="min-h-screen flex flex-col items-center justify-center p-6">
	<h1 class="text-2xl font-bold mb-6 text-gray-800">Create an Account</h1>

	<form class="w-full max-w-sm space-y-4" on:submit|preventDefault={register}>
		<input
			class="w-full px-4 py-2 border rounded"
			type="email"
			placeholder="Email"
			bind:value={email}
			required
		/>

		<input
			class="w-full px-4 py-2 border rounded"
			type="password"
			placeholder="Password"
			bind:value={password}
			required
		/>

		<input
			class="w-full px-4 py-2 border rounded"
			type="password"
			placeholder="Confirm Password"
			bind:value={confirm}
			required
		/>

		<button
			class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
			type="submit"
			disabled={loading}>
			{loading ? 'Registering…' : 'Register'}
		</button>

		{#if message}
			<p class="text-center mt-2">{message}</p>
		{/if}

		<p class="text-center text-sm mt-4">
			Already have an account?
			<a href="/login" class="text-indigo-600 hover:underline">Log in</a>
		</p>
	</form>
</main>
