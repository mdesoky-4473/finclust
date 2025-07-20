<script lang="ts">

	import ClusterBarChart from '$lib/ClusterBarChart.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/stores/auth';
	import { onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	let unsubscribe: () => void = () => {};
	let token: string | null = null;
	let users: any[] = [];
	let selectedAction = 'generate';
	let chosenK = 3;

	
	onMount(() => {
	if (browser) {
		unsubscribe = isAuthenticated.subscribe((auth) => {
			if (!auth) {
				goto('/login');
				return;
			}
			token = localStorage.getItem('token');
		});
		}
	});

	onDestroy(() => {
		unsubscribe();
	});

	async function handleAction() {

		if (!token) {
			alert("You are not authorized.");
			goto('/login');
			return;
		}

		if (selectedAction === 'generate') {
			const res = await fetch('http://localhost:8000/generate', {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const json = await res.json();
			users = json.data;
		} else if (selectedAction === 'cluster') {
			if (users.length === 0) {
				alert("Please generate users first.");
				return;
			}
			const res = await fetch(`http://localhost:8000/cluster?k=${chosenK}`, {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});
			const json = await res.json();
			users = json.clustered_data;
		}
	}

	let clusterCounts: Record<string, number> = {};

	$: if (users.length) {
		clusterCounts = users.reduce((acc, u) => {
			const desc = u.cluster_description ?? `Clusters ${u.cluster}`;
			acc[desc] = (acc[desc] || 0) + 1;
			return acc;
		}, {});
	}
	
</script>

<main class="min-h-screen flex flex-col items-center justify-start text-center p-6">

	<h1 class="text-3xl font-extrabold mb-6 tracking-tight text-gray-800 drop-shadow">
		FinClust: Financial Behavior Segmentation
	</h1>

	<div class="mb-8 flex flex-col sm:flex-row items-center gap-4">
		<select bind:value={selectedAction} class="bg-amber-500 text-white px-5 py-2 rounded-lg hover:bg-amber-600 shadow">
			<option value="generate">Generate Users</option>
			<option value="cluster">Cluster Users</option>
		</select>
		
		{#if selectedAction === 'cluster'}
			<div class="flex items-center gap-2 mr-2">
				<label for="cluster-k" class="text-sm text-gray-700 whitespace-nowrap">
					Choose number of clusters (k):
				</label>
				<input
					id="cluster-k"
					type="number"
					bind:value={chosenK}
					min="1"
					max="10"
					class="bg-amber-500 text-white px-4 py-2 rounded-lg hover:bg-amber-600 shadow text-center"
				/>
			</div>
		{/if}

		<button
			on:click={handleAction}
			class="bg-indigo-600 text-white px-5 py-2 rounded-lg hover:bg-indigo-700 shadow">
			Run Action
		</button>
	</div>

	{#if Object.keys(clusterCounts).length}
		<div class="mt-8 flex flex-col md:flex-row gap-6 justify-center items-start w-full max-w-6xl">
			<!-- Summary -->
			<div class="w-full max-w-md bg-white bg-opacity-90 p-4 rounded shadow">
				<h2 class="text-lg font-semibold mb-2">Cluster Summary</h2>
				<ul class="list-disc list-inside text-left text-gray-800">
					{#each Object.entries(clusterCounts) as [cluster, count]}
						<li>Cluster {cluster}: {count} users</li>
					{/each}
				</ul>
			</div>

			<!-- Chart -->
			<div class="w-full max-w-md">
				<ClusterBarChart data={clusterCounts} />
			</div>
		</div>
	{/if}


	{#if users.length === 0}
		<p class="mt-6 text-gray-600">No users generated yet. Click "Generate Users" to start.</p>
	{/if}


	{#if users.length > 0}
		<table class="mt-6 w-full border text-sm text-gray-800 bg-white bg-opacity-90">
			<thead>
				<tr class="bg-gray-100">
					<th class="p-2 border">Name</th>
					<th class="p-2 border">Age</th>
					<th class="p-2 border">Monthly Spend</th>
					<th class="p-2 border"># Txns</th>
					<th class="p-2 border">Savings</th>
					<th class="p-2 border">Cluster</th>
				</tr>
			</thead>
			<tbody>
				{#each users as user}
					<tr>
						<td class="p-2 border text-black">{user.name}</td>
						<td class="p-2 border text-black">{user.age}</td>
						<td class="p-2 border text-black">${user.monthly_spend}</td>
						<td class="p-2 border text-black">{user.num_txns}</td>
						<td class="p-2 border text-black">${user.savings}</td>
						<td class="p-2 border text-blue">{user.cluster}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}


</main>
