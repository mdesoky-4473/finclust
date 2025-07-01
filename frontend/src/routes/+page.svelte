<script lang="ts">
	let users: any[] = [];
	let selectedAction = 'generate';

	async function handleAction() {
		if (selectedAction === 'generate') {
			const res = await fetch('http://localhost:8000/generate');
			const json = await res.json();
			users = json.data;
		} else if (selectedAction === 'cluster') {
			if (users.length === 0) {
				alert("Please generate users first.");
				return;
			}
			const res = await fetch('http://localhost:8000/cluster');
			const json = await res.json();
			users = json.clustered_data;
		}
	}

	let clusterCounts: Record<string, number> = {};

	$: if (users.length) {
		clusterCounts = users.reduce((acc, u) => {
			const c = u.cluster ?? "Unclustered";
			acc[c] = (acc[c] || 0) + 1;
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

		<button
			on:click={handleAction}
			class="bg-indigo-600 text-white px-5 py-2 rounded-lg hover:bg-indigo-700 shadow">
			Run Action
		</button>
	</div>

		{#if Object.keys(clusterCounts).length}
	<div class="mt-8 w-full max-w-md bg-white bg-opacity-90 p-4 rounded shadow">
		<h2 class="text-lg font-semibold mb-2">Cluster Summary</h2>
		<ul class="list-disc list-inside text-left text-gray-800">
			{#each Object.entries(clusterCounts) as [cluster, count]}
				<li>Cluster {cluster}: {count} users</li>
			{/each}
		</ul>
	</div>
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
