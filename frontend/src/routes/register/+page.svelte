<script lang="ts">
	import { goto } from '$app/navigation';
	import { onDestroy } from 'svelte';

	let email = '';
	let password = '';
	let confirm = '';
	let message = '';
	let loading = false;
	let timer: NodeJS.Timeout | undefined;
	const API_URL = import.meta.env.VITE_API_URL;

	async function register() {
		message = '';
		if (password !== confirm) {
			message = '❌ Passwords do not match';
			return;
		}
		loading = true;

		try {
			const res = await fetch(`${API_URL}/auth/register`, {
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

<main class="min-h-screen flex flex-col items-center justify-center px-4 py-10">
	<div class="w-full max-w-md bg-white bg-opacity-90 p-6 rounded shadow">
		<h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Create an Account</h1>

		<form class="space-y-4" on:submit|preventDefault={register}>
			<input
				class="w-full px-4 py-2 border border-gray-300 rounded text-gray-900"
				type="email"
				placeholder="Email"
				bind:value={email}
				required
			/>

			<input
				class="w-full px-4 py-2 border border-gray-300 rounded text-gray-900"
				type="password"
				placeholder="Password"
				bind:value={password}
				required
			/>

			<input
				class="w-full px-4 py-2 border border-gray-300 rounded text-gray-900"
				type="password"
				placeholder="Confirm Password"
				bind:value={confirm}
				required
			/>

			<button
				class="w-full bg-green-600 text-black px-5 py-2 rounded hover:bg-green-700 shadow"
				type="submit"
				disabled={loading}>
				{loading ? 'Registering…' : 'Register'}
			</button>

			{#if message}
				<p class="text-center text-sm mt-2">{message}</p>
			{/if}

			<p class="text-center text-sm mt-4 text-gray-600">
				Already have an account?
				<a href="/login" class="text-indigo-600 hover:underline">Log in</a>
			</p>
		</form>
	</div>
</main>
