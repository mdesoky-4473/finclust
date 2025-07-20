<script lang="ts">
	import { goto } from '$app/navigation';
    import { isAuthenticated } from '$lib/stores/auth';

	let email = '';
	let password = '';
	let error = '';

	async function handleLogin() {
		error = '';
		try {
			const res = await fetch('http://localhost:8000/auth/jwt/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				},
				body: new URLSearchParams({
					username: email,
					password
				})
			});

			if (res.ok) {
                const token = (await res.json()).access_token;
                localStorage.setItem('token', token);
                isAuthenticated.set(true);
                goto('/');
			} else {
				error = 'Invalid email or password';
			}
		} catch (err) {
			error = 'Login failed. Try again.';
		}
	}
</script>

<main class="min-h-screen flex flex-col items-center justify-center px-4 py-10">
	<div class="w-full max-w-md bg-white bg-opacity-90 p-6 rounded shadow">
		<h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Login</h1>

		<form on:submit|preventDefault={handleLogin} class="space-y-4">
			<input
				type="email"
				bind:value={email}
				required
				placeholder="Email"
				class="w-full border border-gray-300 p-2 rounded text-gray-900"
			/>
			<input
				type="password"
				bind:value={password}
				required
				placeholder="Password"
				class="w-full border border-gray-300 p-2 rounded text-gray-900"
			/>
			<button
				type="submit"
				class="w-full bg-blue-600 text-black px-4 py-2 rounded hover:bg-blue-700"
			>
			Login
			</button>

			{#if error}
				<p class="text-red-500 text-sm mt-2 text-center">{error}</p>
			{/if}
		</form>
	</div>
</main>
